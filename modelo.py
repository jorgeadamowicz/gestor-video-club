import sqlite3
from peewee import *
from functools import reduce
import operator
import re

db = SqliteDatabase("video_base_orm.db") 
"""
Conexión a la base de datos SQLite.

Esta conexión se utiliza para interactuar con la base de datos `video_base_orm.db`.
Se crea una instancia de `SqliteDatabase` que gestiona la conexión.
"""
class BaseModel(Model):
    """
    Clase base para modelos ORM con Peewee.

    Todos los modelos de datos heredarán de esta clase para interactuar con la base de datos.
    """
    class Meta:
        database = db


class Tabla(BaseModel): 
    """
    Modelo que representa la tabla principal en la base de datos.

    Cada instancia de esta clase corresponde a un registro en la tabla `Tabla`.

    Atributos:
        titulo (CharField):
            Título único de la película.
        genero (CharField):
            Género de la película.
        estado (CharField):
            Estado actual de la película (e.g., Disponible, Alquilada).
        socio (CharField):
            Nombre o identificación del socio asociado.
        numero (CharField):
            Número único asociado al alquiler.
        devolucion (CharField):
            Fecha de devolución esperada.
    """
    titulo = CharField(unique=True) 
    genero = CharField()
    estado = CharField()
    socio = CharField()
    numero = CharField()
    devolucion = CharField()

db.connect() 
"""
Establece la conexión con la base de datos.
"""
db.create_tables([Tabla]) 
"""
Crea la tabla `Tabla` en la base de datos, si no existe.
"""


class BaseDeDatos:
    """
    Clase que gestiona las operaciones ABMC (Alta, Baja, Modificación, Consulta) en la base de datos.

    Métodos:
        alta_pelicula: 
            Registra una nueva película en la base de datos.
        elimina_pelicula_de_bd:
            Elimina una película de la base de datos.
        consulta_base_datos:
            Consulta todos los registros en la base de datos.
        verifica_catalogo_en_bd:
            Verifica si una película existe en el catálogo.
        alquilar_pelicula:
            Marca una película como alquilada en la base de datos.
        devolver_pelicula:
            Marca una película como devuelta en la base de datos.
        buscar_en_bd:
            Realiza búsquedas en la base de datos con filtros opcionales.
    """
    def __init__(self):
        """Inicializa una instancia de la clase BaseDeDatos."""
        pass

        
    def alta_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        """
        Registra una nueva película en la base de datos.

        Args:
            titulo (str): Título de la película.
            genero (str): Género de la película.
            estado (str): Estado inicial de la película (e.g., "Disponible").
            socio (str): Socio asociado al alquiler.
            numero (str): Número único asociado al alquiler.
            devolucion (str): Fecha de devolución esperada.
        """
        alta_bd = Tabla() 
        alta_bd.titulo = titulo
        alta_bd.genero = genero
        alta_bd.estado = "Disponible"
        alta_bd.socio = socio
        alta_bd.numero = numero
        alta_bd.devolucion = devolucion
        alta_bd.save()       


    def elimina_pelicula_de_bd(self, titulo):
        """
        Elimina una película de la base de datos por su título.

        Args:
            titulo (str): Título de la película a eliminar.

        Returns:
            None: Si no se encuentra la película en la base de datos.
        """
        try:
            borrar_base = Tabla.get(fn.LOWER(Tabla.titulo) == titulo.lower()) 
            borrar_base.delete_instance()

        except Tabla.DoesNotExist:
            return None 

    def consulta_base_datos(self):
        """
        Consulta todos los registros de la base de datos.

        Returns:
            list: Lista de registros en la tabla `Tabla`.
        """
        rows = Tabla.select()
        return rows

    def verifica_catalogo_en_bd(self, titulo, genero, estado, socio, numero, devolucion):
        """
        Verifica si una película existe en la base de datos.

        Args:
            titulo (str): Título de la película.
            genero (str): Género de la película.
            estado (str): Estado actual de la película.
            socio (str): Socio asociado al alquiler.
            numero (str): Número único asociado al alquiler.
            devolucion (str): Fecha de devolución esperada.

        Returns:
            Tabla: Objeto que representa la película si existe.
            None: Si no se encuentra la película.
        """
        try:
            verifica_base_resultado = Tabla.get(fn.LOWER(Tabla.titulo) == titulo.lower())
            return verifica_base_resultado
        
        except Tabla.DoesNotExist:
            return None

    def alquilar_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        """
        Actualiza el estado de una película como alquilada.

        Args:
            titulo (str): Título de la película.
            genero (str): Género de la película.
            estado (str): Estado a actualizar ("Alquilada").
            socio (str): Socio que alquiló la película.
            numero (str): Número único asociado al alquiler.
            devolucion (str): Fecha de devolución esperada.
        """
        actualizar_bd = Tabla.update(
            titulo = titulo,
            genero = genero,
            estado = "Alquilada", 
            socio = socio,
            numero = numero, 
            devolucion = devolucion
        ).where(fn.LOWER(Tabla.titulo) == titulo.lower())
        actualizar_bd.execute()

    def devolver_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        """
        Marca una película como devuelta en la base de datos.

        Args:
            titulo (str): Título de la película.
            genero (str): Género de la película.
            estado (str): Nuevo estado ("Disponible").
            socio (str): Socio asociado (se limpia al devolver).
            numero (str): Número único asociado (se limpia al devolver).
            devolucion (str): Fecha de devolución (se limpia al devolver).
        """
        devolucion_bd = Tabla.update(
            titulo = titulo,
            genero = genero,
            estado = "Disponible",
            socio = "",
            numero = "",
            devolucion = "").where(fn.LOWER(Tabla.titulo) == titulo.lower()) 

        devolucion_bd.execute()
        
    def buscar_en_bd(self, titulo = None, genero = None, estado = None, socio = None):# se asigna el valor "None" por defecto a los argumentos en donde no se proporciona algún valor. 
        """
        Realiza búsquedas en la base de datos con filtros opcionales.

        Args:
            titulo (str, optional): Título parcial o completo.
            genero (str, optional): Género de la película.
            estado (str, optional): Estado de la película.
            socio (str, optional): Socio asociado al alquiler.

        Returns:
            list: Lista de resultados que cumplen las condiciones.
            list: Lista vacía si no se especifican filtros.
        """
        
        condiciones = [] #se crea un lista de condiciones
        
        if titulo:#evalúa si cada parámetro tiene un valor y lo agrega a la lista
            condiciones.append(fn.LOWER(Tabla.titulo).contains(titulo.lower()))
        if genero:
            condiciones.append(fn.LOWER(Tabla.genero) == genero.lower())
        if estado:
            condiciones.append(fn.LOWER(Tabla.estado) == estado.lower())
        if socio:
            condiciones.append(fn.LOWER(Tabla.socio) == socio.lower())
        
        if not condiciones:
            return[] # si no hay coniciones devuelve una lista vacia. 

        consulta_bd = Tabla.select().where(reduce(operator.and_, condiciones)) 
        resultado = list(consulta_bd)
        return resultado
        
    
    
