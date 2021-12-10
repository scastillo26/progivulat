import pymongo
from pymongo import MongoClient
from bson import ObjectId

BASE_DE_DATOS = "panamaslang"

# Definir el cluster con la cadena de conexion conectarse al servidor
cluster = MongoClient("mongodb://localhost:27017/")
db = cluster[BASE_DE_DATOS]
collection = db["diccionario"] 

def principal():   
    menu = """
1) Agregar nueva palabra
2) Editar palabra existente
3) Eliminar palabra existente
4) Ver listado de palabras
5) Buscar significado de palabra
6) Salir
Elige: """
    eleccion = ""
    while eleccion != "6":
        eleccion = input(menu)
        if eleccion == "1":
            palabra = input("\nIngresa palabra: ")
            # Comprobar si no existe
            posible_significado = buscar_significado_palabra(palabra)               
            if posible_significado:       
               print(f"La palabra '{palabra}' ya existe")
            else:
                significado = input("Ingresa el significado: ")
                agregar_palabra(palabra, significado)
                print("Palabra agregada")
        if eleccion == "2":
            palabra = input("\nIngresa la palabra que quieres editar: ")
             # Comprobar si no existe
            posible_significado =  buscar_significado_palabra(palabra)
            if posible_significado:       
                nuevo_significado = input("Ingresa el nuevo significado: ")
                editar_palabra(posible_significado["palabra"], nuevo_significado)
                print("Palabra actualizada")              
            else:
               print(f"La palabra '{palabra}' no existe")                 
        if eleccion == "3":
            palabra = input("\nIngresa la palabra a eliminar: ")
             # Comprobar si no existe
            posible_significado =  buscar_significado_palabra(palabra)
            if posible_significado:       
                eliminar_palabra(palabra)
                print("Palabra eliminada")              
            else:
               print(f"La palabra '{palabra}' no existe")    
            
        if eleccion == "4":
            palabras = obtener_palabras()           
            print("\n========Lista de palabras========\n")
            for palabra in palabras:
                # Al leer desde la base de datos se devuelven los datos como arreglo, por
                # lo que hay que imprimir el primer elemento
                print(palabra["palabra"] + ": " + palabra["significado"])
           
        if eleccion == "5":
            palabra = input(
                "\nIngresa la palabra de la cual quieres saber el significado: ")
            posible_significado = buscar_significado_palabra(palabra)
            if posible_significado:
                significado = posible_significado["significado"]
                print(f"El significado de '{palabra}' es:\n{significado}")
            else:
                print(f"Palabra '{palabra}' no encontrada")


def agregar_palabra(palabra, significado):
    post = {"palabra" : palabra, "significado": significado}
    collection.insert_one(post)


def editar_palabra(palabra, nuevo_significado):    
    collection.update_one({"palabra": palabra}, {"$set":{"significado": nuevo_significado}})


def eliminar_palabra(palabra):
    collection.delete_one({"palabra" : palabra})


def obtener_palabras(): 
    return collection.find({})


def buscar_significado_palabra(palabra):      
    document = ""

    for model in collection.find({}):       
        if model["palabra"] == palabra:
            document = model           
            break
             
    return document

   
if __name__ == '__main__':
    principal()
