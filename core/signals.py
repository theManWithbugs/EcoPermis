from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_q.models import Schedule

@receiver(post_migrate)
def criar_cron(sender, **kwargs):
    if sender.name == "core":  # só roda quando a app core migra
        Schedule.objects.get_or_create(
            func='pesquisa.tasks.verificar_status_pesquisa',
            schedule_type=Schedule.CRON,
            cron='0 0 * * *',
        )
