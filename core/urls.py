from django.urls import path
from core import views
from core.views import *

urlpatterns = [
    path('pagina_sucess/', views.pagina_sucesso, name='pagina_sucesso'),

    path('', views.login_view, name='login'),
    path('home/login', views.perfil, name='perfil'),

    path('home/', views.home, name='home'),
    path('home/pesquisas/', views.pesquisas, name='pesquisas'),
    path('home/info_pesquisa/<str:id>/', views.info_pesquisa, name='info_pesquisa'),

    # Forms view
    path('home/solic_pesquisa', views.solic_pesquisa, name='solic_pesq'),
    path('home/pagina_teste', views.pagina_test, name='pagina_teste')
]
