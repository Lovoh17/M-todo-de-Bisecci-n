#Librerias
from django.shortcuts import render,redirect
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
import io
import base64
import pandas as pd
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
from .models import Usuarios
from .models import DifferenceDividedHistory
#Vista principal
def home(request):
    return render(request ,'Biseccion/home.html')
#Vista del login y validaciones

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo_User = form.cleaned_data['username']
            password_User = form.cleaned_data['password']
            
            # Autenticar al usuario con las credenciales ingresadas
            user = authenticate(request, username=correo_User, password=password_User)
            
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirigir a la vista deseada para usuarios autenticados
            else:
                # Agregar mensaje de error con credenciales ingresadas
                error_message = f"Usuario: {correo_User}, Contraseña: {password_User}"
                form.add_error(None, error_message)
    else:
        form = LoginForm()

    return render(request, 'Biseccion/login.html', {'form': form})
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

def mostrar_teoria(request):
    contexto = {
        'explicacion_teorica': teoria_diferencias()
    }
    return render(request, 'Biseccion/teoriaDif.html', contexto)
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
# Función para convertir la ecuación simbólica a función lambda y aplicar el método de bisección
def biseccion(ecuacion, a, b, tol_porcentual, max_iter=100):
    try:
        x = symbols('x')
        f = lambdify(x, ecuacion)  # Convertir la expresión simbólica a una función lambda
    except Exception as e:
        raise ValueError(f"No se pudo convertir la ecuación: {str(e)}")

    iter_count = 0
    iteraciones = []
    error = 100.0  # Inicializar el error alto para asegurar que entre en el bucle while
    prev_midpoint = None
    
    while error > tol_porcentual:
        iter_count += 1
        midpoint = (a + b) / 2.0
        
        # Evaluación de f(x) en el punto medio
        fx_mid = f(midpoint)
        
        # Calcular el error porcentual entre las aproximaciones sucesivas
        if prev_midpoint is not None:
            error = abs((midpoint - prev_midpoint) / midpoint) * 100
        else:
            error = 100.0
        
        # Redondear los valores antes de agregarlos a iteraciones
        raiz_actual = round(midpoint, 4)
        error = round(error, 4)
        
        # Agregar a iteraciones solo si es una nueva iteración o se ha alcanzado la tolerancia
        iteraciones.append([iter_count, f'F({raiz_actual})', raiz_actual, f'{error}%'])

        if fx_mid == 0:  # La raíz se encuentra exactamente en el punto medio
            break
        
        if f(a) * fx_mid < 0:
            b = midpoint
        else:
            a = midpoint
        
        prev_midpoint = midpoint
        
        if iter_count >= max_iter:
            break

    raiz_aproximada = (a + b) / 2.0
    
    # Calcular el error porcentual final
    if raiz_aproximada != 0:
        error_final = abs((raiz_aproximada - prev_midpoint) / raiz_aproximada) * 100
    else:
        error_final = 0
    
    # Redondear los valores finales
    raiz_aproximada = round(raiz_aproximada, 4)
    error_final = round(error_final, 4)
    
    # Agregar la última iteración a iteraciones
    iteraciones.append([iter_count, f'F({raiz_aproximada})', raiz_aproximada, f'{error_final}%'])

    return raiz_aproximada, iter_count, error_final, iteraciones
# Función para encontrar intervalos donde la función cambia de signo
def encontrar_intervalos(f, rango_min, rango_max, paso):
    intervalos = []
    x = rango_min
    while x < rango_max:
        if f(x) * f(x + paso) < 0:
            intervalos.append((x, x + paso))
        x += paso
    
    df_intervalos = pd.DataFrame(intervalos, columns=["Inicio Intervalo", "Fin Intervalo"])
    return df_intervalos
# Vista para calcular el método de bisección y mostrar resultados
def calcular_biseccion(request):
    resultado_biseccion = None
    mensaje = None
    grafica_base64 = None

    if request.method == 'POST':
        form = BiseecionForm(request.POST)
        if form.is_valid():
            ecuacion = form.cleaned_data['Ec_values']
            valor_min = float(form.cleaned_data['valor_min'])
            valor_max = float(form.cleaned_data['valor_max'])
            error_porcentual = float(form.cleaned_data['error_porcentual'])

            try:
                x = symbols('x')
                ecuacion = sympify(ecuacion, locals={'sin': sin, 'cos': cos, 'tan': tan, 'exp': exp})
                resultado_biseccion = biseccion(ecuacion, valor_min, valor_max, error_porcentual)

                # Obtener datos para graficar
                raiz_aproximada, _, _, iteraciones_data = resultado_biseccion

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

                # Convertir la gráfica a base64 para mostrar en la plantilla
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
# Función para calcular la derivada numérica usando diferencia hacia atras
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

def calcular_errores(derivada_fwd, derivada_bwd, derivada_cen, derivada_exacta_val):
    error_fwd = abs(derivada_fwd - derivada_exacta_val)
    error_bwd = abs(derivada_bwd - derivada_exacta_val)
    error_cen = abs(derivada_cen - derivada_exacta_val)
    
    return {
        'error_fwd': round(error_fwd, 4),
        'error_bwd': round(error_bwd, 4),
        'error_cen': round(error_cen, 4)
    }

@login_required
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
                x = sp.symbols('x')
                ecuacion = sp.sympify(funcion)
                f = sp.lambdify(x, ecuacion)

                # Calcular la derivada exacta
                derivada_exacta = sp.diff(ecuacion, x)
                derivada_exacta_func = sp.lambdify(x, derivada_exacta)
                derivada_exacta_val = round(derivada_exacta_func(valor_x), 4)

                # Calcular las derivadas utilizando los tres métodos
                derivada_fwd, formula_fwd, pasos_fwd = derivada_forward(f, valor_x, valor_h)
                derivada_bwd, formula_bwd, pasos_bwd = derivada_backward(f, valor_x, valor_h)
                derivada_cen, formula_cen, pasos_cen = derivada_central(f, valor_x, valor_h)

                # Calcular los errores
                errores = calcular_errores(derivada_fwd, derivada_bwd, derivada_cen, derivada_exacta_val)
               
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

                # Guardar el resultado en el historial
                DifferenceDividedHistory.objects.create(
                    user=request.user,
                    function=funcion,
                    x_value=valor_x,
                    h_value=valor_h,
                    derivada_fwd=derivada_fwd,
                    formula_fwd=formula_fwd,
                    pasos_fwd="\n".join(pasos_fwd),
                    derivada_bwd=derivada_bwd,
                    formula_bwd=formula_bwd,
                    pasos_bwd="\n".join(pasos_bwd),
                    derivada_cen=derivada_cen,
                    formula_cen=formula_cen,
                    pasos_cen="\n".join(pasos_cen),
                    derivada_exacta=derivada_exacta_val,
                    error_fwd=errores['error_fwd'],
                    error_bwd=errores['error_bwd'],
                    error_cen=errores['error_cen']
                )

                # Preparar los resultados para mostrar en la plantilla
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

            except Exception as e:
                resultado = {'error': str(e)}

    else:
        form = DiferenciacionForm()

    return render(request, 'Biseccion/diferencias.html', {'form': form, 'resultado': resultado, 'grafica_base64': grafica_base64})
#Funcion de nuevo registro de usuario
def registro(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
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
#Funcion de cerrar secion
def cerrar_sesion(request):
    logout(request)
    return redirect('/')
#Vista para ver el perfil de usuario
def perfil(request): 
    return render(request, 'Biseccion/perfil.html')
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

    # Mostrar raíz aproximada, número de iteraciones y error
    c.drawString(100, height - 60, f"Raíz aproximada: {resultado_biseccion}")
    c.drawString(100, height - 80, "Número de iteraciones: No calculado")
    c.drawString(100, height - 100, "Error: No calculado")

    c.showPage()
    c.save()

    return response

@login_required
def diferencias_historial(request):
    history = DifferenceDividedHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'Biseccion/historial.html', {'history': history})