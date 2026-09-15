"""Storage backends used by the project.

In production the media files uploaded by users (product images and profile
pictures) are stored on Cloudinary, because the filesystem of platforms like
Render is ephemeral and would lose the uploads on every deploy. Locally the
standard ``FileSystemStorage`` keeps saving files inside ``MEDIA_ROOT``.
"""

from urllib.request import urlopen

import cloudinary
import cloudinary.api
import cloudinary.exceptions
import cloudinary.uploader
from django.core.files.base import ContentFile
from django.core.files.storage import Storage


class CloudinaryMediaStorage(Storage):
    """Django storage backend that persists media files on Cloudinary."""

    resource_type = "image"

    def __init__(self, **options):
        self.options = options

    # -- helpers ----------------------------------------------------------
    @staticmethod
    def _normalize(name):
        return str(name).replace("\\", "/").lstrip("/")

    @classmethod
    def _public_id(cls, name):
        """Turn a storage name (``produtos/foto.png``) into a public ID."""
        normalized = cls._normalize(name)
        return normalized.rsplit(".", 1)[0] if "." in normalized else normalized

    # -- Storage API ------------------------------------------------------
    def _save(self, name, content):
        result = cloudinary.uploader.upload(
            content,
            public_id=self._public_id(name),
            resource_type=self.resource_type,
            overwrite=True,
            unique_filename=False,
            **self.options,
        )
        stored = result.get("public_id", self._public_id(name))
        image_format = result.get("format")
        return f"{stored}.{image_format}" if image_format else stored

    def _open(self, name, mode="rb"):
        with urlopen(self.url(name)) as response:  # noqa: S310 - trusted CDN URL
            return ContentFile(response.read(), name=name)

    def exists(self, name):
        try:
            cloudinary.api.resource(
                self._public_id(name), resource_type=self.resource_type
            )
        except cloudinary.exceptions.NotFound:
            return False
        return True

    def delete(self, name):
        try:
            cloudinary.uploader.destroy(
                self._public_id(name), resource_type=self.resource_type
            )
        except cloudinary.exceptions.NotFound:
            pass

    def url(self, name):
        return cloudinary.CloudinaryImage(self._public_id(name)).build_url(secure=True)

    def size(self, name):
        try:
            resource = cloudinary.api.resource(
                self._public_id(name), resource_type=self.resource_type
            )
        except cloudinary.exceptions.NotFound:
            return 0
        return resource.get("bytes", 0)

    def get_available_name(self, name, max_length=None):
        # Cloudinary public IDs are unique and uploads overwrite in place.
        return name