# API de Votación - Django REST Framework

Una API RESTful desarrollada con Django REST Framework para gestionar un sistema de votación electrónica. Permite registrar votantes, candidatos y procesar votos con validaciones de integridad.

## 🚀 Características

- **Gestión de Votantes**: Registro y administración de votantes
- **Gestión de Candidatos**: Registro de candidatos con información de partido político
- **Sistema de Votación**: Procesamiento seguro de votos con validaciones
- **Estadísticas en Tiempo Real**: Consulta de resultados y métricas de participación
- **Validaciones de Integridad**: 
  - Un votante no puede ser candidato y viceversa
  - Cada votante solo puede votar una vez
  - No se pueden eliminar candidatos con votos
- **Autenticación JWT**: Seguridad mediante tokens JWT
- **API RESTful**: Endpoints bien estructurados siguiendo estándares REST

## 📊 Modelos de Datos

### Voter (Votante)
- `id`: Identificador único
- `name`: Nombre completo (máx. 101 caracteres)
- `email`: Email único
- `has_voted`: Booleano que indica si ya votó

### Candidate (Candidato)
- `id`: Identificador único
- `name`: Nombre completo (máx. 100 caracteres)
- `party`: Partido político (opcional)
- `email`: Email único
- `votes`: Contador de votos recibidos

### Vote (Voto)
- `id`: Identificador único
- `voter`: Relación OneToOne con Voter
- `candidate`: Relación ForeignKey con Candidate
- `voted_at`: Timestamp del momento del voto

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.2.3
- **API**: Django REST Framework
- **Base de Datos**: PostgreSQL
- **Autenticación**: JWT (Simple JWT)
- **CORS**: django-cors-headers
- **Python**: 3.x

## 📋 Prerrequisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python 3.8 o superior
- PostgreSQL
- pip (gestor de paquetes de Python)
- Git

## 🚀 Instrucciones para Ejecutar el Proyecto Localmente

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
```

### 2. Crear y Activar un Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos

#### Crear Base de Datos en PostgreSQL

#### Configurar settings.py

Edita el archivo `voting_api/settings.py` y actualiza la configuración de la base de datos:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'voting_db',           # Nombre de tu base de datos
        'USER': 'voting_user',         # Tu usuario de PostgreSQL
        'PASSWORD': 'tu_password',     # Tu contraseña
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Realizar Migraciones

```bash
# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario 
python manage.py createsuperuser
```

### 6. Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

## 📖 Documentación de la API

### Base URL
```
http://localhost:8000/api/
```

### Autenticación

La API utiliza autenticación JWT. Primero debes obtener un token:

```bash
POST /api/token/
Content-Type: application/json

{
    "username": "tu_usuario",
    "password": "tu_password"
}
```

Respuesta:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Endpoints Principales

#### Votantes
- `GET /api/voters/` - Listar todos los votantes
- `POST /api/voters/` - Crear un nuevo votante
- `GET /api/voters/{id}/` - Obtener un votante específico
- `PUT /api/voters/{id}/` - Actualizar un votante
- `DELETE /api/voters/{id}/` - Eliminar un votante (solo si no ha votado)

#### Candidatos
- `GET /api/candidates/` - Listar todos los candidatos
- `POST /api/candidates/` - Crear un nuevo candidato
- `GET /api/candidates/{id}/` - Obtener un candidato específico
- `PUT /api/candidates/{id}/` - Actualizar un candidato
- `DELETE /api/candidates/{id}/` - Eliminar un candidato (solo si no tiene votos)

#### Votos
- `GET /api/votes/` - Listar todos los votos
- `POST /api/votes/` - Registrar un nuevo voto
- `GET /api/votes/statistics/` - Obtener estadísticas de votación

### Ejemplos de Uso

#### Crear un Votante
```bash
POST /api/voters/
Authorization: Bearer <tu_token_jwt>
Content-Type: application/json

{
    "name": "Juan Pérez",
    "email": "juan@email.com"
}
```

#### Crear un Candidato
```bash
POST /api/candidates/
Authorization: Bearer <tu_token_jwt>
Content-Type: application/json

{
    "name": "María González",
    "party": "Partido Democrático",
    "email": "maria@email.com"
}
```

#### Registrar un Voto
```bash
POST /api/votes/
Authorization: Bearer <tu_token_jwt>
Content-Type: application/json

{
    "voter": 1,
    "candidate": 1
}
```

#### Obtener Estadísticas
```bash
GET /api/votes/statistics/
Authorization: Bearer <tu_token_jwt>
```

Respuesta:
```json
{
    "total_votes": 150,
    "total_voters": 200,
    "voters_who_voted": 150,
    "participation_rate": 75.0,
    "candidates_results": [
        {
            "id": 1,
            "name": "María González",
            "party": "Partido Democrático",
            "votes": 80,
            "percentage": 53.33
        },
        {
            "id": 2,
            "name": "Carlos López",
            "party": "Party Republicano",
            "votes": 70,
            "percentage": 46.67
        }
    ]
}
```

### Autenticación JWT
Obtención del token de acceso:
![image1](https://github.com/user-attachments/assets/7c61590e-dd27-4010-9d05-3e15c971f514)

#### Crear Votante
![image2](https://github.com/user-attachments/assets/b1c0b210-9897-4ede-8408-9015e6a4ce6c)

#### Obtener Votante Específico
![image3](https://github.com/user-attachments/assets/05981f76-f8c6-44c7-9bac-989e054bf2f2)

#### Crear Candidato
![image4](https://github.com/user-attachments/assets/b8db3b23-3ad0-4b6d-b5cc-1e13b1ff5a52)

### Sistema de Votación

#### Registrar Voto


#### Validación - Votante ya votó
![image7](https://github.com/user-attachments/assets/bea92f0c-4e4d-4e0a-8dd7-bd12e43dd472)

![image6](https://github.com/user-attachments/assets/486b40ce-982b-41ba-a74b-e1aeded3be54)


## 🔒 Validaciones de Seguridad

- **Unicidad de Email**: Cada email solo puede estar asociado a un votante O un candidato
- **Voto Único**: Cada votante solo puede emitir un voto
- **Integridad Referencial**: No se pueden eliminar candidatos con votos o votantes que ya votaron
- **Transacciones Atómicas**: Los votos se procesan de forma atómica para mantener consistencia


## 📝 Notas Adicionales

- El proyecto incluye configuración CORS para desarrollo
- La autenticación JWT está configurada por defecto
- Los candidatos se ordenan por número de votos (descendente) y nombre
- Los votantes se ordenan alfabéticamente por nombre
