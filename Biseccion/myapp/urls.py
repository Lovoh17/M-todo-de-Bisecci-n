from django.urls import path
from . import views
#from django.urls import include, path

urlpatterns = [
    path('', views.home, name='home'),
    path('/Biseccion/myapp/templates/Biseccion/calcular_biseccion.html', views.calcular_biseccion, name='calcular_Biseccion'),
]
