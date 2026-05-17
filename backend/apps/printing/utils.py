import numpy as np
from stl import mesh

# Constantes de coste. Se pueden ajustar segun los precios reales del material
DENSIDAD_PLA_G_CM3 = 1.24
COSTE_FILAMENTO_G = 0.05
GASTOS_OPERATIVOS = 2.00
MARGEN_BENEFICIO = 1.25


def calcular_metricas_stl(file_path: str) -> dict:
    """
    Lee un archivo STL, calcula su volumen con numpy-stl
    y devuelve el volumen, el peso y el precio estimado.
    """
    try:
        malla = mesh.Mesh.from_file(file_path)

        # get_mass_properties analiza los triangulos de la malla
        # y devuelve volumen, centro de gravedad e inercia
        volumen, _, _ = malla.get_mass_properties()

        # El volumen viene en mm3, lo pasamos a cm3
        volumen_cm3 = abs(volumen) / 1000.0

        peso_gramos = volumen_cm3 * DENSIDAD_PLA_G_CM3

        # Formula de precio: (peso * coste_material + gastos_fijos) * margen
        precio = (peso_gramos * COSTE_FILAMENTO_G + GASTOS_OPERATIVOS) * MARGEN_BENEFICIO

        return {
            'status': 'success',
            'volume_cm3': round(volumen_cm3, 2),
            'weight_grams': round(peso_gramos, 2),
            'price': round(precio, 2),
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
        }


def validar_archivo_stl(file) -> bool:
    """Comprueba que el archivo sea un STL valido antes de procesarlo."""
    try:
        header = file.read(80)
        file.seek(0)
        return len(header) >= 5
    except Exception:
        return False
