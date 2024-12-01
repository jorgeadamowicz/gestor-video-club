from tkinter import Tk

from vista import VistaVideoClub

from modelo import BaseDeDatos
# from modelo import alta_pelicula
# from modelo import consulta_base_datos
# from modelo import elimina_pelicula_de_bd
# from modelo import buscar_en_bd
# from modelo import verifica_catalogo_en_bd
# from modelo import alquilar_pelicula
# from modelo import devolver_pelicula

# class ControladorVideoClub:
#     def __init__(self, ventana):
#         self.controlador_ventana = ventana
#         self.objeto_vista = VistaVideoClub(self.controlador_ventana, self)
#         self.modelo = BaseDeDatos
        # self.base_datos = BaseDeDatos()
        # self.vista = VistaVideoClub()

### PRUEBA PASANDO MODELO
class ControladorVideoClub:
    def __init__(self, modelo) -> None:
        self.modelo = modelo ## Modelo como atributo del controlador
        

#crea conexion y tabla
    # def iniciar_sistema(self):
    #     self.controlador_ventana.mainloop()# 4)crea el loop para que se pueda ver la ventana
    

#gestiona la llamda al modelo (alta pelicula)
    def gestiona_alta_pelicula(self,titulo, genero, estado, socio, numero, devolucion):
        self.modelo.alta_pelicula(titulo, genero, estado, socio, numero, devolucion)

#gestiona la llamda al modelo (baja pelicula)
    def gestiona_baja_pelicula(self, titulo):
        self.modelo.elimina_pelicula_de_bd(titulo)

#gestiona la llamda al modelo (busqueda)
    def gestiona_busqueda(self, titulo, genero, estado, socio):
        rows = self.modelo.buscar_en_bd(titulo, genero, estado, socio)

        if len(rows)== 0:
            return []#lista vacia
        else:
            return rows

#consulta base de datos y envia la información para actualizar la vista
    def consulta_y_actualiza(self):
    
        rows = self.modelo.consulta_base_datos()  # Consulta los datos a través del modelo
        return rows  # Devuelve los datos a la vista

    #verifica si la pelicula se encuenta en el catalogo de la bd.
    def gestiona_verifica_catalogo(self, titulo,  genero, estado, socio, numero, devolucion):
        resultado = self.modelo.verifica_catalogo_en_bd(titulo, genero, estado, socio, numero, devolucion)
        
        return resultado 

#gestiona la llamda al modelo (alquilar pelicula)
    def gestiona_alquilar_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        self.modelo.alquilar_pelicula(titulo, genero, estado, socio, numero, devolucion)

#gestiona la llamda al modelo (devolver pelicula)
    def gestiona_devolver_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        self.modelo.devolver_pelicula(titulo, genero, estado, socio, numero, devolucion)

if __name__ == "__main__": #Este condicional se usa para verificar si el script se está ejecutando directamente o si está siendo importado como un módulo en otro script. Si el script se ejecuta directamente, el valor de __name__ será "__main__", y el código dentro del condicional se ejecutará.

    # ventana = Tk() # 1) se crea la ventana
    # application = ControladorVideoClub(ventana) #2)se crea una instancia de Controlador donde se pasa (ventana) como parametro
    
    # Punto de inicio de la aplicación
    ventana = Tk() #crea la ventana
    modelo = BaseDeDatos()   # Instanciación del modelo. Se crea el objeto de la clase BaseDeDatos de manera que pueda acceder a los metodos de esta clase
    application = ControladorVideoClub(modelo)  # El controlador recibe el modelo
    vista = VistaVideoClub(ventana, application) # La vista recibe la ventana y el objeto application de la clase ControladorVideoClub
    ventana.mainloop()

    #application.iniciar_sistema()# 3) llama al metodo iniciar sistema()

#ventana.mainloop()
"""NOTAS: Explicacion: interconexion clase 4/11 1:28 hs """