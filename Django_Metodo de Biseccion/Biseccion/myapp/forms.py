from django import forms
from .models import ExerciseHistory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
class BiseecionForm(forms.Form):
    Ec_values = forms.CharField( label='Escriba la ecuacion:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: x**2+5*3x' ,'class': 'input_mdReserva' }))
    valor_min = forms.CharField(label='Ingrese el rango mínimo de búsqueda:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: -3','class': 'input_mdReserva'}))
    valor_max = forms.CharField(label='Ingrese el rango máximo de búsqueda', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 3','class': 'input_mdReserva'}))
    step = forms.CharField(label='Ingrese el tamaño del paso para buscar intervalos: ', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 1','class': 'input_mdReserva'}))
    error_porcentual = forms.CharField(label='Ingrese el valor de le Tolerancia', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 0.001','class': 'input_mdReserva'}))

class DiferenciacionForm(forms.Form):
    f = forms.CharField(label='Escriba la ecuacion:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: x**2+5*3x','class': 'input_mdReserva'}))
    x = forms.CharField(label='Ingrese el valor de X:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 7','class': 'input_mdReserva'}))
    h = forms.CharField(label='Ingrese el valor de h', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 0.4','class': 'input_mdReserva'}))


class LoginForm(forms.Form):
    username = forms.CharField(
    max_length=150,
    required=True,
    widget=forms.TextInput(attrs={'class': 'input_smReserva'})
)

    password = forms.CharField(
    widget=forms.PasswordInput(attrs={'class': 'input_smReserva'}),
    required=True
)


class RegistroForm(UserCreationForm):
    email = forms.EmailField(
    required=True,
    widget=forms.EmailInput(attrs={'class': 'input_smReserva'})
)
    first_name = forms.CharField(
    max_length=30,
    required=False,
    widget=forms.TextInput(attrs={'class': 'input_smReserva'})
)
    last_name = forms.CharField(
    max_length=30,
    required=False,
    widget=forms.TextInput(attrs={'class': 'input_smReserva'})
)


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'autofocus': False, 'class': 'input_mdReserva'}),
            'email': forms.EmailInput(attrs={'class': 'input_mdReserva'}),
            'first_name': forms.TextInput(attrs={'class': 'input_mdReserva'}),
            'last_name': forms.TextInput(attrs={'class': 'input_mdReserva'}),
            # Assuming password1 and password2 are using PasswordInput widget
            'password1': forms.PasswordInput(attrs={'class': 'input_mdReserva'}),
            'password2': forms.PasswordInput(attrs={'class': 'input_mdReserva'}),
        }
        
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
        return user
    
class CambioContraseñaForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalización adicional si es necesario
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña actual','class': 'input_mdReserva'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nueva contraseña','class': 'input_mdReserva'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña','class': 'input_mdReserva'})



class ExerciseHistoryForm(forms.ModelForm):
    class Meta:
        model = ExerciseHistory
        fields = ['exercise_name', 'duration', 'calories_burned']