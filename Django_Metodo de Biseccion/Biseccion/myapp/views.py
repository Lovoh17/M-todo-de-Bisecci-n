from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
import sympy as sp
from .models import *
from sympy import *
import csv
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from sympy import symbols, lambdify
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def home(request):
    return render(request ,'Biseccion/home.html')

def login_forms(request):
    return render(request, 'Biseccion/login.html',)

def biseccion(ecuacion, a, b, tol_porcentual, max_iter=100):
    try:
        x = symbols('x')
        f = lambdify(x, ecuacion)  # Convertir la expresión simbólica a una función lambda
    except Exception as e:
        raise ValueError(f"No se pudo convertir la ecuación: {str(e)}")

    iter_count = 0
    iteraciones = []

    # Arrays para graficar la función y la raíz
    x_vals = np.linspace(a, b, 400)
    y_vals = f(x_vals)
    root_x_vals = []
    root_y_vals = []

    while True:
        iter_count += 1
        midpoint = (a + b) / 2.0
        error_absoluto = abs(b - a) / 2.0
        raiz_actual = midpoint
        
        # Calcular error porcentual
        if raiz_actual != 0:
            error_porcentual = abs(midpoint - a) / abs(midpoint) * 100
        else:
            error_porcentual = 0
        
        # Redondear los valores antes de agregarlos a iteraciones
        raiz_actual = round(raiz_actual, 4)
        error_absoluto = round(error_absoluto, 4)
        error_porcentual = round(error_porcentual, 4)
        
        # Agregar a iteraciones solo si es una nueva iteración o se ha alcanzado la tolerancia
        iteraciones.append([iter_count, raiz_actual, error_absoluto, error_porcentual])

        if error_porcentual < tol_porcentual or f(midpoint) == 0:
            break
        
        if f(a) * f(midpoint) < 0:
            b = midpoint
        else:
            a = midpoint

        if iter_count >= max_iter:
            break

        # Actualizar valores para graficar la raíz
        root_x_vals.append(midpoint)
        root_y_vals.append(f(midpoint))

    raiz_aproximada = (a + b) / 2.0
    error_absoluto = abs(b - a) / 2.0
    
    # Calcular el error porcentual final
    if raiz_aproximada != 0:
        error_porcentual = abs(raiz_aproximada - a) / abs(raiz_aproximada) * 100
    else:
        error_porcentual = 0
    
    # Redondear los valores finales
    raiz_aproximada = round(raiz_aproximada, 4)
    error_absoluto = round(error_absoluto, 4)
    error_porcentual = round(error_porcentual, 4)
    
    # Agregar la última iteración a iteraciones
    iteraciones.append([iter_count, raiz_aproximada, error_absoluto, error_porcentual])

    return raiz_aproximada, iter_count, error_absoluto, iteraciones, error_porcentual, x_vals, y_vals, root_x_vals, root_y_vals


#Usamos la funcion de la vista para traer los datos y mostrarlos
def calcular_biseccion(request):
    resultado_biseccion = None
    mensaje = None
    grafica_base64 = None

    if request.method == 'POST':
        form = BiseecionForm(request.POST)
        if form.is_valid():
            ec_values = form.cleaned_data['Ec_values']
            valor_min = float(form.cleaned_data['valor_min'])
            valor_max = float(form.cleaned_data['valor_max'])
            error_porcentual = float(form.cleaned_data['error_porcentual'])

            try:
                x = symbols('x')
                ecuacion = sympify(ec_values, locals={'sin': sin, 'cos': cos, 'tan': tan, 'exp': exp})
                resultado_biseccion = biseccion(ecuacion, valor_min, valor_max, error_porcentual)
                form = BiseecionForm()

                # Obtener datos para graficar
                raiz_aproximada, _, _, _, _, x_vals, y_vals, root_x_vals, root_y_vals = resultado_biseccion

                # Graficar la función y la raíz encontrada
                plt.figure(figsize=(8, 6))
                plt.plot(x_vals, y_vals, label='Función')
                plt.scatter(root_x_vals, root_y_vals, color='red', label='Raíz')
                plt.xlabel('x')
                plt.ylabel('f(x)')
                plt.title('Gráfica de la Función y Raíz Encontrada por Bisección')
                plt.legend()

                # Convertir la gráfica a base64 para mostrar en el template
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                grafica_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                buffer.close()

            except ValueError as e:
                mensaje = str(e)
    else:
        form = BiseecionForm()

    context = {
        'form': form,
        'resultado_biseccion': resultado_biseccion,
        'mensaje': mensaje,
        'grafica_base64': grafica_base64,
    }
    return render(request, 'Biseccion/calcular_biseccion.html', context)
#por el momento no jala 
def generar_pdf(request):
    resultado_biseccion = request.GET.get('resultado_biseccion')

    if not resultado_biseccion:
        return HttpResponse("No se encontraron resultados para generar el PDF.", content_type="text/plain")

    resultado_biseccion = json.loads(resultado_biseccion)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resultado_biseccion.pdf"'

    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 40, "Resultados de la Bisección")
    c.drawString(100, height - 60, f"Raíz aproximada: {resultado_biseccion[0]}")
    c.drawString(100, height - 80, f"Número de iteraciones: {resultado_biseccion[1]}")
    c.drawString(100, height - 100, f"Error absoluto: {resultado_biseccion[2]}")

    c.drawString(100, height - 140, "Iteraciones:")

    x_offset = 100
    y_offset = height - 160
    row_height = 20

    c.drawString(x_offset, y_offset, "Iteración")
    c.drawString(x_offset + 100, y_offset, "Raíz")
    c.drawString(x_offset + 200, y_offset, "Error absoluto")
    c.drawString(x_offset + 300, y_offset, "Error porcentual")

    for iteracion in resultado_biseccion[3]:
        y_offset -= row_height
        c.drawString(x_offset, y_offset, str(iteracion[0]))
        c.drawString(x_offset + 100, y_offset, str(iteracion[1]))
        c.drawString(x_offset + 200, y_offset, str(iteracion[2]))
        c.drawString(x_offset + 300, y_offset, str(iteracion[3]))

    c.showPage()
    c.save()

    return response