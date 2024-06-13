from django import forms

class BiseecionForm(forms.Form):
    Ec_values = forms.CharField(label='Escriba la ecuacion:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: x**2+5*3x'}))
    valor_min = forms.CharField(label='Ingrese el rango mínimo de búsqueda:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: -3'}))
    valor_max = forms.CharField(label='Ingrese el rango máximo de búsqueda', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 3'}))
    step = forms.CharField(label='Ingrese el tamaño del paso para buscar intervalos: ', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 1'}))
    error_porcentual = forms.CharField(label='Ingrese el valor de le Tolerancia', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 0.001'}))

