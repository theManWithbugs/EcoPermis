from django.urls import path
from core import views
from core.views import *

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/perfil', views.perfil, name='perfil'),
    path('home/editar_perfil/<str:id>/', views.editar_perfil, name='edit_perfil'),

    path('logout/', views.logoutView, name='logout'),

    path('home/', views.home, name='home'),

    path('home/search/', views.realizar_busca, name='search'),

    #Solicitar
    #--------------------------------------------------------------------------------------#
    path('home/solicitar/', views.realizar_solic, name='realizar_solic'),
    path('home/listar_solicitacoes/', views.listar_solicitacoes, name='listar_solic'),
    #--------------------------------------------------------------------------------------#
    path('home/info_pesquisa/<str:id>/', views.info_pesquisa, name='info_pesquisa'),

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

    #-------------------------------------------------------------------------------------#
    path('home/info_solic_ugai/<str:id>/', views.info_solic_ugai, name='info_solic_ugai'),

    path('home/aprovar_soli_ugai/<str:id>/', views.aprov_uso_ugai, name='aprov_uso_ugai'),

    #Json responses above here
    path('api/ped_ugais_naprov/', views.api_ugai_solicitadas, name='ugai_naprov'),
    #-------------------------------------------------------------------------------------#

    path('api/get_years/', views.resp_get_years, name='get_years'),

    path('api/render_api_page/', views.render_teste_page, name='render_api_page'),
    path('api/get_page_by_year/', views.get_page_by_year, name='get_year_page')
]
