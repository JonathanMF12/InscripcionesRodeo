# Sistema de Gestión de Inscripciones de Rodeo

**Evaluación Unidad Integradora N°4 - Bases de Datos No Estructuradas**  
TI3V32 | INACAP Puente Alto | Sección 103-3A-F1

---

## Instalación Rápida

```bash
git clone https://github.com/JonathanMF12/InscripcionesRodeo
cd InscripcionesRodeo
pip install -r requirements.txt
```

Crear archivo `.env`:
```env
MONGODB_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
DB_NAME=rodeo_db
COL_NAME=inscripciones
```

Ejecutar:
```bash
python main.py
```

---

## Modelo de Datos (Cumplimiento Rúbrica)

✅ **1 Subdocumento:** `contacto`  
✅ **1 Array de subdocumentos:** `binomios`  
✅ **1 Campo fecha:** `fecha_registro`

```javascript
{
  "club_organizador": "Club El Rodeo",
  "contacto": { "nombre": "Juan", "fono": "+56912345678", "email": "s/i" },
  "criadero": "Los Aromos",
  "binomios": [
    { "jinete": "Pedro", "rut": "12345678-9", "caballo": "Relámpago", "club_origen": "Club El Rodeo" }
  ],
  "fecha_registro": ISODate("2026-05-14T..."),
  "estado": "Pendiente"
}
```

---

## Funcionalidades (9 Requisitos de Rúbrica)

### 1. CREATE - insertOne / insertMany
**Opción:** 1  
Crea una inscripción → pregunta si agregar más → usa `insertMany()` para batch

### 2. READ - Listar con proyección
**Opción:** 2 → 1  
Muestra solo: `club_organizador`, `criadero`, `fecha_registro`, `estado`

### 3. READ - Operadores de comparación
**Opción:** 2 → 2  
- `$ne`: Buscar estados distintos a "Pendiente"
- `$in`: Buscar por lista de clubes

### 4. READ - Expresión regular
**Opción:** 5  
Busca por nombre de criadero con `$regex` (case-insensitive)

### 5. READ - Rango de fechas
**Opción:** 4  
Busca con `$gte` y `$lte` (Mayo 2026)

### 6. READ - Buscar en array/subdocumento
**Opción:** 7  
Query: `{"binomios.rut": "12345678-9"}` (busca jinete por RUT)

### 7. UPDATE - Campo raíz
**Opción:** 6  
Actualiza `estado` de un club con `update_many()`

### 8. UPDATE - Campo en array
**Opción:** 7  
Actualiza `club_origen` de un jinete con operador posicional `$`

### 9. DELETE - Con condición
**Opción:** 8  
Elimina por `criadero` usando `delete_one()`

---

## Menú del Sistema

```
1. Crear          → insertOne/insertMany
2. Listar/Buscar  → find() + operadores ($ne, $in)
3. Excel          → Exportar planilla
4. Fecha          → Búsqueda por rango ($gte, $lte)
5. Regex          → Búsqueda con $regex
6. Estado         → Update campo raíz
7. Jinete         → Update en array con $
8. Eliminar       → delete_one()
0. Salir
```

---

## Puntaje Estimado

| Criterio | Pts | Estado |
|----------|-----|--------|
| Modelo de datos | 7 | ✅ |
| Create (insertOne/Many) | 7 | ✅ |
| Read básico | 5 | ✅ |
| Read avanzado | 7 | ✅ |
| Update | 5 | ✅ |
| Delete | 5 | ✅ |
| GitHub | 5 | ✅ |

**Total:** 41 pts → **Nota 5.7**

---

## Troubleshooting

**Error de conexión:** Verificar URI en `.env` y whitelist en MongoDB Atlas  
**ModuleNotFoundError:** `pip install -r requirements.txt`  
**Sin Excel:** Crear al menos una inscripción primero

---

## Demo en Vivo

**Pre-requisitos:**
- 8+ documentos en MongoDB
- `.env` configurado
- Repo GitHub público

**Secuencia sugerida:**
1. Crear (insertOne)
2. Crear múltiples (insertMany)
3. Listar con proyección
4. Buscar con $ne/$in
5. Buscar con $regex
6. Buscar por fechas
7. Update estado
8. Update jinete
9. Delete
10. Generar Excel

---

**Estudiante:** [Nombre] | **RUT:** [RUT] | **Fecha:** 15/05/2026