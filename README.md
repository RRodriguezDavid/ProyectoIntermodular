# Print3D Shop - TFG DAM 2024/2025

Plataforma de venta de modelos 3D y servicio de impresion bajo demanda, desarrollada como Trabajo de Fin de Grado del ciclo de Desarrollo de Aplicaciones Multiplataforma.

## Stack tecnologico

| Capa | Tecnologia |
|---|---|
| Backend | Python / Django 4.2 |
| API REST | Django REST Framework + JWT |
| Frontend Web | Django Templates + Three.js |
| App Movil | Flutter (Dart) |
| Base de datos | PostgreSQL |
| Procesamiento 3D | numpy-stl |

---

## Puesta en marcha - Backend (Django)

### Requisitos previos
- Python 3.11 o superior
- PostgreSQL 15 o superior
- Git

### Instalacion

```bash
cd backend

& "C:\Users\david\AppData\Local\Programs\Python\Launcher\py.exe" -m venv venv
C:\Users\david\AppData\Local\Python\bin\python.exe -m venv venv
.\venv\Scripts\Activate.ps1            # Windows
# source venv/bin/activate     # Mac / Linux

python -m pip install -r requirements.txt
python -m pip install python-decouple dj-database-url
```

### Configurar la base de datos

```bash
copy .env.example .env        # Windows
# cp .env.example .env        # Mac / Linux
```

Editar `.env` con las credenciales de PostgreSQL y crear la base de datos:

```sql
CREATE DATABASE tfg_3d_db;
```

### Migraciones y superusuario

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Arrancar el servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

La web queda disponible en  http://127.0.0.1:8000
                            http://192.168.1.36:8000

---

## Puesta en marcha - App Flutter

### Requisitos previos
- Flutter SDK 3.x
- Android Studio o VS Code con el plugin Flutter

### Instalacion

```bash
cd mobile
flutter pub get
```

### Configurar la URL de la API

En `lib/services/auth_service.dart` y `lib/services/api_service.dart` hay que ajustar la URL base:
- Emulador Android: http://10.0.2.2:8000
- Dispositivo fisico: la IP local del PC, por ejemplo http://192.168.1.100:8000

### Ejecutar la app

```bash
flutter run -d chrome      # Chrome
```

---

## Estructura del proyecto

```
tfg-3d-marketplace/
├── backend/
│   ├── apps/
│   │   ├── users/    # Autenticacion y perfiles
│   │   ├── store/    # Catalogo de productos y modelos 3D
│   │   ├── cart/     # Carrito de compra con sesiones
│   │   ├── orders/   # Gestion de pedidos
│   │   └── printing/ # Servicio de impresion y calculo de precios
│   ├── api/          # Endpoints REST para Flutter
│   └── templates/    # Plantillas HTML
└── mobile/
    └── lib/
        ├── models/
        ├── services/
        ├── screens/
        └── widgets/
```

---

## Roles de usuario

| Rol | Acceso web | Acceso app |
|---|---|---|
| Cliente | Catalogo, carrito, subir STL, historial | Ver estado de sus pedidos |
| Administrador | Lo anterior mas panel de admin | Ver todos los pedidos y cambiar estado |

---

## Formula de calculo del precio de impresion

```
Precio = (Volumen_cm3 x Densidad_PLA x Coste_filamento + Gastos_fijos) x Margen
```

Valores por defecto configurables en `apps/printing/utils.py`:
- Densidad PLA: 1,24 g/cm3
- Coste filamento: 0,05 euros/g
- Gastos fijos: 2,00 euros
- Margen: 25%

---

## Endpoints de la API REST

| Metodo | Endpoint | Descripcion | Permiso |
|---|---|---|---|
| POST | /api/v1/token/ | Login, devuelve token JWT | Publico |
| POST | /api/v1/token/refresh/ | Renovar token | Publico |
| GET | /api/v1/me/ | Datos del usuario autenticado | Auth |
| GET | /api/v1/orders/ | Lista de pedidos | Auth |
| GET | /api/v1/orders/id/ | Detalle de un pedido | Auth |
| PATCH | /api/v1/orders/id/status/ | Cambiar estado del pedido | Solo Admin |
