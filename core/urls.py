from django.urls import path
from core import views
from core.views import *

urlpatterns = [
    path('pagina_sucess/', views.pagina_sucesso, name='pagina_sucesso'),

    path('', views.login_view, name='login'),
    path('home/login', views.perfil, name='perfil'),

    path('home/', views.home, name='home'),
    path('home/pesquisas_solic/', views.pesquisas_solic, name='pesquisas_solic'),
    path('home/info_pesquisa/<str:id>/', views.info_pesquisa, name='info_pesquisa'),

    #info_pesquisa only action
    path('aprovar_pesquisa/<str:id>/', views.aprovar_pesquisa, name='aprov_pesq'),
    path('excluir_arq/<str:id>/', views.excluir_arq, name='excluir_arq'),

    # Forms view
    path('home/dados_pessoais/', views.dados_pessoais, name='dados_pessoais'),
    path('home/solic_pesquisa/', views.solic_pesquisa, name='solic_pesq'),
]
