import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

BASE_DE_DATOS = "panamaslang"

# Definir MariaDB engine usando MariaDB Connector/Python
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:test123@127.0.0.1:3306/" + BASE_DE_DATOS)

Base = declarative_base()

class Diccionario(Base):
   __tablename__ = "diccionario"
   id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
   palabra = sqlalchemy.Column(sqlalchemy.String(length=100))
   significado = sqlalchemy.Column(sqlalchemy.String(length=100))
  

Base.metadata.create_all(engine)

# Crear una session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

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
            posible_significado = buscar_significado_palabra(palabra).count()
            if posible_significado > 0:       
                print(f"La palabra '{palabra}' ya existe")
            else:
                significado = input("Ingresa el significado: ")
                agregar_palabra(palabra, significado)
                print("Palabra agregada")
        if eleccion == "2":
            palabra = input("\nIngresa la palabra que quieres editar: ")
             # Comprobar si no existe
            posible_significado = buscar_significado_palabra(palabra).count()
            if posible_significado > 0:       
                nuevo_significado = input("Ingresa el nuevo significado: ")
                editar_palabra(palabra, nuevo_significado)
                print("Palabra actualizada")              
            else:
               print(f"La palabra '{palabra}' no existe")                 
        if eleccion == "3":
            palabra = input("\nIngresa la palabra a eliminar: ")
            eliminar_palabra(palabra)
        if eleccion == "4":
            palabras = obtener_palabras()           
            print("\n========Lista de palabras========\n")
            for palabra in palabras:
                # Al leer desde la base de datos se devuelven los datos como arreglo, por
                # lo que hay que imprimir el primer elemento
                print(palabra.palabra + ": " + palabra.significado)
           
        if eleccion == "5":
            palabra = input(
                "\nIngresa la palabra de la cual quieres saber el significado: ")
            significado = buscar_significado_palabra(palabra)
            if significado.count() > 0:
                print(f"El significado de '{palabra}' es:\n{significado[0].significado}")
            else:
                print(f"Palabra '{palabra}' no encontrada")


def agregar_palabra(palabra, significado):
    slang = Diccionario(palabra=palabra, significado=significado)
    session.add(slang)
    session.commit()


def editar_palabra(palabra, nuevo_significado):
    session.query(Diccionario).filter(
        Diccionario.palabra==palabra
    ).update({
        Diccionario.palabra: palabra,
        Diccionario.significado: nuevo_significado
    })   
    session.commit()


def eliminar_palabra(palabra):
    session.query(Diccionario).filter(Diccionario.palabra == palabra).delete()
    session.commit()


def obtener_palabras(): 
    return session.query(Diccionario).all() 


def buscar_significado_palabra(palabra):    
    return session.query(Diccionario).filter_by(palabra=palabra)

if __name__ == '__main__':
    principal()
