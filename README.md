# 🐎 Sistema de Gestión de Rodeos

Sistema de consola desarrollado en Python para la gestión de inscripciones de rodeos, utilizando MongoDB como base de datos no relacional. Este proyecto corresponde a la **Evaluación Unidad Integradora N°4** de la asignatura TI3V32 — Bases de Datos No Estructuradas, INACAP Puente Alto.

---

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
  - [Menú Principal](#menú-principal)
  - [Menú de Búsquedas](#menú-de-búsquedas)
- [Funcionalidades](#funcionalidades)
  - [Create](#1-create---crear-inscripción)
  - [Read](#2-read---consultas-y-búsquedas)
  - [Update](#3-update---actualizaciones)
  - [Delete](#4-delete---eliminación)
  - [Exportar a Excel](#5-exportar-a-excel)
- [Estructura del Documento](#estructura-del-documento)
- [Autores](#autores)

---

## 📝 Descripción

Este sistema permite gestionar inscripciones de rodeos, almacenando información sobre clubes organizadores, contactos, criaderos y binomios (parejas de jinetes con sus caballos). Implementa un CRUD completo sobre MongoDB con operaciones avanzadas como búsquedas con operadores de comparación, expresiones regulares, rangos de fechas y consultas en subdocumentos.

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Descripción |
|------------|---------|-------------|
| Python | 3.x | Lenguaje de programación principal |
| PyMongo | 4.17.0 | Driver oficial de MongoDB para Python |
| MongoDB | 7.x | Base de datos NoSQL documental |
| Pandas | 2.3.3 | Manipulación y análisis de datos |
| OpenPyXL | 3.1.5 | Generación de archivos Excel (.xlsx) |
| python-dotenv | 0.9.9 | Gestión de variables de entorno |

---

## ⚙️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

1. **Python 3.8 o superior** — [Descargar Python](https://www.python.org/downloads/)
2. **MongoDB** (local o Atlas) — [Instalar MongoDB](https://www.mongodb.com/docs/manual/installation/)
3. **pip** (gestor de paquetes de Python, incluido por defecto)

> 💡 **Nota:** Si usas MongoDB Atlas (nube), necesitarás la URI de conexión de tu cluster.

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/sistema-gestion-rodeos.git
cd sistema-gestion-rodeos
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Contenido del `requirements.txt`:**
```
openpyxl==3.1.5
pandas==2.3.3
pymongo==4.17.0
dotenv==0.9.9
```

---

## 🔧 Configuración

El sistema utiliza variables de entorno para la conexión a MongoDB. Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Conexión a MongoDB Atlas
MONGODB_URI=mongodb+srv://usuario:contraseña@cluster.mongodb.net/

# O conexión local
# MONGODB_URI=mongodb://localhost:27017

# Nombre de la base de datos
DB_NAME=rodeos_db

# Nombre de la colección
COL_NAME=inscripciones
```

> ⚠️ **Importante:** Nunca subas el archivo `.env` a GitHub. Asegúrate de incluirlo en tu `.gitignore`.

---

## ▶️ Uso

Para ejecutar el sistema, simplemente corre:

```bash
python main.py
```

### Menú Principal

```
╔════════════════════════════════════════╗
║   SISTEMA DE GESTIÓN DE RODEOS 🐎      ║
╠════════════════════════════════════════╣
║ 1. Crear inscripción                   ║
║ 2. Buscar/Consultar                    ║
║ 3. Actualizar estado (raíz)            ║
║ 4. Actualizar jinete (array)           ║
║ 5. Eliminar inscripción                ║
║ 6. Exportar a Excel                    ║
║ 0. Salir                               ║
╚════════════════════════════════════════╝
```

### Menú de Búsquedas

```
╔════════════════════════════════════════╗
║          MENÚ DE BÚSQUEDAS             ║
╠════════════════════════════════════════╣
║ 1. Listar todos (proyección)           ║
║ 2. Operadores comparación ($ne/$in)    ║
║ 3. Expresión regular ($regex)          ║
║ 4. Rango de fechas ($gte/$lte)         ║
║ 5. Buscar en subdocumento (contacto)   ║
║ 0. Volver                              ║
╚════════════════════════════════════════╝
```

---

## 🎯 Funcionalidades

### 1. Create — Crear Inscripción

Registra una nueva inscripción de rodeo con los siguientes datos:

- **Club organizador** (obligatorio)
- **Contacto** (nombre, teléfono, email) — *subdocumento*
- **Criadero** (opcional)
- **Serie** (por defecto: "Libre")
- **Binomios** — *array de subdocumentos* con 2 jinetes, cada uno con:
  - Nombre del jinete
  - RUT
  - Nombre del caballo
  - Club de origen
- **Fecha de registro** (automática)
- **Estado** (por defecto: "Pendiente")

> 🔄 Soporta inserción múltiple (`insertMany`) si se agregan varias inscripciones seguidas.

### 2. Read — Consultas y Búsquedas

| Función | Operador MongoDB | Descripción |
|---------|-----------------|-------------|
| Listar todos | `find()` con proyección | Muestra club, criadero, fecha y estado |
| Operadores de comparación | `$ne`, `$in` | Excluye estado o filtra por lista de clubes |
| Expresión regular | `$regex` | Búsqueda insensible a mayúsculas en criaderos |
| Rango de fechas | `$gte`, `$lte` | Filtra inscripciones entre dos fechas |
| Subdocumento | dot notation + `$regex` | Busca contactos por nombre |

### 3. Update — Actualizaciones

- **Actualizar estado (campo raíz):** Modifica el estado de todas las inscripciones de un club usando `update_many`.
- **Actualizar jinete (dentro de array):** Modifica el club de origen de un jinete específico usando el operador posicional `$`.

### 4. Delete — Eliminación

Elimina una inscripción filtrando por el nombre del criadero usando `delete_one` con condición específica.

### 5. Exportar a Excel

Genera un archivo `Planilla_Oficial_Rodeo.xlsx` con todos los registros de la colección, excluyendo el campo `_id`.

---

## 📄 Estructura del Documento

```json
{
  "club_organizador": "Club de Rodeo Los Andes",
  "contacto": {
    "nombre": "Juan Pérez",
    "fono": "+56912345678",
    "email": "s/i"
  },
  "criadero": "Criadero El Volcán",
  "serie": "Libre",
  "binomios": [
    {
      "jinete": "Pedro Rojas",
      "rut": "12.345.678-9",
      "caballo": "Relámpago",
      "club_origen": "Club de Rodeo Los Andes"
    },
    {
      "jinete": "Luis Torres",
      "rut": "9.876.543-2",
      "caballo": "Trueno",
      "club_origen": "Club de Rodeo Los Andes"
    }
  ],
  "fecha_registro": ISODate("2026-05-15T18:00:00Z"),
  "estado": "Pendiente"
}
```

---

## 👥 Autores

- **Integrante 1** — [GitHub](https://github.com/usuario1)
- **Integrante 2** — [GitHub](https://github.com/usuario2)

**Docente:** Michael Arjel Mayerovich  
**Asignatura:** TI3V32 — Bases de Datos No Estructuradas  
**Sede:** INACAP Puente Alto  
**Sección:** 103-3A-F1  
**Fecha:** Mayo 2026

---

## 📜 Licencia

Proyecto académico desarrollado para fines educativos en INACAP.

---

> 🐎 *"El rodeo no es solo deporte, es tradición."*
