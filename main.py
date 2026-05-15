import pymongo
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv


# --- CONEXIÓN CLUSTER ATLAS ---
load_dotenv()
uri = os.getenv("MONGODB_URI")
client = pymongo.MongoClient(uri)
db = client[os.getenv("DB_NAME")]
coleccion = db[os.getenv("COL_NAME")]

# --- FUNCIONES ---

# === CREATE ===
def crear_documento():
    """insertOne / insertMany según cantidad de documentos"""
    print("\n--- Nueva Inscripción ---")
    
    documentos = []
    
    while True:
        while True:
            club = input("Club (Obligatorio): ").strip()
            contacto = input("Nombre Contacto (Obligatorio): ").strip()
            if club and contacto: break
            print("❌ Club y Contacto son obligatorios.")

        criadero = input("Criadero (Opcional): ").strip() or "N/A"
        fono = input("Fono: ")

        lista_binomios = []
        print("\n--- Ingrese los datos de la Collera (2 Jinetes) ---")
        for i in range(1, 3):
            print(f"\nDatos Jinete {i}:")
            jinete = {
                "jinete": input(f"Nombre Jinete {i}: "),
                "rut": input(f"RUT Jinete {i}: "),
                "caballo": input(f"Nombre Caballo {i}: "),
                "club_origen": club
            }
            lista_binomios.append(jinete)

        nueva = {
            "club_organizador": club,
            "contacto": {"nombre": contacto, "fono": fono, "email": "s/i"},
            "criadero": criadero,
            "serie": "Libre",
            "binomios": lista_binomios,
            "fecha_registro": datetime.now(),
            "estado": "Pendiente"
        }
        
        documentos.append(nueva)
        
        mas = input("\n¿Agregar otra inscripción? (s/n): ").strip().lower()
        if mas != 's':
            break
    
    if len(documentos) == 1:
        res = coleccion.insert_one(documentos[0])
        print(f"\n✅ Inscripción registrada con éxito. ID: {res.inserted_id}")
    else:
        res = coleccion.insert_many(documentos)
        print(f"\n✅ {len(res.inserted_ids)} inscripciones registradas con éxito.")
        for id in res.inserted_ids:
            print(f"   ID: {id}")

# === READ ===
def listar_y_exportar():
    """Lista con proyección de campos relevantes"""
    print("\n╔════════════════════════════════════════╗")
    print("║         LISTADO DE INSCRIPCIONES       ║")
    print("╚════════════════════════════════════════╝\n")
    
    datos = list(coleccion.find({}, {
        "_id": 0,
        "club_organizador": 1,
        "criadero": 1,
        "fecha_registro": 1,
        "estado": 1
    }))
    
    if datos:
        for doc in datos:
            f = doc['fecha_registro'].strftime('%d-%m-%Y')
            print(f"📍 {doc['club_organizador']:20} | {doc['criadero']:15} | {f} | {doc['estado']}")
        
        # Opción de generar Excel
        opcion = input("\n1. Generar Excel  2. Salir\nOpción: ").strip()
        if opcion == "1": 
            exportar_excel()
    else:
        print("❌ No hay registros disponibles.")

def buscar_avanzada_operadores():
    """Búsqueda con $ne y $in"""
    print("\n╔════════════════════════════════════════╗")
    print("║     BÚSQUEDA CON OPERADORES ($ne/$in)  ║")
    print("╚════════════════════════════════════════╝\n")
    print("1. Buscar por estado distinto ($ne)")
    print("2. Buscar por lista de clubes ($in)")
    print("0. Volver\n")
    
    op = input("Opción: ").strip()
    
    if op == "1":
        estado = input("\nEstado a excluir: ").strip()
        for doc in coleccion.find({"estado": {"$ne": estado}}):
            print(f"📍 Club: {doc['club_organizador']} | Estado: {doc['estado']}")
            
    elif op == "2":
        clubes_input = input("\nClubes separados por coma: ").strip()
        clubes = [c.strip() for c in clubes_input.split(",")]
        for doc in coleccion.find({"club_organizador": {"$in": clubes}}):
            print(f"📍 Encontrado: {doc['club_organizador']}")

def buscar_por_nombre_regex():
    """Búsqueda con expresión regular"""
    print("\n╔════════════════════════════════════════╗")
    print("║      BÚSQUEDA CON REGEX (criadero)     ║")
    print("╚════════════════════════════════════════╝\n")
    
    texto = input("Texto a buscar en Criadero: ").strip()
    for doc in coleccion.find({"criadero": {"$regex": texto, "$options": "i"}}):
        print(f"📍 Resultado: {doc['criadero']}")

def buscar_por_rango_fecha():
    """Búsqueda por rango de fechas con $gte y $lte"""
    print("\n╔════════════════════════════════════════╗")
    print("║       BÚSQUEDA POR RANGO DE FECHAS     ║")
    print("╚════════════════════════════════════════╝\n")
    
    inicio, fin = datetime(2026, 5, 1), datetime(2026, 5, 31)
    query = {"fecha_registro": {"$gte": inicio, "$lte": fin}}
    
    print(f"🔍 Buscando entre {inicio.date()} y {fin.date()}...\n")
    for doc in coleccion.find(query):
        print(f"📍 Encontrado: {doc['criadero']} ({doc['fecha_registro'].date()})")

def buscar_en_subdocumento():
    """Búsqueda dentro de subdocumento contacto (NUEVA - PARA RÚBRICA)"""
    print("\n╔════════════════════════════════════════╗")
    print("║   BÚSQUEDA EN SUBDOCUMENTO (contacto)  ║")
    print("╚════════════════════════════════════════╝\n")
    
    nombre = input("Nombre de contacto a buscar (usa $regex): ").strip()
    query = {"contacto.nombre": {"$regex": nombre, "$options": "i"}}
    if coleccion.count_documents(query) == 0:
        print("❌ No se encontraron contactos con ese nombre.")
        return
    elif coleccion.count_documents(query) != 0:
        print(f"✅ Se encontraron {coleccion.count_documents(query)} contacto(s) con ese nombre:\n")
        for doc in coleccion.find(query):
            print(f"📍 Encontrado: {doc['contacto']['nombre']} | {doc['contacto']['email']} | {doc['contacto']['fono']}")
        pass

# def buscar_en_array():
#     """Búsqueda dentro de array de binomios"""
#     print("\n╔════════════════════════════════════════╗")
#     print("║     BÚSQUEDA EN ARRAY (binomios.rut)   ║")
#     print("╚════════════════════════════════════════╝\n")
    
#     rut = input("RUT del jinete a buscar: ").strip()
#     query = {"binomios.rut": rut}
#     for doc in coleccion.find(query):
#         print(doc['binomios'])
#         print(f"📍 Encontrado: {doc['binomios'][0]['jinete']}")
#     pass

# === UPDATE ===
def actualizar_estado():
    """Actualizar estado (campo raíz) con update_many"""
    print("\n╔════════════════════════════════════════╗")
    print("║     ACTUALIZAR ESTADO (campo raíz)     ║")
    print("╚════════════════════════════════════════╝\n")
    
    club = input("Club a actualizar: ").strip()
    nuevo = input("Nuevo estado: ").strip()
    
    res = coleccion.update_many({"club_organizador": club}, {"$set": {"estado": nuevo}})
    print(f"✅ Modificados: {res.modified_count}")
    
    # TODO PARA DESTACADO: Mostrar documentos ANTES y DESPUÉS del update

def actualizar_jinete():
    """Actualizar campo dentro de array con operador posicional $"""
    print("\n╔════════════════════════════════════════╗")
    print("║  ACTUALIZAR JINETE (dentro de array)   ║")
    print("╚════════════════════════════════════════╝\n")
    
    rut = input("RUT del jinete: ").strip()
    nuevo_club = input("Nuevo club de origen: ").strip()
    
    res = coleccion.update_one({"binomios.rut": rut}, {"$set": {"binomios.$.club_origen": nuevo_club}})
    print("✅ Actualizado" if res.modified_count > 0 else "❌ No encontrado")
    
    # TODO PARA DESTACADO: Mostrar documentos ANTES y DESPUÉS del update

# === DELETE ===
def eliminar_registro():
    """Eliminar documento con condición específica"""
    print("\n╔════════════════════════════════════════╗")
    print("║         ELIMINAR INSCRIPCIÓN           ║")
    print("╚════════════════════════════════════════╝\n")
    
    criadero = input("Criadero a eliminar: ").strip()
    
    res = coleccion.delete_one({"criadero": criadero})
    print("✅ Eliminado" if res.deleted_count > 0 else "❌ No encontrado")
    
    # TODO PARA DESTACADO: Mostrar documento ANTES de eliminar + pedir confirmación

# === EXPORTAR ===
def exportar_excel():
    """Genera archivo Excel con todos los registros"""
    print("\n📊 Generando planilla Excel...")
    
    datos = list(coleccion.find())
    if datos:
        df = pd.DataFrame(datos)
        if '_id' in df.columns: 
            del df['_id']
        df.to_excel("Planilla_Oficial_Rodeo.xlsx", index=False)
        print("✅ Planilla_Oficial_Rodeo.xlsx generada exitosamente.")
    else:
        print("❌ No hay datos para exportar.")

# === MENÚS ===
def menu_busqueda():
    """Submenú de búsquedas"""
    while True:
        print("\n╔════════════════════════════════════════╗")
        print("║          MENÚ DE BÚSQUEDAS             ║")
        print("╠════════════════════════════════════════╣")
        print("║ 1. Listar todos (proyección)           ║")
        print("║ 2. Operadores comparación ($ne/$in)    ║")
        print("║ 3. Expresión regular ($regex)          ║")
        print("║ 4. Rango de fechas ($gte/$lte)         ║")
        print("║ 5. Buscar en subdocumento (contacto)   ║")
#        print("║ 6. Buscar en array (binomios)         ║")
        print("║ 0. Volver                              ║")
        print("╚════════════════════════════════════════╝\n")
        
        op = input("Opción: ").strip()
        
        if op == "1": listar_y_exportar()
        elif op == "2": buscar_avanzada_operadores()
        elif op == "3": buscar_por_nombre_regex()
        elif op == "4": buscar_por_rango_fecha()
        elif op == "5": buscar_en_subdocumento()
#        elif op == "6": buscar_en_array()
        elif op == "0": break

def menu():
    """Menú principal del sistema"""
    while True:
        print("\n╔════════════════════════════════════════╗")
        print("║   SISTEMA DE GESTIÓN DE RODEOS 🐎      ║")
        print("╠════════════════════════════════════════╣")
        print("║ 1. Crear inscripción                   ║")
        print("║ 2. Buscar/Consultar                    ║")
        print("║ 3. Actualizar estado (raíz)            ║")
        print("║ 4. Actualizar jinete (array)           ║")
        print("║ 5. Eliminar inscripción                ║")
        print("║ 6. Exportar a Excel                    ║")
        print("║ 0. Salir                               ║")
        print("╚════════════════════════════════════════╝\n")
        
        op = input("Opción: ").strip()
        
        if op == "1": crear_documento()
        elif op == "2": menu_busqueda()
        elif op == "3": actualizar_estado()
        elif op == "4": actualizar_jinete()
        elif op == "5": eliminar_registro()
        elif op == "6": exportar_excel()
        elif op == "0": 
            print("\n👋 ¡Hasta pronto!")
            break

if __name__ == "__main__":
    menu()