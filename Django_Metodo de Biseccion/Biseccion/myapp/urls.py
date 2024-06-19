from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('/Django_Metodo de Biseccion/Biseccion/myapp/templates/Biseccion/login.html', views.login_view, name='login'),
    path('/Django_Metodo de Biseccion/Biseccion/myapp/templates/Biseccion/registro.html', views.registro, name='registro'),
    path('/Django_Metodo de Biseccion/Biseccion/myapp/templates/Biseccion/creadores.html', views.creator_list, name='creator'),
    path('/Django_Metodo de Biseccion/Biseccion/myapp/templates/Biseccion/cambio_contraseña.html', views.cambio_contraseña, name='editar'),
    path('/Django_Metodo de Biseccion/Biseccion/myapp/templates/Biseccion/teoriaBiseccion.html', views.metodo_biseccion, name='teoriaB'),
    path('/Django_Metodo de Biseccion/Biseccion/myapp/templates/Biseccion/teoriaDif.html', views.mostrar_teoria, name='teoriaD'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('perfil/', views.perfil, name='perfil'),
    path('historial/', views.diferencias_historial, name='exercise_history'),
    #path('biseccion_historial.html/', views.biseccion_historial, name='biseccion_history'),
    path('/Biseccion/myapp/templates/Biseccion/calcular_biseccion.html', views.calcular_biseccion, name='calcular_Biseccion'),
    path('diferencias.html', views.diferencias, name='diferencias_divididas'),
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
