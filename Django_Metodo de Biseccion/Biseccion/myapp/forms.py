from django import forms
from .models import ExerciseHistory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from tinymce.widgets import TinyMCE
from .models import Profile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import sympy as sp

####################################################################################################################################
class BiseccionForm(forms.Form):
    equation = forms.CharField(
        label='Escriba la ecuación:',
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: x**2 + 5*3*x'}),
        required=True,
        max_length=100,
    )
    x_start = forms.FloatField(
        label='Ingrese el rango mínimo de búsqueda:',
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: -3'}),
        required=True,
    )
    x_end = forms.FloatField(
        label='Ingrese el rango máximo de búsqueda:',
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 3'}),
        required=True,
    )
    step = forms.FloatField(
        label='Ingrese el tamaño del paso para buscar intervalos:',
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 1'}),
        required=True,
    )
    tol = forms.FloatField(
        label='Ingrese el valor de la Tolerancia:',
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 0.001'}),
        required=True,
        min_value=0.0,
        max_value=100.0,
    )

    def clean(self):
        cleaned_data = super().clean()

        x_start = cleaned_data.get('x_start')
        x_end = cleaned_data.get('x_end')
        step = cleaned_data.get('step')

        if x_start >= x_end:
            raise ValidationError(_('El valor mínimo debe ser menor que el valor máximo.'))

        if step <= 0:
            raise ValidationError(_('El tamaño del paso debe ser mayor que cero.'))

        equation_str = cleaned_data.get('equation')
        try:
            # Intenta crear una expresión sympy a partir de la ecuación
            sp.sympify(equation_str)
        except sp.SympifyError:
            raise ValidationError(_('La ecuación ingresada no es válida.'))

        return cleaned_data

####################################################################################################################################

class DiferenciacionForm(forms.Form):
    f = forms.CharField(label='Escriba la ecuacion:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: x**2+5*3x'}))
    x = forms.CharField(label='Ingrese el valor de X:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 7'}))
    h = forms.CharField(label='Ingrese el valor de h', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 0.4'}))

    def clean_f(self):
        f_value = self.cleaned_data['f']
        try:
            sp.sympify(f_value)
        except SyntaxError:
            raise forms.ValidationError('La ecuación ingresada no es válida.')

        return f_value

    def clean_x(self):
        x_value = self.cleaned_data['x']
        try:
            float(x_value)
        except ValueError:
            raise forms.ValidationError('Ingrese un valor numérico válido para X.')

        return x_value

    def clean_h(self):
        h_value = self.cleaned_data['h']
        try:
            float(h_value)
        except ValueError:
            raise forms.ValidationError('Ingrese un valor numérico válido para h.')

        return h_value

    def clean(self):
        cleaned_data = super().clean()
        x_value = cleaned_data.get('x')
        h_value = cleaned_data.get('h')

        if x_value and h_value:
            x_float = float(x_value)
            h_float = float(h_value)

            if h_float == 0:
                raise forms.ValidationError('El valor de h no puede ser cero.')

        return cleaned_data

####################################################################################################################################

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

####################################################################################################################################
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile = Profile.objects.create(user=user)
            image = self.cleaned_data.get('image')
            if image:
                profile.image = image
                profile.save()
        return user 

####################################################################################################################################

class CambioContraseñaForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalización adicional si es necesario
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña actual'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nueva contraseña'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'})

####################################################################################################################################
class ExerciseHistoryForm(forms.ModelForm):
    class Meta:
        model = ExerciseHistory
        fields = ['exercise_name', 'duration', 'calories_burned']

####################################################################################################################################