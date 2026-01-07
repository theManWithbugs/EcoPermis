from django.utils import timezone
from models import DadosSolicPesquisa

def verificar_status_pesquisa():
    hoje = timezone.localdate()

    pesquisas = DadosSolicPesquisa.objects.filter(
        final_atividade__lt=hoje,
        status=True
    )

    for p in pesquisas:
        p.status = False
        p.save()
