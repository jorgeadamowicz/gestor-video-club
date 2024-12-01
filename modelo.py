import sqlite3
from peewee import *
from functools import reduce
import operator
import re

db = SqliteDatabase("video_base_orm.db") #indica con que base de datos vamos a trabajar. Se instancia un objeto de la clase
#SqliteDatabase que me permitirá acceder a la conexion con la bd. 

class BaseModel(Model):
    class Meta:
        database = db


class Tabla(BaseModel): #Clase que va a ser mapeada por el ORM
    titulo = CharField(unique=True) #cada atributo corresponde a una columna en la BD
    genero = CharField()
    estado = CharField()
    socio = CharField()
    numero = CharField()
    devolucion = CharField()
db.connect() #conerctamos con la bd
db.create_tables([Tabla]) #creamos la tabla

## MODELO ##

##  
class BaseDeDatos:
    def __init__(self):
        pass

        
## funcion Alta Pelicula ingresa una película a la base de datos. 
    def alta_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        alta_bd = Tabla() #intancio un objeto de la clase Tabla y declaro sus atributos. 
        alta_bd.titulo = titulo
        alta_bd.genero = genero
        alta_bd.estado = "Disponible"
        alta_bd.socio = socio
        alta_bd.numero = numero
        alta_bd.devolucion = devolucion
        alta_bd.save() #graba ->  "commit" en SQL       

# ## funcion Baja Pelicula de la base de datos.
    def elimina_pelicula_de_bd(self, titulo):
        try:
            borrar_base = Tabla.get(fn.LOWER(Tabla.titulo) == titulo.lower()) #fn.LOWER -> LOWER(titulo) en SQL
            borrar_base.delete_instance()

        except Tabla.DoesNotExist:
            return None  # Opcionalmente, devuelve None para indicar que no se encontró

## funcion consulta la base de datos y retorna info para actualizar vista
    def consulta_base_datos(self):
        rows = Tabla.select()
        return rows

# ## funcion verifica si la pelicula existe en la base de datos
    def verifica_catalogo_en_bd(self, titulo, genero, estado, socio, numero, devolucion):
        try:
            verifica_base_resultado = Tabla.get(fn.LOWER(Tabla.titulo) == titulo.lower())
            return verifica_base_resultado
        
        except Tabla.DoesNotExist:
            return None
###NOTAS: 
    # LA FUNCION: debe invocar a la función de la vista para mostrar el mensaje al usuario
    ## PROBLEMAS: AttributeError: 'BaseDeDatos' object has no attribute 'mostrar_mensaje_no_encontrado'
    ## VERIFICACIÓN DE DECLARACION:
    # La funcion mostrar_mensaje_no_encontrado(titulo) se encuentra en modulo Vista linea 336 (OK)
    # SOLUCION:
    # se agregó un return None para informar al controlador que "la pelicula no existe"
    # se quitó la linea self.mostrar_mensaje_no_encontrado(titulo) del modelo.
    # se delegó al controlador invocar a la funcion "mostrar_mensaje_no_encontrado"

# ## funcion modifica registro alquiler en la base de datos
    def alquilar_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        
        actualizar_bd = Tabla.update(
            titulo = titulo,
            genero = genero,
            estado = "Alquilada", 
            socio = socio,
            numero = numero, 
            devolucion = devolucion
        ).where(fn.LOWER(Tabla.titulo) == titulo.lower())
        actualizar_bd.execute()

# ## funcion modifica registro devolucion en bd y actualiza la vista
    def devolver_pelicula(self, titulo, genero, estado, socio, numero, devolucion):

        devolucion_bd = Tabla.update(
            titulo = titulo,
            genero = genero,
            estado = "Disponible",
            socio = "",
            numero = "",
            devolucion = "").where(fn.LOWER(Tabla.titulo) == titulo.lower()) 

        devolucion_bd.execute()
        
# ## funcion busca en la base de datos
    def buscar_en_bd(self, titulo = None, genero = None, estado = None, socio = None):# se asigna el valor "None" por defecto a los argumentos en donde no se proporciona algún valor. 
        
        #se crea un lista de condiciones
        condiciones = []
        #evalúa si cada parámetro tiene un valor y lo agrega a la lista
        if titulo:
            #REFACTORING: Busqueda por palabra clave. En la busqueda no es necesario ingresar el titulo completo, tal como fue cargado al darse de alta.
            condiciones.append(fn.LOWER(Tabla.titulo).contains(titulo.lower()))
        if genero:
            condiciones.append(fn.LOWER(Tabla.genero) == genero.lower())
        if estado:
            condiciones.append(fn.LOWER(Tabla.estado) == estado.lower())
        if socio:
            condiciones.append(fn.LOWER(Tabla.socio) == socio.lower())
        
        if not condiciones:
            return[] # si no hay coniciones devuelve una lista vacia. 

        # Realiza la consulta usando "AND" entre todos los elemntos de "condiciones"
        
        consulta_bd = Tabla.select().where(reduce(operator.and_, condiciones)) 
        # devuelve una lista con los resultados
        resultado = list(consulta_bd)
        return resultado
        
    
    
