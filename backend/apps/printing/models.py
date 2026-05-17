from django.db import models
from django.contrib.auth.models import User


class CustomSTL(models.Model):
    STATUS_CHOICES = [
        ('UPLOADED', 'Subido - Pendiente de analisis'),
        ('CALCULATED', 'Precio calculado'),
        ('ERROR', 'Error en el archivo'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_stls', verbose_name="Usuario")
    file = models.FileField(upload_to='user_uploads/%Y/%m/%d/', verbose_name="Archivo STL")
    nombre_archivo = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UPLOADED')

    # Campos calculados con numpy-stl
    volume_cm3 = models.FloatField(null=True, blank=True, verbose_name="Volumen (cm3)")
    estimated_weight_gr = models.FloatField(null=True, blank=True, verbose_name="Peso (g)")
    calculated_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio calculado (euros)"
    )
    notas_cliente = models.TextField(blank=True, verbose_name="Instrucciones del cliente")

    def save(self, *args, **kwargs):
        # Guardamos primero para que el archivo tenga ruta en disco
        super().save(*args, **kwargs)

        # Solo calculamos si el archivo existe y aun no tiene precio
        if self.file and not self.calculated_price:
            from .utils import calcular_metricas_stl
            result = calcular_metricas_stl(self.file.path)

            if result['status'] == 'success':
                self.volume_cm3 = result['volume_cm3']
                self.estimated_weight_gr = result['weight_grams']
                self.calculated_price = result['price']
                self.status = 'CALCULATED'
            else:
                self.status = 'ERROR'

            # Guardamos solo los campos calculados para evitar recursion infinita
            super().save(update_fields=['volume_cm3', 'estimated_weight_gr', 'calculated_price', 'status'])

    def __str__(self):
        return f"STL de {self.user.username} - {self.nombre_archivo or self.id}"

    class Meta:
        verbose_name = "STL Personalizado"
        verbose_name_plural = "STLs Personalizados"
        ordering = ['-uploaded_at']
