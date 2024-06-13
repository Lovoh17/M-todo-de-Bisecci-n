from django.db import models
from sympy import symbols, parse_expr

def biseccion(ec_values, valor_min, valor_max, error_porcentual):
    # Define la función f(x) usando sympy
    x = symbols('x')
    f = parse_expr(ec_values)
    
    # Convertir los valores mínimos y máximos a flotantes
    a = float(valor_min)
    b = float(valor_max)
    
    tol = error_porcentual / 100.0
    
    iter_count = 0
    iteraciones = []
    
    while (b - a) / 2.0 > tol:
        iter_count += 1
        midpoint = (a + b) / 2.0
        error = abs(b - a) / 2.0
        iteraciones.append([iter_count, round(midpoint, 4), round(error, 4)])
        
        if f.subs(x, midpoint) == 0:  # Raíz encontrada en el punto medio
            print(f"Iteración {iter_count}: Raíz encontrada en el punto medio")
            return midpoint, iter_count, 0, iteraciones
        
        elif f.subs(x, a) * f.subs(x, midpoint) < 0:  # La raíz está en [a, midpoint]
            b = midpoint
        else:  # La raíz está en [midpoint, b]
            a = midpoint
        
        print(f"Iteración {iter_count}: Intervalo actualizado [{round(a, 4)}, {round(b, 4)}]")
    
    raiz_aproximada = (a + b) / 2.0
    error = abs(b - a) / 2.0
    iteraciones.append([iter_count + 1, round(raiz_aproximada, 4), round(error, 4)])
    
    return raiz_aproximada, iter_count, error, iteraciones

def encontrar_intervalos(ec_values, valor_min, valor_max, paso):
    # Define la función f(x) usando sympy
    x = symbols('x')
    f = parse_expr(ec_values)
    
    # Convertir los valores mínimos y máximos a flotantes
    rango_min = float(valor_min)
    rango_max = float(valor_max)
    
    intervalos = []
    x_val = rango_min
    
    while x_val < rango_max:
        if f.subs(x, x_val) * f.subs(x, x_val + paso) < 0:
            intervalos.append((x_val, x_val + paso))
        x_val += paso
    
    return intervalos
