"""
Módulo para implementar el patrón observador en la gestión de inventario del Video Club.

Este módulo define las clases y métodos necesarios para implementar el patrón observador, 
permitiendo registrar eventos en un archivo CSV cada vez que se realiza un cambio en el 
inventario de películas. 

Clases:
    - `Sujeto`: Clase base que permite registrar y notificar observadores.
    - `Observador`: Clase abstracta para definir la interfaz de los observadores.
    - `Observador`: Observador concreto que registra eventos en un archivo CSV.
    - `Inventario`: Sujeto concreto que gestiona una lista de películas y notifica los cambios a los observadores.

Funciones:
    registrar_evento(tipo_evento, pelicula): Registra un evento en un archivo CSV.

Patrón observador:
    - `Sujeto`: Notifica cambios en su estado a todos los observadores registrados.
    - `Observador`: Recibe notificaciones y actúa en consecuencia.
    - `RegistroCsv`: Implementa la interfaz `Observador` y registra eventos en un archivo CSV.
"""
from datetime import datetime
from os.path import exists
import csv

#metodo para registrar evento en archivo csv
def registrar_evento(tipo_evento, pelicula): #aca debo agregar el nombre de la pelicula
    """
    Registra un evento en un archivo CSV.

    Este método crea o actualiza un archivo llamado `log_peliculas.csv` para registrar 
    eventos relacionados con el inventario de películas, como altas o bajas.

    Args:
        tipo_evento (str): Tipo de evento a registrar (por ejemplo, "Alta Pelicula").
        pelicula (str): Nombre de la película relacionada con el evento.

    Crea:
        Un archivo CSV con las columnas "Fecha", "Tipo de Evento" y "Pelicula" si no existe.
    """
    fecha_actual = datetime.now()
    fecha_actual = fecha_actual.strftime("%d-%m-%Y %H:%M:%S")
    archivo_nuevo = not exists("log_peliculas.csv")  # Verifica si el archivo existe
    with open("log_peliculas.csv", "a", newline= "") as archivo_csv:
        escritor = csv.writer(archivo_csv)
        if archivo_nuevo:  # Si es un archivo nuevo, agrega encabezado
            escritor.writerow(["Fecha", "Tipo de Evento", "Pelicula"])
        escritor.writerow([fecha_actual, tipo_evento, pelicula])

#defino el patron observador

class Sujeto:
    """
    Clase base que implementa el comportamiento de un sujeto en el patrón observador.

    Permite registrar observadores y notificarles cuando ocurre un cambio en el estado 
    del sujeto.

    Atributos:
        _observadores (list): Lista de observadores registrados.

    Métodos:
        registrar_observador(observador):
            Agrega un observador a la lista de observadores.
        notificar_observadores(tipo_evento, pelicula):
            Notifica a todos los observadores sobre un evento.
    """
    def __init__(self):
        self._observadores = []
        
    #metodo regitrar observador. agrega un observador a la lista de observadores
    def registrar_observador(self, observador):
        """
        Registra un observador en la lista de observadores.

        Args:
            observador (Observador): Instancia de una clase que implementa la interfaz Observador.
        """
        self._observadores.append(observador)
        
    #metodo notificar observadores. recorre la lista de observadores y notifica a cada uno
    def notificar_observadores(self, tipo_evento, pelicula):
        """
        Notifica a todos los observadores registrados sobre un evento.

        Args:
            tipo_evento (str): Tipo de evento que ocurrió (por ejemplo, "Alta Pelicula").
            pelicula (str): Nombre de la película relacionada con el evento.
        """
        for observador in self._observadores:
            observador.actualizar(tipo_evento, pelicula) 
            
#defino la clase observador con un metodo actualizar
class Observador:
    """
    Clase abstracta que define la interfaz para los observadores en el patrón observador.

    Métodos:
        actualizar(tipo_evento, pelicula):
            Método abstracto que debe ser implementado por las subclases.
    """
    def actualizar(self, tipo_evento, pelicula):
        raise NotImplementedError("Metodo actualizar debe ser implementado en la subclase")
    
# defino la clase observador concreto. será el encargado de registrar el evento en un archivo csv
class RegistroCsv(Observador):
    """
    Observador concreto que registra eventos relacionados con el inventario de películas 
    en un archivo CSV.

    Métodos:
        actualizar(tipo_evento, pelicula):
            Registra un evento llamando a la función `registrar_evento`.
    """
    def actualizar(self, tipo_evento, pelicula):
        registrar_evento(tipo_evento, pelicula) #llama a registrar_evento que hereda de Observador para registrar el evento en un archivo csv

#clase sujeto concreto        
class Inventario(Sujeto):
    """
    Sujeto concreto que gestiona una lista de películas y notifica a los observadores sobre 
    cambios en el inventario.

    Atributos:
        peliculas (list): Lista de películas en el inventario.

    Métodos:
        agregar_pelicula(pelicula):
            Agrega una película al inventario y notifica a los observadores.
        eliminar_pelicula(pelicula):
            Elimina una película del inventario y notifica a los observadores.
    """
    def __init__(self):
        super().__init__()
        self.peliculas = []
        
    #cuando se agregúe una película se notificará al observador del evento
    def agregar_pelicula(self, pelicula):
        """
        Agrega una película al inventario y notifica a los observadores.

        Args:
            pelicula (str): Nombre de la película a agregar.
        """
        self.peliculas.append(pelicula)
        self.notificar_observadores("Alta Pelicula", pelicula)
        
    #cuando se elimine una película se notificará al observador del evento
    def eliminar_pelicula(self, pelicula):
        """
        Elimina una película del inventario y notifica a los observadores.

        Args:
            pelicula (str): Nombre de la película a eliminar.
        """
        if pelicula in self.peliculas:
            self.peliculas.remove(pelicula)
            self.notificar_observadores("Baja Pelicula", pelicula)