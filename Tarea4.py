import redis

# Se establese la conexión de redis en la base de datos 0
# redis://localhost:6379
collection = redis.Redis(host='localhost', port=6379, db=0)
hashName = "diccionario"

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
            posible_significado = collection.hexists(hashName, palabra)         
            if posible_significado:       
                print(f"La palabra '{palabra}' ya existe")
            else:
                significado = input("Ingresa el significado: ")
                agregar_palabra(palabra, significado)
                print("Palabra agregada")
        if eleccion == "2":
            palabra = input("\nIngresa la palabra que quieres editar: ")
             # Comprobar si no existe
            posible_significado = collection.hexists(hashName, palabra)
            if posible_significado:       
                nuevo_significado = input("Ingresa el nuevo significado: ")
                editar_palabra(palabra, nuevo_significado)
                print("Palabra actualizada")              
            else:
               print(f"La palabra '{palabra}' no existe")                 
        if eleccion == "3":
            palabra = input("\nIngresa la palabra a eliminar: ")
             # Comprobar si no existe
            posible_significado = collection.hexists(hashName, palabra)
            if posible_significado:       
                eliminar_palabra(palabra)
                print("Palabra eliminada")              
            else:
               print(f"La palabra '{palabra}' no existe")    
            
        if eleccion == "4":
            palabras = obtener_palabras()           
            print("\n========Lista de palabras========\n")
            for palabra in palabras:
                print(palabra.decode())                
           
        if eleccion == "5":
            palabra = input(
                "\nIngresa la palabra de la cual quieres saber el significado: ")
            posible_significado = collection.hexists(hashName, palabra)
            if posible_significado:
                significado = buscar_significado_palabra(palabra)
                print(f"El significado de '{palabra}' es:\n{significado.decode()}")
            else:
                print(f"Palabra '{palabra}' no encontrada")


def agregar_palabra(palabra, significado):  
    collection.hset(hashName, palabra, significado)


def editar_palabra(palabra, nuevo_significado):    
    collection.hset(hashName, palabra, nuevo_significado)


def eliminar_palabra(palabra):
    collection.hdel(hashName, palabra)


def obtener_palabras(): 
    return collection.hgetall(hashName)


def buscar_significado_palabra(palabra):                 
    return collection.hget(hashName, palabra)

   
if __name__ == '__main__':
    principal()
