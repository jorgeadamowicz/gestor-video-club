
### importar bibliotecas ##

from tkinter import*
from tkinter.messagebox import *
import sqlite3 
from tkinter import ttk
from tkcalendar import Calendar
import re

## ventana principal Interface Grafica ## 

ventana = Tk()
ventana.title("Videoclub")
ventana.geometry("1000x650")
ventana.iconbitmap("icono.ico")
ventana.configure(bg= "AntiqueWhite1")

## declaración variables Tk

var_titulo = StringVar() #nombre
var_genero = StringVar() #genero
var_estado = StringVar() #estado
var_socio = StringVar() #nombre socio
var_num_socio = StringVar() #numero socio
var_devolucion = StringVar() #fecha con tkcalendar

## funcion crea base de datos sqlite ##

def crea_base_datos():
    con = sqlite3.connect("video_base.db")
    return con

## funcion crea tabla sqlite ##

def crea_tabla(con):
    cursor = con.cursor()
    sql = "CREATE TABLE IF NOT EXISTS video_base (id INTEGER PRIMARY KEY AUTOINCREMENT, Titulo TEXT, Genero TEXT, Estado TEXT, Socio TEXT, Numero TEXT, Devolucion TEXT)"
    cursor.execute(sql)
    con.commit()

con = crea_base_datos()
crea_tabla(con)

## LabelFrame datapicker ##
lf_datapicker = LabelFrame(ventana, text="Fecha Devolución",padx=10, pady=10)
lf_datapicker.grid(row=0, column=2, padx=20, pady=20)

## funcion datapicker ##
def obtener_fecha():
    fecha_seleccionada = calendario.get_date()
    var_devolucion.set(fecha_seleccionada) 

calendario = Calendar(lf_datapicker, date_pattern="dd/mm/yyyy")
calendario.grid(row= 0, column= 0, pady=20)


## Metodo ##

## funcion getter recupera valores de campos entry y los envía por parametro

def recuperar_enviar_valores(): 
    el_titulo = var_titulo.get()
    el_genero = var_genero.get()
    el_estado = var_estado.get()
    el_socio = var_socio.get()
    el_numero = var_num_socio.get()
    la_devolucion = var_devolucion.get() 

    alta_pelicula(con, el_titulo, el_genero, el_estado, el_socio, el_numero, la_devolucion)
    limpiar_campos()

## funcion verifica si la pelicula existe en catalogo

def verifica_existe_en_bd(con, titulo, genero, estado, socio, numero, devolucion):
    cursor= con.cursor()
    data= (titulo,)
    sql= "SELECT * FROM video_base WHERE LOWER(Titulo) = LOWER(?)" 
    cursor.execute(sql,data)
    resultado = cursor.fetchone()
    
    if resultado:
        #print(" resultado de la consulta", resultado)
        estado_disponibilidad = resultado[3]
        if estado_disponibilidad == "Disponible":
            alquilar_pelicula(con, titulo, genero, estado, socio, numero, devolucion)
            limpiar_campos()
        else:
            showwarning("Atencion", "Película No disponible en este momento!")
            limpiar_campos()
    else: 
        showinfo("INFO", "La película no se encuentra en catálogo!")


## funcion modifica registro alquiler en bd y actualiza la vista

def alquilar_pelicula(con, titulo, genero, estado, socio, numero, devolucion):
    # valida que el campo "socio" no se encuentre vacío al realizar el alquiler.
    patron = r"\S"
    if not re.match(patron,socio):
        showerror("ERROR", "El campo socio debe ser completado.")
        return 
    
    cursor= con.cursor()
    estado = "Alquilada"
    data= (genero, estado, socio, numero, devolucion, titulo)
    sql= "UPDATE video_base SET  genero = ?, estado = ?, socio = ?, numero = ?, devolucion = ?  WHERE LOWER(titulo) =LOWER(?)"
    cursor.execute(sql,data)
    con.commit()
    showinfo("INFO", "Pelicula Alquilada con exito.")
    actualizar_el_treeview(con) # llama a la funcion que envia los datos a la vista

## funcion que inserta los valores en el treeview

def actualizar_el_treeview(con):
    #limpiar el treeview
    for item in tree.get_children(): 
        tree.delete(item)

    #consulta la base de datos sqlite
    cursor = con.cursor()
    sql = "SELECT * FROM video_base"
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    #insertar los registros en el treeview
    for row in rows:
        tree.insert("", END, values=row)

## funcion modifica registro devolucion en bd y actualiza la vista

def devolucion_pelicula(con, titulo, genero, estado, socio, numero, devolucion):
    cursor= con.cursor()
    estado = "Disponible"
    socio = ""
    numero = ""
    devolucion = ""
    sql= "UPDATE video_base SET  estado = ?, socio = ?, numero = ?, devolucion = ?  WHERE LOWER(titulo) =LOWER(?)"
    data= (estado, socio, numero, devolucion, titulo)
    cursor.execute(sql,data)
    con.commit()
    showinfo("INFO", "Devolución exitosa")
    actualizar_el_treeview(con) # llama a la funcion que envia los datos a la vista
    limpiar_campos()

## funcion Alta Pelicula ingresa una película al catálogo

def alta_pelicula(con, titulo, genero, estado, socio, numero, devolucion):
    cursor= con.cursor()
    estado = "Disponible"
    data= (titulo, genero, estado, socio, numero, devolucion)
    sql= "INSERT INTO video_base (titulo, genero, estado, socio, numero, devolucion) VALUES (?,?,?,?,?,?)"
    cursor.execute(sql,data)
    con.commit()
    showinfo("INFO", "Pelicula ingresada al catálogo con exito.")
    actualizar_el_treeview(con) # llama a la funcion que envia los datos a la vista

## funcion Baja Pelicula del catálogo, borra registro.

def baja_pelicula(con, titulo):
    cursor= con.cursor()
    respuesta = askquestion("Confimación", "Está seguro que quiere borrar la película del catálogo?")
    if respuesta == "yes":
        sql= "DELETE FROM video_base WHERE LOWER(titulo) = LOWER(?)"
        data= (titulo,)
        cursor.execute(sql,data)
        con.commit()
        showinfo("INFO", "Pelicula retirada del catalog con exito.")
        actualizar_el_treeview(con)
        limpiar_campos()
    else:
        showinfo("INFO", "Operación cancelada!" )
        limpiar_campos()

## funcion buscar

def buscar(con, titulo, genero, estado, socio):
    cursor= con.cursor()
    #completa los campos vacios con un valor predeterminado. Nota: reemplaza busqueda dinámica SQL 
    if titulo == "":
        titulo = "none"
    if genero == "":
        genero = "none"
    if estado == "":
        estado = "none"
    if socio == "":
        socio = "none"

    sql = """SELECT *
        FROM video_base
        WHERE LOWER(titulo) = LOWER(?)
          OR  LOWER(genero) = LOWER(?)
          OR LOWER(estado) = LOWER(?)
          OR LOWER(socio) = LOWER(?)"""
    
    data= (titulo,genero, estado, socio)
    cursor.execute(sql,data)
    rows = cursor.fetchall()

    if len(rows)== 0:
        showinfo("INFO", "No se encontraron resultados.")

    else:        
        #limpiar el treeview
        for item in tree.get_children():
            tree.delete(item)

        #Muestra los registros encontrados
        for row in rows:
            tree.insert("", END, values=row)

## funcion limpiar campos

def limpiar_campos():
    var_titulo.set("")
    var_genero.set("")
    var_estado.set("")
    var_socio.set("")
    var_num_socio.set("")
    var_devolucion.set("")

## funcion salir de la aplicacion
def salir_app():
    respuesta = askquestion("Confimación", "Está seguro que quiere salir de la aplicación?")
    if respuesta == "yes":
        ventana.quit()
    else:
        showinfo("INFO", "Operación cancelada!" )
 

## Vista ## Treeview ##  

lf_treeview = LabelFrame(ventana, text="Resultados", padx=20, pady=20)
lf_treeview.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

tree = ttk.Treeview(lf_treeview, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"), show= "headings")

tree.column("col1", width=70, minwidth=30, anchor=CENTER)
tree.column("col2", width=135, minwidth=80, anchor=CENTER)
tree.column("col3", width=135, minwidth=80, anchor=CENTER)
tree.column("col4", width=135, minwidth=80, anchor=CENTER)
tree.column("col5", width=135, minwidth=80, anchor=CENTER)
tree.column("col6", width=135, minwidth=80, anchor=CENTER)
tree.column("col7", width=135, minwidth=80, anchor=CENTER)

tree.heading("col1", text="Id")
tree.heading("col2", text="Titulo")
tree.heading("col3", text="Genero")
tree.heading("col4", text="Estado")
tree.heading("col5", text="Socio")
tree.heading("col6", text="Número")
tree.heading("col7", text="Devolución")

tree.grid(row=0, column=0, sticky="nsew")

# Añadir un scrollbar al Treeview
scrollbar = ttk.Scrollbar(lf_treeview, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

# labelFrame busqueda

lf_busqueda = LabelFrame(ventana, text="Busqueda", padx=10, pady=10)
lf_busqueda.grid(row=0, column=0, columnspan=1, padx=10, pady=20)

# campo de Entrada de datos

Label(lf_busqueda, text="Buscar por Titulo").grid(row=0, column=0,pady=10, sticky=W)
Entry(lf_busqueda, textvariable= var_titulo).grid(row=0, column=1)
Label(lf_busqueda, text="Busqueda por Genero").grid(row=1, column=0, pady=10, sticky=W)
Entry(lf_busqueda, textvariable= var_genero).grid(row=1, column=1)
Label(lf_busqueda, text="Busqueda por Estado").grid(row=2, column=0, pady=10, sticky=W)
Entry(lf_busqueda, textvariable=var_estado).grid(row=2, column=1)
Label(lf_busqueda, text="Busqueda por Socio").grid(row=3, column=0, pady=10, sticky=W)
Entry(lf_busqueda, textvariable= var_socio).grid(row=3, column=1)

# boton busqueda

Button(lf_busqueda, text="Buscar", command= lambda: buscar(con,var_titulo.get(), var_genero.get(), var_estado.get(), var_socio.get())).grid(row=4, column=1, padx=10, pady=10,sticky=NSEW) 
Button(lf_busqueda, text="Nueva busqueda", command= limpiar_campos).grid(row=4, column=0,padx=10, pady=10,sticky=NSEW )

# labelFrame gestion_peliculas

lf_gestion_peliculas = LabelFrame(ventana, text="Gestión Películas",padx=10, pady=10)
lf_gestion_peliculas.grid(row=0, column=1, padx=20, pady=20)

# campo de Entrada de datos

Label(lf_gestion_peliculas, text="Titulo").grid(row=0, column=0, sticky=W)
Entry(lf_gestion_peliculas, textvariable= var_titulo).grid(row=0, column=1)
Label(lf_gestion_peliculas, text="Genero").grid(row=1, column=0, sticky=W)
Entry(lf_gestion_peliculas, textvariable= var_genero).grid(row=1, column=1)
Label(lf_gestion_peliculas, text="Socio").grid(row=2, column=0, sticky=W)
Entry(lf_gestion_peliculas, textvariable= var_socio). grid(row=2, column=1)
Label(lf_gestion_peliculas, text="N° Socio").grid(row=3, column=0, pady=10, sticky=W)
Entry(lf_gestion_peliculas, textvariable= var_num_socio).grid(row=3, column=1)
Label(lf_gestion_peliculas, text="Fecha Dev.").grid(row=4, column=0,pady=10, sticky=W)
Entry(lf_gestion_peliculas, textvariable= var_devolucion).grid(row=4, column=1)

# botones gestion peliculas # NOTA: Falta retocar diseño. eje color rojo para baja.

Button(lf_gestion_peliculas, text="Alquilar", width=12, command= lambda: verifica_existe_en_bd(con, var_titulo.get(), var_genero.get(), var_estado.get(), var_socio.get(), var_num_socio.get(), var_devolucion.get())).grid(row=0, column=2, padx=10, pady=10,sticky=W)
Button(lf_gestion_peliculas, text="Devolución", width=12, command= lambda: devolucion_pelicula(con, var_titulo.get(), var_genero.get(), var_estado.get(), var_socio.get(), var_num_socio.get(), var_devolucion.get())).grid(row=1, column=2, padx=10, pady=10,sticky=W)
Button(lf_gestion_peliculas, text="Alta Pelicula", width=12, command=recuperar_enviar_valores).grid(row=2, column=2, padx=10, pady=10,sticky=W)
Button(lf_gestion_peliculas, text="Baja Pelicula", width=12, command= lambda: baja_pelicula(con, var_titulo.get())).grid(row=3, column=2, padx=10, pady=10,sticky=W)
Button(lf_gestion_peliculas, text="Obtener Fecha", width=12, command=obtener_fecha).grid(row=4, column=2, padx=10, pady=10,sticky=W)

## menu de inicio

menubar = Menu(ventana)

menu_archivo = Menu(menubar, tearoff=0)
menu_archivo.add_command(label="Mostrar base", command= lambda: actualizar_el_treeview(con))
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command= lambda: salir_app())#invoca a funcion salir.
menubar.add_cascade(label="Archivo", menu=menu_archivo)

ventana.config(menu=menubar)

## funcion cargar datos desde la vista

def carga_datos_desde_tree(event):
    valor = tree.focus() #obtiene el id de la linea seleccionada
    valores = tree.item(valor, "values") #recupera los valores y los asigna a la variable "valores"
    #print(item)
    #asigna los valores de la fila a los campos Entry a traves del metodo "setter"
    var_titulo.set(valores[1])
    var_genero.set(valores[2])
    var_estado.set(valores[3])
    var_socio.set(valores[4])
    var_num_socio.set(valores[5])
    var_devolucion.set(valores[6])

tree.bind("<Double-1>", carga_datos_desde_tree)# evento vinculado a la vista utilizando el método bind

ventana.mainloop()