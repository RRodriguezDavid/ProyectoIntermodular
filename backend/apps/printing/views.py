"""
Vistas para el servicio de impresión personalizada (subida de STL).
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomSTL
from .utils import validar_archivo_stl


@login_required
def upload_stl(request):
    """
    Vista para subir un archivo STL para impresión personalizada.
    Al guardar, el modelo calcula automáticamente el precio.
    """
    if request.method == 'POST' and request.FILES.get('stl_file'):
        archivo = request.FILES['stl_file']

        # Validación básica de extensión
        if not archivo.name.lower().endswith('.stl'):
            messages.error(request, 'Solo se aceptan archivos con extensión .stl')
            return render(request, 'printing/upload_stl.html')

        custom_stl = CustomSTL.objects.create(
            user=request.user,
            file=archivo,
            nombre_archivo=archivo.name,
            notas_cliente=request.POST.get('notas', ''),
        )

        if custom_stl.status == 'CALCULATED':
            messages.success(
                request,
                f'Archivo procesado. Volumen: {custom_stl.volume_cm3} cm³ | '
                f'Peso: {custom_stl.estimated_weight_gr} g | '
                f'Precio estimado: {custom_stl.calculated_price} €'
            )
            return redirect('printing:confirm', pk=custom_stl.pk)
        else:
            messages.error(request, 'Error al procesar el archivo STL. Verifica que sea un archivo válido.')
            custom_stl.delete()

    return render(request, 'printing/upload_stl.html')


@login_required
def confirm_print(request, pk):
    """Muestra el resumen del precio y permite añadir al carrito."""
    custom_stl = get_object_or_404(CustomSTL, pk=pk, user=request.user)
    return render(request, 'printing/confirm_print.html', {'custom_stl': custom_stl})


@login_required
def my_uploads(request):
    """Lista de archivos STL subidos por el usuario."""
    uploads = CustomSTL.objects.filter(user=request.user)
    return render(request, 'printing/my_uploads.html', {'uploads': uploads})
