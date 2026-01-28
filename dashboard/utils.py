from core.models import *
from collections import Counter
from django.forms.models import model_to_dict
from datetime import date
from django.db.models import Count

def tipo_solic_data(request):

  area_atuacao = [
    'NA', 'FAUNA', 'FLORA', 'ECOLOGIA', 'GEOLOGIA', 'SOCIOECONOMIA',
    'ARQUEOLOGIA', 'TURISMO', 'RECURSOS HIDRICOS', 'EDUCAÇÃO AMBIENTAL',
    'CAVIDADES NATURAIS','OUTROS'
  ]

  resultado = {}
  for x in area_atuacao:
    resultado[x] = DadosSolicPesquisa.objects.filter(area_atuacao=x).count()

  return resultado

def solic_uso_ugai(request):

  data_atual = date.today()
  ano_atual = data_atual.year

  ugais = [
    'UGAI LIBERDADE', 'UGAI ACURAUA', 'UGAI JURUPARI', 'UGAI ANTIMARY', 'UGAI CHANDLESS'
  ]

  resultado = {}
  for x in ugais:
    resultado[x] = SolicitacaoUgais.objects.filter(ugai=x, data_solicitacao__year=str(ano_atual)).count()

  return resultado
