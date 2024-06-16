from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('/Django_Metodo de Biseccion/Biseccion/myapp/templates/Biseccion/login.html', views.login_view, name='login'),
    path('/Django_Metodo de Biseccion/Biseccion/myapp/templates/Biseccion/registro.html', views.registro, name='registro'),
    path('/Django_Metodo de Biseccion/Biseccion/myapp/templates/Biseccion/cambio_contraseña.html', views.cambio_contraseña, name='editar'),
    path('/Django_Metodo de Biseccion/Biseccion/myapp/templates/Biseccion/teoriaBiseccion.html', views.metodo_biseccion, name='teoriaB'),
    path('/Django_Metodo de Biseccion/Biseccion/myapp/templates/Biseccion/teoriaDif.html', views.mostrar_teoria, name='teoriaD'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('perfil/', views.perfil, name='perfil'),
    path('/Biseccion/myapp/templates/Biseccion/calcular_biseccion.html', views.calcular_biseccion, name='calcular_Biseccion'),
    path('diferencion/', views.diferencias, name='diferencias_divididas'),
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),
]
