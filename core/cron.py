from datetime import timezone
from django_q.models import Schedule

def iniciar_agendamentos():
    # Evita criar duplicado
    if not Schedule.objects.filter(func='core.tasks.verificar_status_pesquisa').exists():
        Schedule.objects.create(
            func='core.tasks.verificar_status_pesquisa',
            schedule_type=Schedule.DAILY,
            repeats=-1,
            next_run=timezone.now()
        )
