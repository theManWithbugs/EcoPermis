from django.shortcuts import render
from django.http import JsonResponse
from .utils import *

def base(request):
  template_name = 'dashboard/base.html'
  return render(request, template_name)

def home(request):
  template_name = 'dashboard/home.html'
  return render(request, template_name)

def resp_bar_chart(request):
  dados = tipo_solic_data(request)
  return JsonResponse(dados, safe=False)

#Quantidade de solicitações de uso de ugai
def resp_solic_ugai(request):
  dados = solic_uso_ugai(request)
  return JsonResponse(dados, safe=False)