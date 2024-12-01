from tkinter import Tk, StringVar, LabelFrame, ttk
from tkinter import Label, Entry, Button, Menu
from tkinter import CENTER, W, NSEW

from tkinter.messagebox import askquestion, showerror, showinfo, showwarning
from tkcalendar import Calendar

import re

from controlador import iniciar_sistema
from controlador import gestiona_alta_pelicula
from controlador import consulta_y_actualiza
from controlador import gestiona_baja_pelicula
from controlador import gestiona_busqueda
from controlador import gestiona_verifica_catalogo
from controlador import gestiona_alquilar_pelicula
from controlador import gestiona_devolver_pelicula

con = iniciar_sistema()

## VISTA ##

## ventana principal Interface Grafica ## 

def vista_principal(ventana):
    ventana.title("Videoclub")
    ventana.geometry("1000x650")
    #ventana.iconbitmap("icono.ico") #VER MAS TARDE! (NO ENCUENTRA EL ARCHIVO)
    ventana.configure(bg= "AntiqueWhite1")

    ## declaración variables Tk
    var_titulo = StringVar() #nombre
    var_genero = StringVar() #genero
    var_estado = StringVar() #estado
    var_socio = StringVar() #nombre socio
    var_num_socio = StringVar() #numero socio
    var_devolucion = StringVar() #fecha con tkcalendar

    ## LabelFrame datapicker ##
    lf_datapicker = LabelFrame(ventana, text ="Fecha Devolución", padx = 10, pady = 10)
    lf_datapicker.grid(row=0, column=2, padx=20, pady=20)

    ## funcion datapicker ##
    def obtener_fecha():
        fecha_seleccionada = calendario.get_date()
        var_devolucion.set(fecha_seleccionada) 

    calendario = Calendar(lf_datapicker, date_pattern = "dd/mm/yyyy")
    calendario.grid(row = 0, column = 0, pady = 20)

    
    ## funcion verifica si la pelicula esta en catalogo 
    def verificar_y_alquilar(con, titulo, genero, estado, socio, numero, devolucion):
        
        resultado = gestiona_verifica_catalogo(con, titulo, genero, estado, socio, numero, devolucion)
        print(resultado)
        print(type(resultado))
        gestionar_resultado_existe_catalogo(con, resultado, titulo, genero, estado, socio, numero, devolucion)

    ## funcion maneja el resultado de la verificación de existencia de una película en la base de datos.
    def gestionar_resultado_existe_catalogo(con, resultado, titulo, genero, estado, socio, numero, devolucion):
        
        if resultado:
            
            estado_disponibilidad = resultado[3]
            if estado_disponibilidad == "Disponible":
                alquila_pelicula(con, titulo, genero, estado, socio, numero, devolucion)
                limpiar_campos()
            else:
                showwarning("Atencion", "Película No disponible en este momento!")
                limpiar_campos()
        else: 
            showinfo("INFO", "La película no se encuentra en catálogo!")

    ## funcion alquila pelicula.
    def alquila_pelicula(con, titulo, genero, estado, socio, numero, devolucion):
    # valida que el campo "socio" no se encuentre vacío al realizar el alquiler.
        patron = r"\S"
        if not re.match(patron,socio):
            showerror("ERROR", "El campo socio debe ser completado.")
            return 

        gestiona_alquilar_pelicula(con, titulo, genero, estado, socio, numero, devolucion)
        showinfo("INFO", "Pelicula Alquilada con exito.")
        actualizar_el_treeview(con) 

    ## funcion devuelve pelicula.
    def devuelve_pelicula(con, titulo, genero, estado, socio, numero, devolucion):

        gestiona_devolver_pelicula(con, titulo, genero, estado, socio, numero, devolucion)
        showinfo("INFO", "Devolución exitosa")
        actualizar_el_treeview(con) # llama a la funcion que envia los datos a la vista
        limpiar_campos()


    ## funcion getter recupera valores de campos entry y realiza el alta.
    def recuperar_enviar_valores(): 

        el_titulo = var_titulo.get()
        el_genero = var_genero.get()
        el_estado = var_estado.get()
        el_socio = var_socio.get()
        el_numero = var_num_socio.get()
        la_devolucion = var_devolucion.get() 

        gestiona_alta_pelicula(con, el_titulo, el_genero, el_estado, el_socio, el_numero, la_devolucion)
        showinfo("INFO", "Pelicula ingresada al catálogo con exito.")
        limpiar_campos()
        actualizar_el_treeview(con) # llama a la funcion que envia los datos a la vista

    ## funcion Baja Pelicula borra registro.
    def baja_pelicula(con, titulo):
        
        respuesta = askquestion("Confimación", "Está seguro que quiere borrar la película del catálogo?")
        if respuesta == "yes":
            gestiona_baja_pelicula(con, titulo)
            showinfo("INFO", "Pelicula retirada del catalog con exito.")
            actualizar_el_treeview(con)
            limpiar_campos()
        else:
            showinfo("INFO", "Operación cancelada!" )
            limpiar_campos()

    ## funcion buscar
    def buscar(con, titulo, genero, estado, socio):

        rows = gestiona_busqueda(con, titulo, genero, estado, socio)
        if not rows: #verifica si la lista está vacia. 
            showinfo("INFO", "No se encontraron resultados.")

        else:        
            #limpiar el treeview
            for item in tree.get_children():
                tree.delete(item)

            #Muestra los registros encontrados
            for row in rows:
                tree.insert("", "end", values=row)

    ## funcion que inserta los valores en el treeview. 

    def actualizar_el_treeview(con):
        
        for item in tree.get_children(): 
            tree.delete(item)   
        
        rows = consulta_y_actualiza(con) #consulta la base de datos sqlite a traves del controlador
        
        #insertar los registros en el treeview
        for row in rows:
            tree.insert("", "end", values=row)

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
    lf_treeview = LabelFrame(ventana, text="Resultados", padx = 20, pady = 20)
    lf_treeview.grid(row = 1, column = 0, columnspan = 3, padx = 20, pady = 20, sticky = "nsew")

    tree = ttk.Treeview(lf_treeview, columns = ("col1", "col2", "col3", "col4", "col5", "col6", "col7"), show = "headings")

    tree.column("col1", width=70, minwidth = 30, anchor = CENTER)
    tree.column("col2", width=135, minwidth = 80, anchor = CENTER)
    tree.column("col3", width=135, minwidth = 80, anchor = CENTER)
    tree.column("col4", width=135, minwidth = 80, anchor = CENTER)
    tree.column("col5", width=135, minwidth = 80, anchor = CENTER)
    tree.column("col6", width=135, minwidth = 80, anchor = CENTER)
    tree.column("col7", width=135, minwidth = 80, anchor = CENTER)

    tree.heading("col1", text = "Id")
    tree.heading("col2", text = "Titulo")
    tree.heading("col3", text = "Genero")
    tree.heading("col4", text = "Estado")
    tree.heading("col5", text = "Socio")
    tree.heading("col6", text = "Número")
    tree.heading("col7", text = "Devolución")

    tree.grid(row = 0, column = 0, sticky = "nsew")

    # Añadir un scrollbar al Treeview  
    scrollbar = ttk.Scrollbar(lf_treeview, orient = "vertical", command = tree.yview)
    tree.configure(yscroll = scrollbar.set)
    scrollbar.grid(row = 0, column = 1, sticky = 'ns')

    # labelFrame busqueda
    lf_busqueda = LabelFrame(ventana, text = "Busqueda", padx = 10, pady = 10)
    lf_busqueda.grid(row=0, column=0, columnspan=1, padx=10, pady=20)

    # campo de Entrada de datos busqueda
    Label(lf_busqueda, text = "Buscar por Titulo").grid(row = 0, column = 0, pady = 10, sticky = W)
    Entry(lf_busqueda, textvariable = var_titulo).grid(row = 0, column = 1)
    Label(lf_busqueda, text = "Busqueda por Genero").grid(row = 1, column = 0, pady = 10, sticky = W)
    Entry(lf_busqueda, textvariable= var_genero).grid(row=1, column=1)
    Label(lf_busqueda, text = "Busqueda por Estado").grid(row = 2, column = 0, pady = 10, sticky = W)
    Entry(lf_busqueda, textvariable=var_estado).grid(row=2, column=1)
    Label(lf_busqueda, text = "Busqueda por Socio").grid(row = 3, column = 0, pady = 10, sticky = W)
    Entry(lf_busqueda, textvariable = var_socio).grid(row = 3, column = 1)

    # boton busqueda
    Button(lf_busqueda, text = "Buscar", command = lambda: buscar(con, var_titulo.get(), var_genero.get(), var_estado.get(), var_socio.get())).grid(row = 4, column = 1, padx = 10, pady = 10, sticky = NSEW) 
    Button(lf_busqueda, text = "Nueva busqueda", command = limpiar_campos).grid(row = 4, column = 0,padx = 10, pady = 10, sticky = NSEW )

    # labelFrame gestion_peliculas
    lf_gestion_peliculas = LabelFrame(ventana, text = "Gestión Películas", padx = 10, pady = 10)
    lf_gestion_peliculas.grid(row = 0, column = 1, padx = 20, pady = 20)

    # campo de Entrada de datos
    Label(lf_gestion_peliculas, text = "Titulo").grid(row = 0, column = 0, sticky = W)
    Entry(lf_gestion_peliculas, textvariable = var_titulo).grid(row = 0, column = 1)
    Label(lf_gestion_peliculas, text = "Genero").grid(row = 1, column = 0, sticky = W)
    Entry(lf_gestion_peliculas, textvariable = var_genero).grid(row = 1, column = 1)
    Label(lf_gestion_peliculas, text = "Socio").grid(row = 2, column = 0, sticky = W)
    Entry(lf_gestion_peliculas, textvariable= var_socio). grid(row=2, column=1)
    Label(lf_gestion_peliculas, text = "N° Socio").grid(row = 3, column = 0, pady = 10, sticky = W)
    Entry(lf_gestion_peliculas, textvariable = var_num_socio).grid(row = 3, column = 1)
    Label(lf_gestion_peliculas, text = "Fecha Dev.").grid(row = 4, column = 0,pady = 10, sticky = W)
    Entry(lf_gestion_peliculas, textvariable = var_devolucion).grid(row = 4, column = 1)

    # botones gestion peliculas 
    Button(lf_gestion_peliculas, text = "Alquilar", width = 12, command = lambda: verificar_y_alquilar(con, var_titulo.get(), var_genero.get(), var_estado.get(), var_socio.get(), var_num_socio.get(), var_devolucion.get())).grid(row = 0, column = 2, padx = 10, pady = 10,sticky = W)
    Button(lf_gestion_peliculas, text = "Devolución", width = 12, command = lambda: devuelve_pelicula(con, var_titulo.get(), var_genero.get(), var_estado.get(), var_socio.get(), var_num_socio.get(), var_devolucion.get())).grid(row = 1, column = 2, padx = 10, pady = 10,sticky = W)
    Button(lf_gestion_peliculas, text = "Alta Pelicula", width = 12, command = recuperar_enviar_valores).grid(row = 2, column = 2, padx = 10, pady = 10,sticky = W)
    Button(lf_gestion_peliculas, text = "Baja Pelicula", width = 12, command = lambda: baja_pelicula(con, var_titulo.get())).grid(row = 3, column = 2, padx = 10, pady = 10,sticky = W)
    Button(lf_gestion_peliculas, text = "Obtener Fecha", width = 12, command = obtener_fecha).grid(row = 4, column = 2, padx = 10, pady = 10,sticky = W)

    ## menu de inicio
    menubar = Menu(ventana)

    menu_archivo = Menu(menubar, tearoff = 0)
    menu_archivo.add_command(label = "Mostrar base", command = lambda: actualizar_el_treeview(con))
    menu_archivo.add_separator()
    menu_archivo.add_command(label = "Salir", command = lambda: salir_app())#invoca a funcion salir.
    menubar.add_cascade(label = "Archivo", menu=menu_archivo)

    ventana.config(menu = menubar)

    ## funcion cargar datos desde la vista
    def carga_datos_desde_tree(event):#(ok)
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


 