from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True, max_length=100)
    imagen = models.ImageField(upload_to='perfiles/', default='perfiles/default.png')
    #contrasena = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.pk or not self.password.startswith('pbkdf2_'):  # Si es nuevo o no está encriptada
            self.set_password(self.password)
        super().save(*args, **kwargs)


class objeto(models.Model):
    nombre=models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='imagenes_objetos/', blank=True, null=True)
    imagen2= models.ImageField(upload_to='imagenes_objetos/', blank=True, null=True)
    imagen3= models.ImageField(upload_to='imagenes_objetos/', blank=True, null=True)
    propietario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mis_objetos')
    disponible = models.BooleanField(default=True)
   
    def __str__(self):
        return self.nombre

class SolicitudPrestamo(models.Model): 
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
        ('devuelto', 'Devuelto'),
    ]
    objeto = models.ForeignKey(objeto, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='solicitudes_enviadas')
    propietario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='solicitudes_recibidas')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    mensaje = models.TextField(blank=True, null=True) 
    mensaje_contacto = models.TextField(blank=True, null=True) 


    def __str__(self):
        return f"Solicitud de {self.solicitante.username} para {self.objeto.nombre}" 
