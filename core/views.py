from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from produtos.models import Produto
from vendas.models import Venda
# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["total_produtos"] = Produto.objects.filter(usuario=user).count()
        context["total_vendas"] = Venda.objects.filter(usuario=user).count()
        return context
