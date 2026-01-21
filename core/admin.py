from django.contrib import admin
from core.models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(DadosSolicPesquisa)
admin.site.register(MembroEquipe)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass