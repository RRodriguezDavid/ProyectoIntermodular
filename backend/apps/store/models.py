from django.db import models


class Category(models.Model):
    TIPO_CHOICES = [
        ('modelo', 'Modelo 3D'),
        ('filamento', 'Filamento'),
        ('consumible', 'Consumible'),
    ]
    name = models.CharField(max_length=100, verbose_name="Nombre")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='modelo')
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Product(models.Model):
    # Un producto puede ser un filamento con stock fijo o un modelo 3D con archivo STL
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripcion")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio base (euros)")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Categoria"
    )
    stock = models.IntegerField(default=0, verbose_name="Stock disponible")
    imagen = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Imagen")
    activo = models.BooleanField(default=True, verbose_name="Visible en tienda")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def tiene_stl(self):
        return hasattr(self, 'stl_model')

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at']


class STLModel(models.Model):
    # Modelo 3D vinculado a un producto. El archivo STL se usa en el visor Three.js
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stl_model')
    file = models.FileField(upload_to='stl_models/', verbose_name="Archivo STL")
    volume_cm3 = models.FloatField(null=True, blank=True, verbose_name="Volumen (cm3)")
    weight_gr = models.FloatField(null=True, blank=True, verbose_name="Peso estimado (g)")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"STL de {self.product.name}"

    class Meta:
        verbose_name = "Modelo STL"
        verbose_name_plural = "Modelos STL"
