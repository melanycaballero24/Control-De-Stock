# Permite transformar listas/diccionarios de Python a formato de texto JSON 
import json
# Da acceso a funciones del sistema operativo (lo usamos para ver si el archivo .json ya existe)
import os

#Esto define el nombre del archivo donde se guardarán los datos de forma permanente
ARCHIVO = "productos.json"

def cargar_productos():
    #Si el archivo físico no existe,evita un error de lectura
    if not os.path.exists(ARCHIVO):
        return []
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:  # Si el archivo está vacío
                return []
            #Covierte la cadena de texto JSON en una lista de diccionarios de Python
            return json.loads(contenido)
    except Exception as e:
        print(f"Error al cargar: {e}")
        return []

def guardar_productos(productos):
    #Recibe la lista de productos actualizada de la memoria 
    # y la escribe en el JSON para asegurar la persistencia de los datos 
    try:
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(productos, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar: {e}")