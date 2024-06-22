####################################################################################################################################

#Librerias
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
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
from django.http import HttpResponseForbidden
import io
import os
import urllib, base64
import pandas as pd
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
from .models import Usuarios
from .models import DifferenceDividedHistory
from django.conf import settings

####################################################################################################################################

#Vista principal
def principal(request):
    return render(request ,'Biseccion/index.html')

####################################################################################################################################

def home(request):
    return render(request ,'Biseccion/home.html')

####################################################################################################################################

#Vista del login y validaciones
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo_User = form.cleaned_data['username']
            password_User = form.cleaned_data['password']
            # Autenticacion
            user = authenticate(request, username=correo_User, password=password_User)
            if user is not None:
                login(request, user)
                return redirect('principal')
            else:
                error_message = f"Usuario: {correo_User}, Contraseña: {password_User}"
                form.add_error(None, error_message)
    else:
        form = LoginForm()

    return render(request, 'Biseccion/login.html', {'form': form})

####################################################################################################################################

#Funcion para la teoria de Diferenciacion Numerica
def teoria_diferencias():
    teoria = """
    <h2>Diferencia hacia adelante:</h2>
    <p>La derivada hacia adelante se aproxima utilizando la siguiente fórmula:</p>
    <pre>f'(x) ≈ (f(x + h) - f(x)) / h</pre>
    <p>Donde:</p>
    <ul>
        <li>f(x): Valor de la función en el punto x.</li>
        <li>f(x + h): Valor de la función en el punto x + h.</li>
        <li>h: Tamaño del paso.</li>
    </ul>

    <h2>Diferencia hacia atrás:</h2>
    <p>La derivada hacia atrás se aproxima utilizando la siguiente fórmula:</p>
    <pre>f'(x) ≈ (f(x) - f(x - h)) / h</pre>
    <p>Donde:</p>
    <ul>
        <li>f(x): Valor de la función en el punto x.</li>
        <li>f(x - h): Valor de la función en el punto x - h.</li>
        <li>h: Tamaño del paso.</li>
    </ul>

    <h2>Diferencia central:</h2>
    <p>La derivada central se aproxima utilizando la siguiente fórmula:</p>
    <pre>f'(x) ≈ (f(x + h) - f(x - h)) / (2 * h)</pre>
    <p>Donde:</p>
    <ul>
        <li>f(x + h): Valor de la función en el punto x + h.</li>
        <li>f(x - h): Valor de la función en el punto x - h.</li>
        <li>h: Tamaño del paso.</li>
    </ul>
    """
    return teoria

####################################################################################################################################

def mostrar_teoria(request):
    contexto = {
        'explicacion_teorica': teoria_diferencias()
    }
    return render(request, 'Biseccion/teoriaDif.html', contexto)

####################################################################################################################################
#Funcion de la teoria de Biseccion
def metodo_biseccion(request):
    formulas = [
        {
            'titulo': 'Punto Medio del Intervalo',
            'formula': 'c = (a + b) / 2',
            'explicacion': 'Donde a y b son los extremos del intervalo inicial, y c es el punto medio.'
        },
        {
            'titulo': 'Criterio de Convergencia',
            'formula': 'f(c) = 0',
            'explicacion': 'El método de bisección determina si la raíz se encuentra en el intervalo izquierdo [a, c] o derecho [c, b] según el cambio de signo en la función evaluada en c.'
        },
        {
            'titulo': 'Actualización del Intervalo',
            'formula': 'Dependiendo del criterio de convergencia, se actualiza el intervalo de búsqueda para la siguiente iteración.',
            'explicacion': 'Si f(a) * f(c) < 0, se actualiza el intervalo a [a, c]. Si f(c) * f(b) < 0, se actualiza el intervalo a [c, b].'
        }
    ]
    
    explicacion_teorica = """
    En el método de bisección se utilizan varias fórmulas para iterar y encontrar la raíz de una ecuación dentro de un intervalo dado. 
    Las principales fórmulas que se emplean en este método son las siguientes:

    1. **Punto Medio del Intervalo**:
       c = (a + b) / 2
       donde a y b son los extremos del intervalo inicial, y c es el punto medio.

    2. **Criterio de Convergencia**:
       El método de bisección determina si la raíz se encuentra en el intervalo izquierdo [a, c] o derecho [c, b] según el cambio de signo en la función evaluada en c:
       - Si f(c) = 0, entonces c es la raíz.
       - Si f(a) * f(c) < 0, la raíz está en el intervalo [a, c].
       - Si f(c) * f(b) < 0, la raíz está en el intervalo [c, b].

    3. **Actualización del Intervalo**:
       Dependiendo del criterio de convergencia, se actualiza el intervalo de búsqueda para la siguiente iteración:
       - Si f(a) * f(c) < 0, se actualiza el intervalo a [a, c].
       - Si f(c) * f(b) < 0, se actualiza el intervalo a [c, b].

    Estas fórmulas y criterios son fundamentales para el funcionamiento del método de bisección, que es un método numérico básico pero efectivo para encontrar raíces de ecuaciones no lineales dentro de un intervalo dado.
    """

    context = {
        'formulas': formulas,
        'explicacion_teorica': explicacion_teorica,
    }
    
    return render(request, 'Biseccion/teoriaBiseccion.html', context)

####################################################################################################################################

# Función auxiliar para encontrar el intervalo inicial
def find_initial_interval(equation, x, x_start, x_end, step):
    f = sp.lambdify(x, equation, 'numpy')
    x_values = np.arange(x_start, x_end + step, step)
    y_values = f(x_values)
    
    intervals = []
    for i in range(len(x_values) - 1):
        if np.sign(y_values[i]) != np.sign(y_values[i + 1]):
            intervals.append((round(x_values[i], 4), round(x_values[i + 1], 4)))
    
    if len(intervals) == 0:
        return None
    elif len(intervals) > 1:
        return intervals[0]
    else:
        return intervals[0]

# Función auxiliar para el método de bisección
def bisection_method(a, b, tol, f):
    if f(a) * f(b) >= 0:
        return None, "El método de bisección no garantiza convergencia en este intervalo."
    
    iter_count = 0
    while True:
        c = (a + b) / 2
        
        if abs(f(c)) < tol:
            return round(c, 4), f"¡Se encontró la raíz aproximada dentro de la tolerancia! x = {round(c, 4)}"
        
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        
        iter_count += 1
    
    return round((a + b) / 2, 4), "Iteraciones completadas. La aproximación final de la raíz es x = {round((a + b) / 2, 4)}"


# Función auxiliar para generar las iteraciones
def generate_iterations(a, b, tol, f):
    iteraciones = []
    iter_count = 0
    previous_c = None
    
    while True:
        c = (a + b) / 2
        error = abs((c - previous_c) / c) if previous_c is not None else None
        
        iteraciones.append((iter_count, round(f(c), 4), round(c, 4), round(error, 4) if error is not None else None))
        
        if abs(f(c)) < tol:
            break
        
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        
        previous_c = c
        iter_count += 1
    
    return iteraciones


# Función auxiliar para generar una gráfica
def generate_plot(equation_str, x_start, x_end, raiz):
    # Crear un símbolo para la variable x
    x = sp.symbols('x')
    
    # Convertir la ecuación a un objeto simbólico
    equation = sp.sympify(equation_str)
    
    # Convertir la ecuación en una función numérica usando lambdify
    f = sp.lambdify(x, equation, 'numpy')
    
    # Crear datos para la gráfica
    x_values = np.linspace(x_start, x_end, 400)
    y_values = f(x_values)
    
    # Generar la gráfica usando matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, label='Función')
    plt.axhline(0, color='gray', linewidth=0.5)
    plt.axvline(raiz, color='red', linestyle='--', label='Raíz')
    plt.scatter(raiz, f(raiz), color='red')
    plt.title('Gráfica de la función y raíz encontrada')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    
    # Convertir la gráfica a base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    grafica_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return grafica_base64

def bisection_view(request):
    mensaje = None
    resultado_biseccion = None
    grafica_base64 = None
    
    if request.method == 'POST':
        form = BiseccionForm(request.POST)
        if form.is_valid():
            # Obtener datos del formulario
            equation_str = form.cleaned_data['equation']
            x_start = form.cleaned_data['x_start']
            x_end = form.cleaned_data['x_end']
            step = form.cleaned_data['step']
            tol = form.cleaned_data['tol']
            
            # Validar que x_start < x_end
            if x_start > x_end:
                mensaje = "El valor inicial del intervalo debe ser menor que el valor final."
            else:
                # Crear un símbolo para la variable x
                x = sp.symbols('x')
                
                # Convertir la ecuación a un objeto simbólico
                equation = sp.sympify(equation_str)
                
                # Encontrar el intervalo inicial
                interval = find_initial_interval(equation, x, x_start, x_end, step)
                if interval is None:
                    mensaje = "No se encontraron cambios de signo en el intervalo dado."
                else:
                    # Convertir la ecuación en una función numérica usando lambdify
                    f = sp.lambdify(x, equation, 'numpy')
                    
                    # Calcular la raíz usando el método de bisección
                    raiz, mensaje_raiz = bisection_method(interval[0], interval[1], tol, f)
                    
                    if raiz is not None:
                        # Preparar resultados
                        iteraciones = generate_iterations(interval[0], interval[1], tol, f)
                        iteraciones.append((raiz, None))  # Agregar la raíz final sin error
                        
                        # Preparar contexto para la plantilla
                        resultado_biseccion = (raiz, len(iteraciones) - 1, None, iteraciones, mensaje_raiz,f)
                        
                        # Generar gráfica
                        grafica_base64 = generate_plot(equation_str, x_start, x_end, raiz)
                        
                        if User.is_authenticated:
                            BiseccionHistory.objects.create(
                                user=request.user,
                                ecuacion=equation_str,
                                valor_min=x_start,
                                valor_max=x_end,
                                error_porcentual=tol,
                                raiz_aproximada=raiz,
                                iter_count=len(iteraciones) - 1,
                            )
                        
                    else:
                        mensaje = "El método de bisección no garantiza convergencia en este intervalo."
        
        else:
            mensaje = "Formulario inválido. Por favor, revise los datos ingresados."
    
    else:
        form = BiseccionForm()
    
    return render(request, 'Biseccion/calcular_biseccion.html', {
        'form': form,
        'mensaje': mensaje,
        'resultado_biseccion': resultado_biseccion,
        'grafica_base64': grafica_base64,
    })

####################################################################################################################################

# Función para calcular la derivada numérica usando diferencia hacia adelante
def derivada_forward(f, x, h):
    f_x = round(f(x), 4)
    f_x_plus_h = round(f(x + h), 4)
    resultado = round((f_x_plus_h - f_x) / h, 4)
    formula_sustituida = f"({f_x_plus_h} - {f_x}) / {h}"
    pasos = [
        f"f(x) = {f_x}",
        f"f(x + h) = {f_x_plus_h}",
        f"({f_x_plus_h} - {f_x}) / {h} = {resultado}"
    ]
    return resultado, formula_sustituida, pasos

####################################################################################################################################

# Función para calcular la derivada numérica usando diferencia hacia atras
def derivada_backward(f, x, h):
    f_x = round(f(x), 4)
    f_x_minus_h = round(f(x - h), 4)
    resultado = round((f_x - f_x_minus_h) / h, 4)
    formula_sustituida = f"({f_x} - {f_x_minus_h}) / {h}"
    pasos = [
        f"f(x) = {f_x}",
        f"f(x - h) = {f_x_minus_h}",
        f"({f_x} - {f_x_minus_h}) / {h} = {resultado}"
    ]
    return resultado, formula_sustituida, pasos

####################################################################################################################################

# Función para calcular la derivada numérica usando diferencia central
def derivada_central(f, x, h):
    f_x = round(f(x), 4)
    f_x_plus_h = round(f(x + h), 4)
    f_x_minus_h = round(f(x - h), 4)
    resultado = round((f_x_plus_h - f_x_minus_h) / (2 * h), 4)
    formula_sustituida = f"({f_x_plus_h} - {f_x_minus_h}) / (2 * {h})"
    pasos = [
        f"f(x) = {f_x}",
        f"f(x + h) = {f_x_plus_h}",
        f"f(x - h) = {f_x_minus_h}",
        f"({f_x_plus_h} - {f_x_minus_h}) / (2 * {h}) = {resultado}"
    ]
    return resultado, formula_sustituida, pasos

####################################################################################################################################

#Calcula error de las diferencias
def calcular_errores(derivada_fwd, derivada_bwd, derivada_cen, derivada_exacta_val):
    error_fwd = abs(derivada_fwd - derivada_exacta_val)
    error_bwd = abs(derivada_bwd - derivada_exacta_val)
    error_cen = abs(derivada_cen - derivada_exacta_val)
    
    return {
        'error_fwd': round(error_fwd, 4),
        'error_bwd': round(error_bwd, 4),
        'error_cen': round(error_cen, 4)
    }

####################################################################################################################################

#Funcion del metodo de diferenciacion numerica
def diferencias(request):
    resultado = {}
    grafica_url = ""
    
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
                
                derivada_exacta = diff(ecuacion, x)
                derivada_exacta_func = lambdify(x, derivada_exacta)
                derivada_exacta_val = round(derivada_exacta_func(valor_x), 4)

                derivada_fwd, formula_fwd, pasos_fwd = derivada_forward(f, valor_x, valor_h)
                derivada_bwd, formula_bwd, pasos_bwd = derivada_backward(f, valor_x, valor_h)
                derivada_cen, formula_cen, pasos_cen = derivada_central(f, valor_x, valor_h)

                errores = calcular_errores(derivada_fwd, derivada_bwd, derivada_cen, derivada_exacta_val)

                if request.user.is_authenticated:
                    DifferenceDividedHistory.objects.create(
                        user=request.user,
                        function=funcion,
                        x_value=valor_x,
                        h_value=valor_h,
                        derivada_fwd=derivada_fwd,
                        derivada_bwd=derivada_bwd,
                        derivada_cen=derivada_cen,
                        derivada_exacta=derivada_exacta_val,
                        error_fwd=errores['error_fwd'],
                        error_bwd=errores['error_bwd'],
                        error_cen=errores['error_cen']
                    )

                resultado = {
                    'derivada_fwd': derivada_fwd,
                    'formula_fwd': formula_fwd,
                    'pasos_fwd': pasos_fwd,
                    'derivada_bwd': derivada_bwd,
                    'formula_bwd': formula_bwd,
                    'pasos_bwd': pasos_bwd,
                    'derivada_cen': derivada_cen,
                    'formula_cen': formula_cen,
                    'pasos_cen': pasos_cen,
                    'derivada_exacta': derivada_exacta_val,
                    'error_fwd': round(errores['error_fwd'], 4),
                    'error_bwd': round(errores['error_bwd'], 4),
                    'error_cen': round(errores['error_cen'], 4)
                }
                
                x_vals = [valor_x - 2*valor_h, valor_x - valor_h, valor_x, valor_x + valor_h, valor_x + 2*valor_h]
                y_vals = [f(val) for val in x_vals]
                
                plt.figure()
                plt.plot(x_vals, y_vals, 'b-', label='Función')
                plt.plot(valor_x, f(valor_x), 'ro', label='Punto de Evaluación')
                plt.xlabel('x')
                plt.ylabel('f(x)')
                plt.title('Gráfica de la Función y Puntos Encontrados')
                plt.legend()
                
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                
                string = base64.b64encode(buf.read())
                grafica_url = 'data:image/png;base64,' + urllib.parse.quote(string)
                buf.close()

                messages.success(request, 'Cálculo de derivadas completado y guardado correctamente.')

            except ValueError as e:
                messages.error(request, f'Ocurrió un error de valor: {str(e)}')
            except SyntaxError as e:
                messages.error(request, f'Ocurrió un error de sintaxis en la ecuación: {str(e)}')
            except Exception as e:
                messages.error(request, f'Ocurrió un error durante el cálculo: {str(e)}')

    else:
        form = DiferenciacionForm()

    return render(request, 'Biseccion/diferencias.html', {'form': form, 'resultado': resultado, 'grafica_url': grafica_url})

####################################################################################################################################

#Funcion de nuevo registro de usuario
def registro(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {username}, tu cuenta ha sido creada exitosamente.')
                return redirect('home')
            else:
                messages.error(request, 'Hubo un problema al autenticarse. Inténtelo de nuevo.')
        else:
            messages.error(request, 'Error al crear la cuenta. Verifique los datos ingresados.')
    else:
        form = RegistroForm()

    return render(request, 'Biseccion/registro.html', {'form': form})

####################################################################################################################################

#Funcion del cambio de contraseña
def cambio_contraseña(request):
    mensaje = ""
    tipo_alerta = ""

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

####################################################################################################################################

#Funcion de cerrar secion
def cerrar_sesion(request):
    logout(request)
    return redirect('/')

####################################################################################################################################

#Vista para ver el perfil de usuario
@login_required
def perfil(request):
    user = request.user
    return render(request, 'Biseccion/perfil.html', {'user': user})

####################################################################################################################################

#Funcion para imprimir el proceso
def generar_pdf(request):
    resultado_biseccion = request.GET.get('resultado_biseccion')

    if not resultado_biseccion:
        return HttpResponse("No se encontraron resultados para generar el PDF.", content_type="text/plain")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resultado_biseccion.pdf"'

    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 40, "Resultados de la Bisección")

    c.drawString(100, height - 60, f"Raíz aproximada: {resultado_biseccion}")
    c.drawString(100, height - 80, "Número de iteraciones: No calculado")
    c.drawString(100, height - 100, "Error: No calculado")

    c.showPage()
    c.save()

    return response

####################################################################################################################################

#Funcion para filtrar el historial del usuario
@login_required
def diferencias_historial(request):
    history = DifferenceDividedHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'Biseccion/historial.html', {'history': history})

####################################################################################################################################

# Función para calcular la derivada numérica usando diferencia hacia atras
@login_required
def historial_biseccion(request):
    history = BiseccionHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'Biseccion/biseccion_historial.html', {'history': history})

####################################################################################################################################

# Función para mostrar el historial de los dos metodos
@login_required
def Historial_general(request):
    history = BiseccionHistory.objects.filter(user=request.user).order_by('-created_at')
    historydiferencias = DifferenceDividedHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'Biseccion/Historial_general.html', {'history': history, 'historydiferencias': historydiferencias})

####################################################################################################################################

# Función para mostrar los libros de biblioteca
def ver_biblioteca(request):
    json_path = os.path.join(settings.BASE_DIR, 'libros.json')
    with open(json_path, 'r') as file:
        libros = json.load(file)
    return render(request, 'Biseccion/biblioteca.html', {'libros': libros})

####################################################################################################################################

# Función para mostrar los videos de biblioteca
@login_required
def ver_videos(request):
    json_path = os.path.join(settings.BASE_DIR, 'videos.json')
    with open(json_path, 'r') as file:
        videos = json.load(file)
    return render(request, 'Biseccion/videos.html', {'videos': videos})

####################################################################################################################################

#Funcion para mostrar los desarrolladores del groyecto
def creator_list(request):
    return render(request, 'Biseccion/creadores.html')