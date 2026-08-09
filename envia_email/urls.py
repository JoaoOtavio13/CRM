from django.urls import path
from . import views

urlpatterns = [
    path('', views.envia_email_view, name='envia_email'),
]