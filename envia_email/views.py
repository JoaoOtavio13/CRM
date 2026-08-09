from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
# Create your views here.

def envia_email_view(request):
    send_mail('Assunto','Esse é o email que estou enviando do Django', 'testeemailjo@gmail.com', ['joaootaviopessoahenrique@gmail.com'])
    return HttpResponse("Email enviado com sucesso!")