from django.urls import path
from core import views
from core.views import *

urlpatterns = [
    path('pagina_sucess/', views.pagina_sucesso, name='pagina_sucesso'),

    path('', views.login_view, name='login'),
    path('home/perfil', views.perfil, name='perfil'),
    path('home/editar_perfil/<str:id>/', views.editar_perfil, name='edit_perfil'),

    path('logout/', views.logoutView, name='logout'),

    path('home/', views.home, name='home'),

    path('home/info_pesquisa/<str:id>/', views.info_pesquisa, name='info_pesquisa'),

    #--------------------------------------------------------------------------------------#
    #Views that needs json response
    path('home/pesquisas_andam/', views.pesquisas_aprovadas, name='pesquisas_aprov'),
    path('home/pesquisas_n_aprov/', views.pesquisas_n_aprovadas, name='pesquisas_n_aprov'),

    #Json responses above here
    path('api/pesq_aprov_resp/', views.api_pesq_aprov, name='pesq_aprov_resp'),
    path('api/pesq_n_aprov_resp/', views.api_pesq_n_aprovadas, name='pesq_n_aprov_resp'),
    #--------------------------------------------------------------------------------------#

    path('home/minhas_solic/', views.minhas_solic, name='minhas_solic'),

    #info_pesquisa only action
    path('aprovar_pesquisa/<str:id>/', views.aprovar_pesquisa, name='aprov_pesq'),
    path('excluir_arq/<str:id>/', views.excluir_arq, name='excluir_arq'),

    # Forms view
    path('home/dados_pessoais/', views.dados_pessoais, name='dados_pessoais'),
    path('home/solic_pesquisa/', views.solic_pesquisa, name='solic_pesq'),
    path('home/solic_ugai/', views.solic_ugais, name='solic_ugai'),

    path('home/pagina_test/', views.pagina_teste, name='pagina_test')
]
