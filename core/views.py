from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

class DashboardView(TemplateView):
    template_name = "core/dashboard.html"