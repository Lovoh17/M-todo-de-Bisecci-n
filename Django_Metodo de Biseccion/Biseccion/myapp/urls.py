from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('/Django_Metodo de Biseccion/Biseccion/myapp/templates/Biseccion/login.html', views.login_forms, name='login'),
    path('/Biseccion/myapp/templates/Biseccion/calcular_biseccion.html', views.calcular_biseccion, name='calcular_Biseccion'),
    path('diferencion/', views.diferencias, name='diferencias_divididas'),
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),
]
