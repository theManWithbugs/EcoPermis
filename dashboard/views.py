from django.shortcuts import render
from django.http import JsonResponse
from .utils import *

import json
from django.http import JsonResponse

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
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
def api_js_chartjs(request):
  template_name = 'dashboard/api_estatisticas.html'
  return render(request, template_name)


#Return data to API
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
def solic_uso_ugai(year):

  ugais = [
    'UGAI LIBERDADE', 'UGAI ACURAUA', 'UGAI JURUPARI', 'UGAI ANTIMARY', 'UGAI CHANDLESS'
  ]

  resultado = {}
  for x in ugais:
    resultado[x] = SolicitacaoUgais.objects.filter(ugai=x, data_solicitacao__year=str(year)).count()

  return resultado

def get_solic_por_ori(year):
  sexos = ['M', 'F']

  objs = SolicitacaoUgais.objects.filter(
    data_solicitacao__year=str(year)).values('user_solic__usuario__sexo').annotate(total=Count('id'))

  resultado = {}
  for x in objs:
    #Pega a chave
    sexo = x.get('user_solic__usuario__sexo')
    #Coloca sexo como chave e total como valor da chave
    resultado[sexo] = x['total']

  return resultado
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

def solic_por_ori(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    year = data.get('year')

    objs = get_solic_por_ori(year)

    return JsonResponse({
      'status': 'ok',
      'objs': objs
    })

  return JsonResponse({'erro': 'Método inválido'}, status=400)

def resp_chart_js(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    year = data.get('year')

    objs = solic_uso_ugai(year)

    solic_por_ori(request)

    # objs_ori = SolicitacaoUgais.objects.values('user_solic__usuario__sexo')

    return JsonResponse({
      'status': 'ok',
      'objs': objs
    })

  return JsonResponse({'erro': 'Método inválido'}, status=400)
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#