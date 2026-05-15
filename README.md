# 🐎 Sistema de Gestión de Inscripciones de Rodeo

Sistema de terminal para gestionar inscripciones de rodeos chilenos, desarrollado con Python y MongoDB Atlas. Permite registrar clubes, criaderos, jinetes y sus binomios, además de generar planillas oficiales en Excel.

## 📋 Características

- ✅ Registro completo de inscripciones con datos de club, contacto y criadero
- 🏇 Gestión de colleras (binomios jinete-caballo)
- 📊 Generación automática de planilla oficial en Excel
- 🔍 Búsquedas por rango de fechas y texto (regex)
- ✏️ Actualización de estados y datos de jinetes
- 🗑️ Eliminación de registros
- 💾 Persistencia en MongoDB Atlas

## 🛠️ Tecnologías

- **Python 3.x**
- **MongoDB Atlas** (base de datos en la nube)
- **pymongo** - Driver oficial de MongoDB
- **pandas** - Procesamiento y exportación de datos
- **openpyxl** - Generación de archivos Excel
- **python-dotenv** - Gestión de variables de entorno

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd <nombre-del-directorio>
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto con la siguiente estructura:

```env
MONGODB_URI=mongodb+srv://usuario:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=nombre_base_datos
COL_NAME=nombre_coleccion
```

**Importante:** Obtén tu URI de conexión desde [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

## 🚀 Uso

Ejecutar el programa:

```bash
python main.py
```

### Menú Principal

```
1. Crear      - Nueva inscripción con collera completa
2. Listar     - Mostrar registros y generar Excel automáticamente
3. Fecha      - Buscar por rango de fechas (mayo 2026)
4. Regex      - Buscar por nombre de criadero
5. Estado     - Actualizar estado de club
6. Jinete     - Actualizar club de origen de jinete
7. Eliminar   - Eliminar registro por criadero
0. Salir      - Cerrar aplicación
```

## 📄 Estructura de Datos

### Documento de Inscripción

```javascript
{
  "_id": ObjectId("..."),
  "club_organizador": "Club El Rodeo",
  "contacto": {
    "nombre": "Juan Pérez",
    "fono": "+56912345678",
    "email": "s/i"
  },
  "criadero": "Los Aromos",
  "serie": "Libre",
  "binomios": [
    {
      "jinete": "Pedro González",
      "rut": "12345678-9",
      "caballo": "Relámpago",
      "club_origen": "Club El Rodeo"
    },
    {
      "jinete": "María Silva",
      "rut": "98765432-1",
      "caballo": "Centella",
      "club_origen": "Club El Rodeo"
    }
  ],
  "fecha_registro": ISODate("2026-05-14T..."),
  "estado": "Pendiente"
}
```

## 📊 Exportación de Datos

La opción **"2. Listar"** genera automáticamente el archivo:

```
Planilla_Oficial_Rodeo.xlsx
```

Este archivo contiene todos los registros en formato tabular, listo para impresión o distribución.

## 🔍 Ejemplos de Uso

### Crear Nueva Inscripción

```
1. Seleccionar opción "1"
2. Ingresar club organizador (obligatorio)
3. Ingresar nombre del contacto (obligatorio)
4. Ingresar criadero (opcional, se asigna "N/A" por defecto)
5. Ingresar teléfono
6. Registrar datos de 2 jinetes (nombre, RUT, caballo)
7. Confirmación con ID de MongoDB
```

### Buscar por Fecha

La opción "3" busca automáticamente registros de mayo 2026. Para personalizar:

```python
inicio = datetime(2026, 5, 1)
fin = datetime(2026, 5, 31)
```

### Actualizar Jinete

Permite cambiar el club de origen de un jinete usando el operador posicional `$` de MongoDB:

```
6. Jinete
RUT jinete: 12345678-9
Nuevo club: Club Los Andes
```

## 🔒 Seguridad

- ⚠️ **Nunca subas el archivo `.env` al repositorio**
- ✅ Asegúrate de que `.env` esté en `.gitignore`
- 🔐 Usa contraseñas fuertes en MongoDB Atlas
- 🌐 Configura IP whitelist en Atlas para mayor seguridad

## 📝 Archivos del Proyecto

```
.
├── main.py                 # Aplicación principal
├── requirements.txt        # Dependencias Python
├── .env                    # Variables de entorno (NO SUBIR)
├── .gitignore             # Archivos ignorados por Git
└── README.md              # Este archivo
```

## 🐛 Solución de Problemas

### Error de conexión a MongoDB

```
pymongo.errors.ServerSelectionTimeoutError
```

**Solución:** Verifica que:
1. El URI en `.env` sea correcto
2. Tu IP esté en la whitelist de MongoDB Atlas
3. Tengas conexión a internet

### Error al generar Excel

```
ModuleNotFoundError: No module named 'openpyxl'
```

**Solución:**
```bash
pip install openpyxl
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso educativo y profesional.

## ✨ Autor

Desarrollado para la gestión eficiente de inscripciones en rodeos chilenos.

---

**Nota:** Este sistema fue diseñado como herramienta práctica para la administración de eventos ecuestres, combinando la simplicidad de una interfaz de terminal con la robustez de MongoDB Atlas.