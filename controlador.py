
"""
Módulo controlador para la aplicación de Video Club.

Este módulo define la clase `ControladorVideoClub`, que actúa como intermediario entre 
la vista y el modelo en la arquitectura MVC. Se encarga de gestionar las solicitudes 
de la vista y de interactuar con el modelo para realizar las consultas en la base de datos.

Clases:
    ControladorVideoClub: Controlador principal que gestiona la lógica de negocio.

Ejecutar como script:
    Cuando se ejecuta directamente, este módulo inicializa el modelo, el controlador y 
    la vista, y lanza la interfaz gráfica de la aplicación.
"""
from tkinter import Tk

from vista import VistaVideoClub

from modelo import BaseDeDatos

from observador import Inventario, RegistroCsv


class ControladorVideoClub:
    """
    Controlador principal que conecta la vista con el modelo en la arquitectura MVC.

    Atributos:
        modelo (BaseDeDatos): Instancia del modelo que contiene la lógica de manejo de datos.

    Métodos:
        gestiona_alta_pelicula(titulo, genero, estado, socio, numero, devolucion):
            Gestiona la solicitud de alta de una película en la base de datos.
        gestiona_baja_pelicula(titulo):
            Gestiona la solicitud de baja de una película en la base de datos.
        gestiona_busqueda(titulo, genero, estado, socio):
            Realiza una búsqueda de películas en la base de datos y devuelve los resultados.
        consulta_y_actualiza():
            Consulta todos los datos de la base de datos y los devuelve.
        gestiona_verifica_catalogo(titulo, genero, estado, socio, numero, devolucion):
            Verifica si una película se encuentra en el catálogo.
        gestiona_alquilar_pelicula(titulo, genero, estado, socio, numero, devolucion):
            Gestiona el alquiler de una película en la base de datos.
        gestiona_devolver_pelicula(titulo, genero, estado, socio, numero, devolucion):
            Gestiona la devolución de una película en la base de datos.
    """
    def __init__(self, modelo) -> None:
        """
        Inicializa el controlador con una instancia del modelo.

        Args:
            modelo (BaseDeDatos): Objeto del modelo que maneja las operaciones de la base de datos.
        """
        self.modelo = modelo 
        
    def gestiona_alta_pelicula(self,titulo, genero, estado, socio, numero, devolucion):
        """
        Gestiona la solicitud de alta de una película en la base de datos.

        Args:
            titulo (str): Título de la película.
            genero (str): Género de la película.
            estado (str): Estado de la película (disponible/alquilada).
            socio (str): Socio asociado a la película, si aplica.
            numero (int): Número único asociado al alquiler.
            devolucion (str): Fecha de devolución esperada.
        """
        self.modelo.alta_pelicula(titulo, genero, estado, socio, numero, devolucion)

    def gestiona_baja_pelicula(self, titulo):
        """
        Gestiona la solicitud de baja de una película en la base de datos.

        Args:
            titulo (str): Título de la película a eliminar.
        """
        self.modelo.elimina_pelicula_de_bd(titulo)


    def gestiona_busqueda(self, titulo, genero, estado, socio):
        """
        Realiza una búsqueda de películas en la base de datos y devuelve los resultados.

        Args:
            titulo (str): Título de la película a buscar.
            genero (str): Género de la película a buscar.
            estado (str): Estado de la película a buscar.
            socio (str): Socio asociado a la película, si aplica.

        Returns:
            list: Lista de resultados de la búsqueda. Vacía si no se encuentran coincidencias.
        """
        rows = self.modelo.buscar_en_bd(titulo, genero, estado, socio)

        if len(rows)== 0:
            return []
        else:
            return rows

    def consulta_y_actualiza(self):
        """
        Consulta todos los datos de la base de datos y los devuelve.

        Returns:
            list: Lista de todas las películas en la base de datos.
        """
        rows = self.modelo.consulta_base_datos() 
        return rows  

    def gestiona_verifica_catalogo(self, titulo,  genero, estado, socio, numero, devolucion, modo= "local"):
        """
        Verifica si una película se encuentra en el catálogo.

        Args:
            titulo (str): Título de la película.
            genero (str): Género de la película.
            estado (str): Estado de la película.
            socio (str): Socio asociado a la película.
            numero (int): Número único asociado al alquiler.
            devolucion (str): Fecha de devolución esperada.
            modo (str, opcional): Define si la consulta es local o remota. 
                              - "local": Muestra el mensaje en la vista si la película no se encuentra.
                              - "remoto": Retorna `None`, permitiendo que el servidor gestione la respuesta. 
                              El valor por defecto es "local".

        Returns:
            dict or None: Datos de la película si se encuentra, `None` en caso contrario.
            si la pelicula no se encuentra llama a vista para mostrar un mensaje al usuario.
        """
        resultado = self.modelo.verifica_catalogo_en_bd(titulo, genero, estado, socio, numero, devolucion)
        if resultado is None:
            if modo == "local":
                print(f"trabajando en modo: {modo}")
                vista.mostrar_mensaje_no_encontrado(titulo)
            else:
                return None # En modo remoto, retorna None para que el servidor gestione el mensaje
        else:
            print(f"el resultado es {resultado}")
            return resultado 

    def gestiona_alquilar_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        """
        Gestiona el alquiler de una película en la base de datos.

        Args:
            titulo (str): Título de la película.
            genero (str): Género de la película.
            estado (str): Estado de la película.
            socio (str): Socio asociado al alquiler.
            numero (int): Número único del alquiler.
            devolucion (str): Fecha de devolución esperada.
        """
        self.modelo.alquilar_pelicula(titulo, genero, estado, socio, numero, devolucion)

    def gestiona_devolver_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        """
        Gestiona la devolución de una película en la base de datos.

        Args:
            titulo (str): Título de la película.
            genero (str): Género de la película. 
            estado (str): Estado de la película. 
            socio (str): Socio asociado al alquiler. 
            numero (int): Número único del alquiler.
            devolucion (str): Fecha de devolución esperada.
        """
        self.modelo.devolver_pelicula(titulo, genero, estado, socio, numero, devolucion)

if __name__ == "__main__": 
    """
    Punto de inicio de la aplicación.

    Este bloque inicializa el modelo, el controlador y la vista, y lanza la 
    interfaz gráfica principal de la aplicación.
    """
    
    inventario = Inventario() #instanciación de la clase Inventario
    registro_csv = RegistroCsv() #instanciación de la clase RegistroCsv
    inventario.registrar_observador(registro_csv) #relaciona el inventario (sujeto) con el registro_csv(observador)
    
    ventana = Tk() #crea la ventana
    modelo = BaseDeDatos(inventario)   # Instanciación del modelo. Se crea el objeto de la clase BaseDeDatos de manera que pueda acceder a los metodos de esta clase
    application = ControladorVideoClub(modelo)  # El controlador recibe el modelo
    vista = VistaVideoClub(ventana, application) # La vista recibe la ventana y el objeto application de la clase ControladorVideoClub
    ventana.mainloop()

  

