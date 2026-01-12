from django.shortcuts import render

def base(request):
  template_name = 'dashboard/base.html'
  return render(request, template_name)

def home(request):
  template_name = 'dashboard/home.html'
  return render(request, template_name)