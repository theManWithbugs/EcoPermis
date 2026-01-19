from django.urls import path
from dashboard import views

app_name = "dashboard"

urlpatterns = [
  path('home/', views.home, name='home'),
  path('resp_tipo_solic/', views.resp_bar_chart, name='res_tipo_solic'),
  path('resp_solic_ugai/', views.resp_solic_ugai, name='resp_solic_ugai')
]