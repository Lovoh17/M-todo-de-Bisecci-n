from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
import sympy as sp
from .models import *
from sympy import *
def home(request):
    return render(request ,'Biseccion/home.html')

from sympy import symbols, lambdify

def biseccion(ecuacion, a, b, tol_porcentual, max_iter=100):
    x = symbols('x')
    f = lambdify(x, ecuacion)  # Convertir la expresión simbólica a una función lambda
    iter_count = 0
    iteraciones = []

    while True:
        iter_count += 1
        midpoint = (a + b) / 2.0
        error_absoluto = abs(b - a) / 2.0
        raiz_actual = midpoint
        
        # Calcular error porcentual
        if a != 0:
            error_porcentual = abs(midpoint - a) / abs(a) * 100
        else:
            error_porcentual = 0
        
        iteraciones.append([iter_count, round(raiz_actual, 4), round(error_absoluto, 4), round(error_porcentual, 4)])

        if error_porcentual < tol_porcentual:
            break
        
        if f(midpoint) == 0:
            return raiz_actual, iter_count, 0, iteraciones, error_porcentual
        elif f(a) * f(midpoint) < 0:
            b = midpoint
        else:
            a = midpoint

        if iter_count >= max_iter:
            break

    raiz_aproximada = (a + b) / 2.0
    error_absoluto = abs(b - a) / 2.0
    error_porcentual = abs(raiz_aproximada - a) / abs(raiz_aproximada) * 100
    iteraciones.append([iter_count + 1, round(raiz_aproximada, 4), round(error_absoluto, 4), round(error_porcentual, 4)])

    return raiz_aproximada, iter_count, error_absoluto, iteraciones, error_porcentual



#Usamos la funcion de la vista para traer los datos y mostrarlos
def calcular_biseccion(request):
    resultado_biseccion = None
    mensaje = None

    if request.method == 'POST':
        form = BiseecionForm(request.POST)
        if form.is_valid():
            ec_values = form.cleaned_data['Ec_values']
            # Convertimos a datos float
            valor_min = float(form.cleaned_data['valor_min'])
            valor_max = float(form.cleaned_data['valor_max']) 
            step = float(form.cleaned_data['step'])
            error_porcentual = float(form.cleaned_data['error_porcentual'])

            try:
                x = symbols('x')
                ecuacion = sympify(ec_values)
                resultado_biseccion = biseccion(ecuacion, valor_min, valor_max, error_porcentual)
            except Exception as e:
                mensaje = f"Error en el cálculo: {str(e)}"
    else:
        form = BiseecionForm()

    context = {
        'form': form,
        'resultado_biseccion': resultado_biseccion,
        'mensaje': mensaje,
    }

    return render(request, 'Biseccion/calcular_biseccion.html', context)