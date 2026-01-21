from django.urls import path
from dashboard import views

app_name = "dashboard"

urlpatterns = [
  path('home/', views.home, name='home'),
  path('resp_tipo_solic/', views.resp_bar_chart, name='res_tipo_solic'),
  path('resp_solic_ugai/', views.resp_solic_ugai, name='resp_solic_ugai'),

  #Teste de comunicação de API js com backend Django
  #URL de renderização da pagina
  path('js_chart/', views.api_js_chartjs, name='api_js_chart'),

  path('js_chart_resp/', views.resp_chart_js, name='chart_resp'),
  path('js_ori_resp/', views.solic_por_ori, name='ori_resp')
]