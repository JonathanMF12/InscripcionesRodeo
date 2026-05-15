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

# CREAR DOCUMENTO MODIFICADO PARA CONSIDERAR INSERTMANY #
def crear_documento():
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
        
        documentos.append(nueva)
        
        mas = input("\n¿Agregar otra inscripción? (s/n): ").strip().lower()
        if mas != 's':
            break
    
    # Insertar con insertOne o insertMany según cantidad
    if len(documentos) == 1:
        res = coleccion.insert_one(documentos[0])
        print(f"\n✅ Inscripción y Collera registradas con éxito. ID: {res.inserted_id}")
    else:
        res = coleccion.insert_many(documentos)
        print(f"\n✅ {len(res.inserted_ids)} inscripciones registradas con éxito.")
        for id in res.inserted_ids:
            print(f"ID: {id}")

def exportar_excel():
    datos = list(coleccion.find())
    df = pd.DataFrame(datos)
    if '_id' in df.columns: 
        del df['_id']
        df.to_excel("Planilla_Oficial_Rodeo.xlsx", index=False)
        print("\n✅ Planilla_Oficial_Rodeo.xlsx actualizada automáticamente.")
    else:
        print("No hay datos disponibles.")

# BUSQUEDA # 
def listar_y_exportar():
    """Lista en consola y genera el Excel si es necesario."""
    print("\n--- Listado y Generación de Planilla ---")
    datos = list(coleccion.find({},{"_id": 0,"club_organizador": 1, "criadero": 1, "fecha_registro": 1, "estado": 1}))
    
    if datos:
        # Mostrar en consola para la rúbrica
        for doc in datos:
            f = doc['fecha_registro'].strftime('%d-%m-%Y')
            print(f"Club: {doc['club_organizador']} | Criadero: {doc['criadero']} | Fecha: {f} ! Estado: {doc['estado']}")
      
    # Generación opcional del Excel

    opcion = input("\n1. Generar Excel 2. Salir\n")
    if opcion == "1": 
        exportar_excel()
    elif opcion == "2":
        print("\n✅ Planilla no generada.")

def buscar_por_rango_fecha():
    inicio, fin = datetime(2026, 5, 1), datetime(2026, 5, 31)
    query = {"fecha_registro": {"$gte": inicio, "$lte": fin}}
    for doc in coleccion.find(query):
        print(f"Encontrado: {doc['criadero']} ({doc['fecha_registro'].date()})")

def buscar_por_nombre_regex():
    texto = input("Texto a buscar en Criadero: ")
    for doc in coleccion.find({"criadero": {"$regex": texto, "$options": "i"}}):
        print(f"Resultado: {doc['criadero']}")

def buscar_avanzada_operadores():
    print("\n--- Búsqueda con Operadores de Comparación ---")
    print("1. Buscar por estado distinto ($ne)")
    print("2. Buscar por lista de clubes ($in)")
    print("3. Atras\n")
    op = input("Opción: ")
    
    if op == "1":
        estado = input("Estado a excluir: ")
        for doc in coleccion.find({"estado": {"$ne": estado}}):
            print(f"Club: {doc['club_organizador']} | Estado: {doc['estado']}")
    elif op == "2":
        clubes_input = input("Clubes separados por coma: ")
        clubes = [c.strip() for c in clubes_input.split(",")]
        for doc in coleccion.find({"club_organizador": {"$in": clubes}}):
            print(f"Encontrado: {doc['club_organizador']}")      
    elif op == "3 ":
        print("\n✅ Busqueda cancelada.")          

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
        print("\n===== MENÚ PRINCIPAL =====")
        print("\n1.Crear \n2.Listar/Buscar \n3.Excel \n4.Fecha \n5.Regex \n6.Estado \n7.Jinete \n8.Eliminar \n0.Salir\n")
        print("==========================\n")
        op = input("Opción: ")

        if op == "1": crear_documento()

        elif op == "2":
            while True:
                print("\n===== MENÚ DE BUSQUEDA =====")
                print("\n1.Listar y Exportar \n2.Búsqueda Avanzada \n0.Atras\n")
                print("============================\n")
                op = input("Opción: ")
                if op == "1": 
                    listar_y_exportar()
                    break

                elif op == "2": buscar_avanzada_operadores()

                elif op == "0": 
                    break

        elif op == "3": exportar_excel()
        elif op == "4": buscar_por_rango_fecha()
        elif op == "5": buscar_por_nombre_regex()
        elif op == "6": actualizar_estado()
        elif op == "7": actualizar_jinete()
        elif op == "8": eliminar_registro()
        elif op == "0": break

if __name__ == "__main__":
    menu()