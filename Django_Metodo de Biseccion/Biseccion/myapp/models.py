
from django.db import models
from django.contrib.auth.models import User
##################################################################################################
class membresias(models.Model):
    id_membresia = models.AutoField(primary_key=True)
    categoria_membresia = models.CharField(max_length=200)


class Usuarios(models.Model):
    id_user = models.AutoField(primary_key=True)
    membresia_id_user = models.ForeignKey(membresias, on_delete=models.RESTRICT)
    nombre_User = models.CharField(max_length=200)
    apellido_User = models.CharField(max_length=200)
    correo_User = models.CharField(max_length=200)
    password_User = models.CharField(max_length=200)


class Historial(models.Model):
    id_Historial = models.AutoField(primary_key=True)
    id_user_Historial = models.ForeignKey(Usuarios, on_delete=models.RESTRICT)
    Procesos_Historial = models.TextField()

def __str__(self):
    return self.Procesos_Historial

class ExerciseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    date = models.DateField(auto_now_add=True)
    calories_burned = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.exercise_name} on {self.date}"
    
class DifferenceDividedHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    function = models.CharField(max_length=255)
    x_value = models.FloatField()
    h_value = models.FloatField()
    derivada_fwd = models.FloatField()
    formula_fwd = models.TextField()
    pasos_fwd = models.TextField()
    derivada_bwd = models.FloatField()
    formula_bwd = models.TextField()
    pasos_bwd = models.TextField()
    derivada_cen = models.FloatField()
    formula_cen = models.TextField()
    pasos_cen = models.TextField()
    derivada_exacta = models.FloatField()
    error_fwd = models.FloatField()
    error_bwd = models.FloatField()
    error_cen = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    
class BiseccionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ecuacion = models.CharField(max_length=255)
    valor_min = models.FloatField()
    valor_max = models.FloatField()
    error_porcentual = models.FloatField()
    raiz_aproximada = models.FloatField()
    iter_count = models.IntegerField()
    error_final = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"Bisección de '{self.ecuacion}' por {self.user.username}"

####################################################################################################################################