from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # Ampliamos el User de Django con datos adicionales del cliente
    # El campo is_staff del User ya diferencia entre Admin y Cliente
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"
