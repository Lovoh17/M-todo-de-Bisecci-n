from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import *
from django.contrib.auth import update_session_auth_hash
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
import io
import base64
import pandas as pd
from django.contrib import messages

def home(request):
    return render(request ,'Biseccion/home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Reemplazar con la vista deseada
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'Biseccion/login.html', {'form': form})

def biseccion(ecuacion, a, b, tol_porcentual, max_iter=100):
    try:
        x = symbols('x')
        f = lambdify(x, ecuacion)  # Convertir la expresión simbólica a una función lambda
    except Exception as e:
        raise ValueError(f"No se pudo convertir la ecuación: {str(e)}")

    iter_count = 0
    iteraciones = []

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
        iteraciones.append([iter_count, f'F({raiz_actual})', raiz_actual, error_porcentual])

        if error_porcentual < tol_porcentual or f(midpoint) == 0:
            break
        
        if f(a) * f(midpoint) < 0:
            b = midpoint
        else:
            a = midpoint

        if iter_count >= max_iter:
            break

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
    iteraciones.append([iter_count, f'F({raiz_aproximada})', raiz_aproximada, f'{error_porcentual}%'])

    return raiz_aproximada, iter_count, error_absoluto, iteraciones, error_porcentual

def encontrar_intervalos(f, rango_min, rango_max, paso):
    intervalos = []
    x = rango_min
    while x < rango_max:
        if f(x) * f(x + paso) < 0:
            intervalos.append((x, x + paso))
        x += paso
    
    df_intervalos = pd.DataFrame(intervalos, columns=["Inicio Intervalo", "Fin Intervalo"])
    return df_intervalos

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
                raiz_aproximada, _, _, iteraciones_data, _, _, _, _ = resultado_biseccion

                # Graficar la función y la raíz encontrada
                x_vals = np.linspace(valor_min, valor_max, 400)
                f = lambdify(x, ecuacion)
                y_vals = f(x_vals)

                plt.figure(figsize=(8, 6))
                plt.plot(x_vals, y_vals, label='Función')
                plt.axhline(0, color='black', linewidth=0.5)
                plt.axvline(raiz_aproximada, color='red', linestyle='--', label=f'Raíz aproximada: {raiz_aproximada}')
                
                for _, _, mid, _ in iteraciones_data:
                    plt.axvline(mid, color='blue', linestyle=':', linewidth=0.5)

                plt.scatter(raiz_aproximada, f(raiz_aproximada), color='red')
                plt.title('Método de Bisección')
                plt.xlabel('x')
                plt.ylabel('f(x)')
                plt.legend()
                plt.grid(True)

                # Convertir la gráfica a base64 para mostrar en el template
                buffer = io.BytesIO()
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


def derivada_forward(f, x, h):
    return (f(x + h) - f(x)) / h
# Función para calcular la derivada numérica usando diferencia hacia adelante
def derivada_backward(f, x, h):
    return (f(x) - f(x - h)) / h
# Función para calcular la derivada numérica usando diferencia central
def derivada_central(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

def diferencias(request):
    resultado = {}
    grafica_base64 = ""

    if request.method == 'POST':
        form = DiferenciacionForm(request.POST)
        if form.is_valid():
            funcion = form.cleaned_data['f']
            valor_x = float(form.cleaned_data['x'])
            valor_h = float(form.cleaned_data['h'])

            try:
                x = symbols('x')
                ecuacion = sympify(funcion)
                f = lambdify(x, ecuacion)

                # Calcular la derivada exacta
                derivada_exacta = diff(ecuacion, x)
                derivada_exacta_func = lambdify(x, derivada_exacta)
                derivada_exacta_val = derivada_exacta_func(valor_x)

                # Calcular las derivadas utilizando los tres métodos
                derivada_fwd = derivada_forward(f, valor_x, valor_h)
                derivada_bwd = derivada_backward(f, valor_x, valor_h)
                derivada_cen = derivada_central(f, valor_x, valor_h)

                # Calcular los errores
                error_fwd = abs(derivada_fwd - derivada_exacta_val)
                error_bwd = abs(derivada_bwd - derivada_exacta_val)
                error_cen = abs(derivada_cen - derivada_exacta_val)

                # Generar los puntos para la gráfica
                x_vals = np.linspace(valor_x - 2, valor_x + 2, 400)
                y_vals = f(x_vals)

                # Crear la gráfica
                plt.figure(figsize=(10, 6))
                plt.plot(x_vals, y_vals, label=f'f(x) = {funcion}')
                plt.scatter([valor_x], [f(valor_x)], color='red', zorder=1)
                
                # Mostrar la derivada exacta y las aproximaciones
                plt.scatter([valor_x], [derivada_exacta_val], color='blue', zorder=5)
                plt.scatter([valor_x], [derivada_fwd], color='green', zorder=5)
                plt.scatter([valor_x], [derivada_bwd], color='purple', zorder=5)
                plt.scatter([valor_x], [derivada_cen], color='orange', zorder=5)

                # Configurar la gráfica
                plt.title('Gráfica de la función y sus derivadas')
                plt.xlabel('x')
                plt.ylabel('f(x)')
                plt.legend()
                plt.grid(True)
                
                # Guardar la gráfica en un buffer
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                grafica_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                buffer.close()

                # Preparar los resultados para mostrar en la plantilla
                resultado = {
                    'derivada_fwd': round(derivada_fwd, 4),
                    'error_fwd': round(error_fwd, 4),
                    'derivada_bwd': round(derivada_bwd, 4),
                    'error_bwd': round(error_bwd, 4),
                    'derivada_cen': round(derivada_cen, 4),
                    'error_cen': round(error_cen, 4),
                    'derivada_exacta': round(derivada_exacta_val, 4)
                }

            except Exception as e:
                resultado = {'error': str(e)}

    else:
        form = DiferenciacionForm()

    return render(request, 'Biseccion/diferencias.html', {'form': form, 'resultado': resultado, 'grafica_base64': grafica_base64})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'Bienvenido {username}, tu cuenta ha sido creada exitosamente.')
            return redirect('home') 
    else:
        form = RegistroForm()
    return render(request, 'Biseccion/registro.html', {'form': form})

def cambio_contraseña(request):
    mensaje = ""
    tipo_alerta = ""  # Inicializar tipo_alerta fuera del bloque 'if'

    if request.method == 'POST':
        form = CambioContraseñaForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '¡Contraseña cambiada exitosamente!')
            return redirect('home')
        else:
            messages.error(request, 'Ha ocurrido un error. Por favor, verifica los datos ingresados.')
    else:
        form = CambioContraseñaForm(request.user)

    return render(request, 'Biseccion/cambio_contraseña.html', {'form': form, 'mensaje': mensaje, 'tipo_alerta': tipo_alerta})

def cerrar_sesion(request):
    logout(request)
    return redirect('/')

def perfil(request): 
    return render(request, 'Biseccion/perfil.html')
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