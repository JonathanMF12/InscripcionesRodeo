import pymongo
import pandas as pd
from datetime import datetime

# --- CONEXIÓN CLUSTER ATLAS ---
uri = "mongodb+srv://jonathanmolina18_db_user:vkxfM9KQaBjp1zmy@cluster0.auwexva.mongodb.net/"
client = pymongo.MongoClient(uri)
db = client["Rodeo2026"]
coleccion = db["Inscripciones"]

# --- FUNCIONES ---

def crear_documento():
    print("\n--- Nueva Inscripción ---")
    
    while True:
        club = input("Club (Obligatorio): ").strip()
        contacto = input("Nombre Contacto (Obligatorio): ").strip()
        if club and contacto: break
        print("❌ Club y Contacto son obligatorios.")

    criadero = input("Criadero (Opcional): ").strip() or "N/A"
    fono = input("Fono: ")

    # --- REGISTRO DE LA COLLERA (ARRAY DE SUBDOCUMENTOS) ---
    lista_binomios = []
    print("\n--- Ingrese los datos de la Collera (2 Jinetes) ---")
    for i in range(1, 3):
        print(f"\nDatos Jinete {i}:")
        jinete = {
            "jinete": input(f"Nombre Jinete {i}: "),
            "rut": input(f"RUT Jinete {i}: "),
            "caballo": input(f"Nombre Caballo {i}: "),
            "club_origen": club # Por defecto el mismo club
        }
        lista_binomios.append(jinete)

    nueva = {
        "club_organizador": club,
        "contacto": {"nombre": contacto, "fono": fono, "email": "s/i"},
        "criadero": criadero,
        "serie": "Libre",
        "binomios": lista_binomios, # Aquí ya no va vacío
        "fecha_registro": datetime.now(),
        "estado": "Pendiente"
    }
    
    res = coleccion.insert_one(nueva)
    print(f"\n✅ Inscripción y Collera registradas con éxito. ID: {res.inserted_id}")

def listar_y_exportar():
    """Lista en consola y genera el Excel automáticamente"""
    print("\n--- Listado y Generación de Planilla ---")
    datos = list(coleccion.find())
    
    if datos:
        # Mostrar en consola para la rúbrica
        for doc in datos:
            f = doc['fecha_registro'].strftime('%d-%m-%Y')
            print(f"Club: {doc['club_organizador']} | Criadero: {doc['criadero']} | Fecha: {f}")
        
        # Generación automática del Excel
        df = pd.DataFrame(datos)
        if '_id' in df.columns: del df['_id']
        df.to_excel("Planilla_Oficial_Rodeo.xlsx", index=False)
        print("\n✅ Planilla_Oficial_Rodeo.xlsx actualizada automáticamente.")
    else:
        print("No hay datos disponibles.")

def buscar_por_rango_fecha():
    inicio, fin = datetime(2026, 5, 1), datetime(2026, 5, 31)
    query = {"fecha_registro": {"$gte": inicio, "$lte": fin}}
    for doc in coleccion.find(query):
        print(f"Encontrado: {doc['criadero']} ({doc['fecha_registro'].date()})")

def buscar_por_nombre_regex():
    texto = input("Texto a buscar en Criadero: ")
    for doc in coleccion.find({"criadero": {"$regex": texto, "$options": "i"}}):
        print(f"Resultado: {doc['criadero']}")

def actualizar_estado():
    club = input("Club: ")
    nuevo = input("Nuevo estado: ")
    res = coleccion.update_many({"club_organizador": club}, {"$set": {"estado": nuevo}})
    print(f"Modificados: {res.modified_count}")

def actualizar_jinete():
    rut = input("RUT jinete: ")
    nuevo_club = input("Nuevo club: ")
    res = coleccion.update_one({"binomios.rut": rut}, {"$set": {"binomios.$.club_origen": nuevo_club}})
    print("Actualizado" if res.modified_count > 0 else "No encontrado")

def eliminar_registro():
    criadero = input("Criadero a eliminar: ")
    res = coleccion.delete_one({"criadero": criadero})
    print("Eliminado" if res.deleted_count > 0 else "No encontrado")

# --- MENÚ ---

def menu():
    while True:
        print("\n1.Crear 2.Listar/Excel 3.Fecha 4.Regex 5.Estado 6.Jinete 7.Eliminar 0.Salir")
        op = input("Opción: ")
        if op == "1": crear_documento()
        elif op == "2": listar_y_exportar() # <-- Aquí hace todo solo
        elif op == "3": buscar_por_rango_fecha()
        elif op == "4": buscar_por_nombre_regex()
        elif op == "5": actualizar_estado()
        elif op == "6": actualizar_jinete()
        elif op == "7": eliminar_registro()
        elif op == "0": break

if __name__ == "__main__":
    menu()