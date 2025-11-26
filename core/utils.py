
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