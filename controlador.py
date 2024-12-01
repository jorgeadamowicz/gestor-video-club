from tkinter import Tk
import vista

from modelo import crea_base_datos, crea_tabla
from modelo import alta_pelicula
from modelo import consulta_base_datos
from modelo import elimina_pelicula_de_bd
from modelo import buscar_en_bd
from modelo import verifica_catalogo_en_bd
from modelo import alquilar_pelicula
from modelo import devolver_pelicula


#crea conexion y tabla
def iniciar_sistema():
    
    con = crea_base_datos()
    crea_tabla(con)
    return con

#gestiona la llamda al modelo (alta pelicula)
def gestiona_alta_pelicula(con, titulo, genero, estado, socio, numero, devolucion):
    alta_pelicula(con, titulo, genero, estado, socio, numero, devolucion)

#gestiona la llamda al modelo (baja pelicula)
def gestiona_baja_pelicula(con, titulo):
    elimina_pelicula_de_bd(con, titulo)

#gestiona la llamda al modelo (busqueda)
def gestiona_busqueda(con, titulo, genero, estado, socio):
    rows = buscar_en_bd(con, titulo, genero, estado, socio)

    if len(rows)== 0:
        return []#lista vacia
    else:
        return rows

#consulta base de datos y envia la información para actualizar la vista
def consulta_y_actualiza(con):
   
    rows = consulta_base_datos(con)  # Consulta los datos a través del modelo
    return rows  # Devuelve los datos a la vista

#verifica si la pelicula se encuenta en el catalogo de la bd.
def gestiona_verifica_catalogo(con, titulo, genero, estado, socio, numero, devolucion):
    
    resultado = verifica_catalogo_en_bd(con, titulo, genero, estado, socio, numero, devolucion)
    return resultado

#gestiona la llamda al modelo (alquilar pelicula)
def gestiona_alquilar_pelicula(con, titulo, genero, estado, socio, numero, devolucion):
    alquilar_pelicula(con, titulo, genero, estado, socio, numero, devolucion)

#gestiona la llamda al modelo (devolver pelicula)
def gestiona_devolver_pelicula(con, titulo, genero, estado, socio, numero, devolucion):
    devolver_pelicula(con, titulo, genero, estado, socio, numero, devolucion)

# if __name__ == "__main__": #Este condicional se usa para verificar si el script se está ejecutando directamente o si está siendo importado como un módulo en otro script. Si el script se ejecuta directamente, el valor de __name__ será "__main__", y el código dentro del condicional se ejecutará.
#     ventana = Tk()
#     vista.vista_principal(ventana)# llama a la funcion que creamos en vista principal a la que le pasa por parametro la ventana.

#     ventana.mainloop()
