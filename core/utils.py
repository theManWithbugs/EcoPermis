from django.db import models
from .models import *

def format_data_br(data):
  data = data.split('-')

  data = f"{data[2]}/{data[1]}/{data[0]}"

  return data

def check_number(phone):
  DDD = str(f"({phone[:2]})")
  number = str(phone[2:])

  result = str(DDD + number)
  print(result)

def validador_cpf(cpf):
  numeros = [int(digito) for digito in cpf if digito.isdigit()]

  if len(numeros) != 11:
      return False

  soma1 = sum(a * b for a, b in zip(numeros[0:9], range(10, 1, -1)))
  digito1 = (soma1 * 10 % 11) % 10
  if numeros[9] != digito1:
      return False

  soma2 = sum(a * b for a, b in zip(numeros[0:10], range(11, 1, -1)))
  digito2 = (soma2 * 10 % 11) % 10
  if numeros[10] != digito2:
      return False

  return True

def calcular_data(data_inicio, data_final):

  data_inicio = data_inicio.split('-')
  data_final = data_final.split('-')

  qnt_anos = int(data_final[0]) - int(data_inicio[0])
  qnt_meses = int(data_final[1]) - int(data_inicio[1])

  if qnt_meses == 0:
    ano_txt = "ano" if qnt_anos == 1 else "anos"
    duracao = f"Duração de: {qnt_anos} {ano_txt}"
  else:
    ano_txt = "ano" if qnt_anos == 1 else "anos"
    mes_txt = "mês" if qnt_meses == 1 else "meses"
    duracao = f"Duração de: {qnt_anos} {ano_txt} e {qnt_meses} {mes_txt}"

  return duracao
