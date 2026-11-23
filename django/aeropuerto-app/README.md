# AeroGestión — aplicación de aeropuerto en Django

**Tema:** administración de operaciones de aeropuerto, aerolíneas, aeronaves y vuelos.  
**App Django:** `aeropuerto`  
**Base de datos predeterminada:** SQLite.

## Modelo de datos

```text
Aerolinea 1 ─────── * Aeronave
Aerolinea 1 ─────── * Vuelo
Aeropuerto * ────── * Aerolinea   (aerolíneas que operan en cada aeropuerto)
Aeropuerto 1 ────── * Vuelo       (vuelos de salida y de llegada)
Aeronave 1 ──────── * Vuelo
User 1 ──────────── * cada entidad (creado_por)
```

- **Aeropuerto:** código IATA, nombre, ciudad y país.
- **Aerolinea:** código, nombre y país de origen.
- **Aeronave:** matrícula, fabricante, modelo, capacidad y aerolínea propietaria.
- **Vuelo:** código, aerolínea, aeronave, origen, destino, fechas de salida/llegada y estado (`TextChoices`).
- Las entidades conservan quién las creó. Las relaciones de aeropuerto, aerolínea y aeronave impiden eliminar datos referenciados (`PROTECT`).

## Preparar desde cero

Requiere Python 3.12 o posterior.

```bash
cd django/aeropuerto-app
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows PowerShell:
# venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations aeropuerto
python manage.py migrate
python manage.py inicializar_aeropuerto
python manage.py check
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/`. El comando `inicializar_aeropuerto` se puede ejecutar otra vez: mantiene los datos de muestra sincronizados y crea los grupos y las cuentas de prueba.

## Grupos y permisos

| Grupo | Permisos |
|---|---|
| `administradores` | Consultar, crear, editar y eliminar los cuatro tipos de registro. |
| `consultores` | Consultar los registros; crear vuelos y editar/eliminar únicamente los vuelos que ellos mismos crearon. |

Las operaciones de escritura comprueban permisos en el servidor; ocultar botones en las plantillas no es la única protección. El cierre de sesión utiliza POST.

## Usuarios de prueba

Las credenciales son únicamente para la demostración local. Cámbielas antes de desplegar la aplicación.

| Usuario | Grupo | Contraseña | Uso |
|---|---|---|---|
| `admin_demo` | `administradores` (también superusuario) | `AdminDemo2026!` | Acceso completo y al admin de Django. |
| `consultor_demo` | `consultores` | `ConsultorDemo2026!` | Consulta y edición de sus propios vuelos. |
| `consultor2_demo` | `consultores` | `Consultor2Demo2026!` | Prueba de la regla de propiedad entre consultores. |

## Estructura

Los modelos, formularios, vistas y URLs se organizan por entidad en paquetes con `__init__.py` que re-exportan sus componentes. Las plantillas están en `aeropuerto/templates/aeropuerto/<entidad>/`. El administrador registra los cuatro modelos con filtros y búsqueda.

## Pruebas

```bash
python manage.py test
```
