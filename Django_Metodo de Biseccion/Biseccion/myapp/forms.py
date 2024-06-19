from django import forms
from .models import ExerciseHistory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
class BiseecionForm(forms.Form):
    Ec_values = forms.CharField(label='Escriba la ecuacion:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: x**2+5*3x'}))
    valor_min = forms.CharField(label='Ingrese el rango mínimo de búsqueda:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: -3'}))
    valor_max = forms.CharField(label='Ingrese el rango máximo de búsqueda', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 3'}))
    step = forms.CharField(label='Ingrese el tamaño del paso para buscar intervalos: ', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 1'}))
    error_porcentual = forms.CharField(label='Ingrese el valor de le Tolerancia', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 0.001'}))

class DiferenciacionForm(forms.Form):
    f = forms.CharField(label='Escriba la ecuacion:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: x**2+5*3x'}))
    x = forms.CharField(label='Ingrese el valor de X:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 7'}))
    h = forms.CharField(label='Ingrese el valor de h', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 0.4'}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            ext = image.name.split('.')[-1].lower()
            if ext not in ['png', 'jpg', 'jpeg']:
                raise forms.ValidationError("Solo se permiten archivos PNG, JPG o JPEG.")
        return image

        
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
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña actual'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nueva contraseña'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'})



class ExerciseHistoryForm(forms.ModelForm):
    class Meta:
        model = ExerciseHistory
        fields = ['exercise_name', 'duration', 'calories_burned']