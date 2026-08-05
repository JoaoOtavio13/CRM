from django.shortcuts import render
from django.views.generic import TemplateView
from produtos.models import Produto
from vendas.models import Venda
# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

class DashboardView(TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_produtos"] = Produto.objects.count()
        context["total_vendas"] = Venda.objects.count()
        return context