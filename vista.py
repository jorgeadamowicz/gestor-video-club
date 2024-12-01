from tkinter import StringVar, LabelFrame, ttk
from tkinter import Label, Entry, Button, Menu
from tkinter import CENTER, W, NSEW
from tkinter.messagebox import askquestion, showerror, showinfo, showwarning
from tkcalendar import Calendar
from validaciones import validar_campo_socio, validar_campos_alquiler, CampoInvalidoError
from estilos import Temas

## VISTA ##

class VistaVideoClub:
    def __init__(self, ventana, application) -> None:
        
        self.ventana = ventana
        self.controlador = application
        
        self.ventana.title("Videoclub")
        self.ventana.geometry("1000x650")
        self.ventana.iconbitmap("icono.ico") 
        #self.ventana.configure(bg= "AntiqueWhite1") ##CONFIGURACION ORIGINAL OK

        # Aplica un tema por defecto al iniciar, reemplaza a configuración original
        self.aplicar_temas(Temas.tema_clasico) 
        self.inicializar_datos()
        self.crear_widgets()
        
        self.actualizar_el_treeview()
   
    ## declaración e inicialización de atributos "variables Tk"
    def inicializar_datos(self):
        self.var_titulo = StringVar() #nombre
        self.var_genero = StringVar() #genero
        self.var_estado = StringVar() #estado
        self.var_socio = StringVar() #nombre socio
        self.var_num_socio = StringVar() #numero socio
        self.var_devolucion = StringVar() #fecha con tkcalendar
    
    def crear_widgets(self): 
    ## LabelFrame datapicker 
        self.lf_datapicker = LabelFrame(self.ventana, text ="Fecha Devolución", padx = 10, pady = 10)
        print("lf_datapicker creado")  # Verificar que esta línea se ejecuta (PRUEBA)
        self.lf_datapicker.grid(row=0, column=2, padx=20, pady=20)

        self.calendario = Calendar(self.lf_datapicker, date_pattern = "dd/mm/yyyy")
        self.calendario.grid(row = 0, column = 0, pady = 20)

    ## labelFrame busqueda
        self.lf_busqueda = LabelFrame(self.ventana, text = "Busqueda", padx = 10, pady = 10)
        self.lf_busqueda.grid(row=0, column=0, columnspan=1, padx=20, pady=20)

    ## campo de Entrada de datos busqueda
        self.label_buscar_titulo = Label(self.lf_busqueda, text = "Buscar por Titulo")
        self.label_buscar_titulo.grid(row = 0, column = 0, pady = 10, sticky = W)
        Entry(self.lf_busqueda, textvariable = self.var_titulo).grid(row = 0, column = 1)
        self.label_buscar_genero = Label(self.lf_busqueda, text = "Busqueda por Genero")
        self.label_buscar_genero.grid(row = 1, column = 0, pady = 10, sticky = W)
        Entry(self.lf_busqueda, textvariable = self.var_genero).grid(row=1, column=1)
        self.label_buscar_estado = Label(self.lf_busqueda, text = "Busqueda por Estado")
        self.label_buscar_estado.grid(row = 2, column = 0, pady = 10, sticky = W)
        Entry(self.lf_busqueda, textvariable = self.var_estado).grid(row=2, column=1)
        self.label_buscar_socio = Label(self.lf_busqueda, text = "Busqueda por Socio")
        self.label_buscar_socio.grid(row = 3, column = 0, pady = 10, sticky = W)
        Entry(self.lf_busqueda, textvariable = self.var_socio).grid(row = 3, column = 1)

    ## boton busqueda
        self.boton_buscar = Button(self.lf_busqueda, text = "Buscar", width = 12, command = lambda: self.buscar(self.var_titulo.get(), self.var_genero.get(), self.var_estado.get(), self.var_socio.get()))
        self.boton_buscar.grid(row = 4, column = 1, padx = 15 , pady = 15, sticky = NSEW) 
        self.boton_nueva_busqueda = Button(self.lf_busqueda, text = "Nueva busqueda", width = 12, command = self.nueva_busqueda)
        self.boton_nueva_busqueda.grid(row = 4, column = 0, padx = 15, pady = 15, sticky = NSEW )

    ## labelFrame gestion_peliculas
        self.lf_gestion_peliculas = LabelFrame(self.ventana, text = "Gestión Películas", padx = 10, pady = 10)
        self.lf_gestion_peliculas.grid(row = 0, column = 1, padx = 20, pady = 20)

    ## campo de Entrada de datos
        self.label_titulo = Label(self.lf_gestion_peliculas, text = "Titulo")
        self.label_titulo.grid(row = 0, column = 0, sticky = W)
        Entry(self.lf_gestion_peliculas, textvariable = self.var_titulo).grid(row = 0, column = 1)
        self.label_genero = Label(self.lf_gestion_peliculas, text = "Genero")
        self.label_genero.grid(row = 1, column = 0, sticky = W)
        Entry(self.lf_gestion_peliculas, textvariable = self.var_genero).grid(row = 1, column = 1)
        self.label_socio = Label(self.lf_gestion_peliculas, text = "Socio")
        self.label_socio.grid(row = 2, column = 0, sticky = W)
        Entry(self.lf_gestion_peliculas, textvariable= self.var_socio). grid(row=2, column=1)
        self.label_n_socio = Label(self.lf_gestion_peliculas, text = "N° Socio")
        self.label_n_socio.grid(row = 3, column = 0, pady = 10, sticky = W)
        Entry(self.lf_gestion_peliculas, textvariable = self.var_num_socio).grid(row = 3, column = 1)
        self.label_fecha_dev = Label(self.lf_gestion_peliculas, text = "Fecha Dev.")
        self.label_fecha_dev.grid(row = 4, column = 0,pady = 10, sticky = W)
        Entry(self.lf_gestion_peliculas, textvariable = self.var_devolucion).grid(row = 4, column = 1)

    ## botones gestion peliculas 
        self.boton_alquilar = Button(self.lf_gestion_peliculas, text = "Alquilar", width = 12, command = lambda: self.verificar_y_alquilar(self.var_titulo.get(), self.var_genero.get(), self.var_estado.get(), self.var_socio.get(), self.var_num_socio.get(), self.var_devolucion.get()))
        self.boton_alquilar.grid(row = 0, column = 2, padx = 10, pady = 10,sticky = W)
        self.boton_devolucion = Button(self.lf_gestion_peliculas, text = "Devolución", width = 12, command = lambda: self.devuelve_pelicula(self.var_titulo.get(), self.var_genero.get(), self.var_estado.get(), self.var_socio.get(), self.var_num_socio.get(), self.var_devolucion.get()))
        self.boton_devolucion.grid(row = 1, column = 2, padx = 10, pady = 10,sticky = W)
        self.boton_alta_pelicula = Button(self.lf_gestion_peliculas, text = "Alta Pelicula", width = 12, command = self.recuperar_enviar_valores)
        self.boton_alta_pelicula.grid(row = 2, column = 2, padx = 10, pady = 10,sticky = W)
        self.boton_baja_pelicula = Button(self.lf_gestion_peliculas, text = "Baja Pelicula", width = 12, command = lambda: self.baja_pelicula(self.var_titulo.get()))
        self.boton_baja_pelicula.grid(row = 3, column = 2, padx = 10, pady = 10,sticky = W)
        self.boton_obtener_fecha = Button(self.lf_gestion_peliculas, text = "Obtener Fecha", width = 12, command = self.obtener_fecha)
        self.boton_obtener_fecha.grid(row = 4, column = 2, padx = 10, pady = 10,sticky = W)

    ## funcion aplica los temas personalizados 
    def aplicar_temas(self, tema):
       
        print(f"aplicando temas{tema}")
       
        #self.ventana.configure(bg = tema['fondo']) #cambia el fondo de la ventana (ok)
        if hasattr(self, 'lf_datapicker'): #Prueba usando funcion hasattr
            self.lf_datapicker.configure(bg=tema['fondo_datapicker'])
            self.ventana.configure(bg = tema['fondo'])
            self.lf_busqueda.configure(bg = tema['fondo_busqueda'])
            self.lf_gestion_peliculas.configure(bg = tema['fondo_gestion'])
            self.lf_treeview.configure(bg = tema["fondo_treeview"])
            ## aqui se podría crear un lista "botones" y recorrerla para asignar el mismo tema. lo mismo para los "label"
            self.boton_buscar.configure(bg = tema["boton"])
            self.boton_nueva_busqueda.configure(bg = tema["boton"])
            self.boton_alquilar.configure(bg = tema["boton"])
            self.boton_devolucion.configure(bg = tema["boton"])
            self.boton_alta_pelicula.configure(bg = tema["boton"])
            self.boton_baja_pelicula.configure(bg = tema["boton"])
            
            self.label_titulo.configure(bg = tema["fondo_label"])
            self.label_genero.configure(bg = tema["fondo_label"])
            self.label_socio.configure(bg = tema["fondo_label"])
            self.label_n_socio.configure(bg = tema["fondo_label"])
            self.label_fecha_dev.configure(bg = tema["fondo_label"])
            self.label_buscar_titulo.configure(bg = tema["fondo_label"])
            self.label_buscar_genero.configure(bg = tema["fondo_label"])
            self.label_buscar_estado.configure(bg = tema["fondo_label"])
            self.label_buscar_socio.configure(bg = tema["fondo_label"])
            
        else:
            print("lf_datapicker no está definido")

        #self.lf_datapicker.configure(bg = tema['fondo_datapicker'])
        # self.lf_busqueda.configure(bg = tema['fondo_busqueda'])
        # self.lf_gestion_peliculas.configure(bg = tema['fondo_gestion'])
        # self.lf_treeview.configure(bg = tema["fondo_treeview"])
        
        # self.boton_buscar.configure(bg = tema["boton"])
        # self.boton_nueva_busqueda.configure(bg = tema["boton"])
        # self.boton_alquilar.configure(bg = tema["boton"])
        # self.boton_devolucion.configure(bg = tema["boton"])
        # self.boton_alta_pelicula.configure(bg = tema["boton"])
        # self.boton_baja_pelicula.configure(bg = tema["boton"])

    ###NOTAS:   
    # PROBLEMA: self.ventana.configure(bg = tema['fondo']) #cambia el fondo de la ventana funciona (ok), pero cuando activo otro de los atributos me da: AttributeError: (eje)'VistaVideoClub' object has no attribute 'lf_datapicker'
    ## COMPROBACIONES:
    # * lf_datapicker (eje), está definido en la linea 40 dentro del metodo crear_widgets()
    # * flujo: crear_widgets() es invocado mucho antes que aplicar_temas()
    # * los estilos se probaron y funcionan al ser llamados desde self.ventana.configure(bg = tema['ATRIBUTO'])
    # * al comprobar la linea: self.lf_datapicker.configure(bg=tema['fondo_datapicker']) utilizando "if hasattr" funciona correctamente.
    ## SOLUCION: (PROVISORIA)
    # * como funcionó el punto anterior fui agregando y probando los otros atributos y al menos quedaron funcionando aunque no es lo que prentendía.
    # * CONSULTA: 1) es probable que al utilizar la funcion ".configure", en mas de un linea, pueda tener un conflicto en tkinter. 
    # 2) como podría optimizar mi metodo aplicar_temas si bien quedó funcionando tuve que repertir muchas lineas para asignar los valores a cada elemento de la vista. 
     
                
        
    ## menu de inicio
        menubar = Menu(self.ventana)

        menu_archivo = Menu(menubar, tearoff = 0)
        menu_archivo.add_command(label = "Mostrar base", command = lambda: self.actualizar_el_treeview())
        menu_archivo.add_separator()
        menu_archivo.add_command(label = "Salir", command = lambda: self.salir_app())#invoca a funcion salir.
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Tema Clasico", command=lambda: self.aplicar_temas(Temas.tema_clasico))
        menu_archivo.add_command(label="Tema Claro", command=lambda: self.aplicar_temas(Temas.tema_claro))
        menu_archivo.add_command(label="Tema Oscuro", command=lambda: self.aplicar_temas(Temas.tema_dark))
        menubar.add_cascade(label = "Archivo", menu=menu_archivo)

        self.ventana.config(menu = menubar)

        self.configuracion_treeview()

    ## Vista ## Treeview ## 
    def configuracion_treeview(self):
        self.lf_treeview = LabelFrame(self.ventana, text="Resultados", padx = 20, pady = 20)
        self.lf_treeview.grid(row = 1, column = 0, columnspan = 3, padx = 20, pady = 20, sticky = "nsew")

        self.tree = ttk.Treeview(self.lf_treeview, columns = ("col1", "col2", "col3", "col4", "col5", "col6", "col7"), show = "headings")

        self.tree.column("col1", width=70, minwidth = 30, anchor = CENTER)
        self.tree.column("col2", width=135, minwidth = 80, anchor = CENTER)
        self.tree.column("col3", width=135, minwidth = 80, anchor = CENTER)
        self.tree.column("col4", width=135, minwidth = 80, anchor = CENTER)
        self.tree.column("col5", width=135, minwidth = 80, anchor = CENTER)
        self.tree.column("col6", width=135, minwidth = 80, anchor = CENTER)
        self.tree.column("col7", width=135, minwidth = 80, anchor = CENTER)

        self.tree.heading("col1", text = "Id")
        self.tree.heading("col2", text = "Titulo")
        self.tree.heading("col3", text = "Genero")
        self.tree.heading("col4", text = "Estado")
        self.tree.heading("col5", text = "Socio")
        self.tree.heading("col6", text = "Número")
        self.tree.heading("col7", text = "Devolución")

        self.tree.grid(row = 0, column = 0, sticky = "nsew")

    # Añadir un scrollbar al Treeview  
        scrollbar = ttk.Scrollbar(self.lf_treeview, orient = "vertical", command = self.tree.yview)
        self.tree.configure(yscroll = scrollbar.set)
        scrollbar.grid(row = 0, column = 1, sticky = 'ns')

    # evento vinculado a la vista utilizando el método bind. 
        self.tree.bind("<Double-1>", self.carga_datos_desde_tree)

    ## funcion datapicker ##
    def obtener_fecha(self):
        fecha_seleccionada = self.calendario.get_date()
        self.var_devolucion.set(fecha_seleccionada)       
            
    ## funcion verifica si la pelicula esta en catalogo 
    def verificar_y_alquilar(self, titulo, genero, estado, socio, numero, devolucion):
        resultado = self.controlador.gestiona_verifica_catalogo(titulo, genero, estado, socio, numero, devolucion)
        self.gestionar_resultado_existe_catalogo(resultado, titulo, genero, estado, socio, numero, devolucion)

    ## funcion maneja el resultado de la verificación de existencia de una película en la base de datos.
    def gestionar_resultado_existe_catalogo(self, resultado, titulo, genero, estado, socio, numero, devolucion):

        if resultado:
            estado_disponibilidad = resultado.estado
            if estado_disponibilidad == "Disponible":
                self.alquila_pelicula(titulo, genero, estado, socio, numero, devolucion)
                self.limpiar_campos()
            else:
                showwarning("Atencion", "Película No disponible en este momento!")
                self.limpiar_campos()
        else: 
            showinfo("INFO", "La película no se encuentra en catálogo!")

    ## funcion alquila pelicula.
    def alquila_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
    
        # comprobacion de campos y manejo de error. llama al metodo validar_campos_alquiler desde el modulo validaciones
        try:
            # Validar los campos antes de enviarlos al controlador
            validar_campo_socio(socio)
            validar_campos_alquiler(numero, devolucion)
       
            self.controlador.gestiona_alquilar_pelicula(titulo, genero, estado, socio, numero, devolucion)
            showinfo("INFO", "Pelicula Alquilada con exito.")
            self.actualizar_el_treeview() 
        #muestra el mensaje de error según corresponda. 
        except CampoInvalidoError as e:
            showerror("ERROR", e.mensaje)

    ## funcion devuelve pelicula.
    def devuelve_pelicula(self, titulo, genero, estado, socio, numero, devolucion):

        self.controlador.gestiona_devolver_pelicula(titulo, genero, estado, socio, numero, devolucion)
        showinfo("INFO", "Devolución exitosa")
        self.limpiar_campos()
        self.actualizar_el_treeview()  

    ## funcion getter recupera valores de campos entry y realiza el alta.
    def recuperar_enviar_valores(self): 

        el_titulo = self.var_titulo.get()
        el_genero = self.var_genero.get()
        el_estado = self.var_estado.get()
        el_socio = self.var_socio.get()
        el_numero = self.var_num_socio.get()
        la_devolucion = self.var_devolucion.get() 

        self.controlador.gestiona_alta_pelicula(el_titulo, el_genero, el_estado, el_socio, el_numero, la_devolucion)
        showinfo("INFO", "Pelicula ingresada al catálogo con exito.")
        self.limpiar_campos()
        self.actualizar_el_treeview()

    ## funcion Baja Pelicula borra registro.
    def baja_pelicula(self, titulo):
        
        respuesta = askquestion("Confimación", "Está seguro que quiere borrar la película del catálogo?")
        if respuesta == "yes":
            self.controlador.gestiona_baja_pelicula(titulo)
            showinfo("INFO", "Pelicula retirada del catalogo con exito.")
            self.actualizar_el_treeview()
            self.limpiar_campos()
        else:
            showinfo("INFO", "Operación cancelada!" )
            self.limpiar_campos()

    ## funcion buscar
    def buscar(self, titulo, genero, estado, socio):

        rows = self.controlador.gestiona_busqueda(titulo, genero, estado, socio)
        if not rows: #verifica si la lista está vacia. 
            showinfo("INFO", "La película no se encuentra en catálogo!")

        else:        
            #limpiar el treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            #Muestra los registros encontrados
            for row in rows:
                self.tree.insert("", "end", values=(row.id, row.titulo, row.genero, row.estado, row.socio, row.numero, row.devolucion))

    ## funcion nueva busqueda 
    def nueva_busqueda(self):
        self.limpiar_campos()
        self.actualizar_el_treeview()

    ## funcion que inserta los valores en el treeview. 
    def actualizar_el_treeview(self):
        
        for item in self.tree.get_children(): 
            self.tree.delete(item)   
        
        rows = self.controlador.consulta_y_actualiza() #consulta la base de datos sqlite a traves del controlador
            
    #insertar los registros en el treeview
        for row in rows:
            self.tree.insert("", "end", values=(row.id, row.titulo, row.genero, row.estado, row.socio, row.numero, row.devolucion))

    ## funcion limpiar campos 
    def limpiar_campos(self):

        self.var_titulo.set("")
        self.var_genero.set("")
        self.var_estado.set("")
        self.var_socio.set("")
        self.var_num_socio.set("")
        self.var_devolucion.set("")

    ## funcion muestra mensaje al usuario desde el except
    def mostrar_mensaje_no_encontrado(self, titulo):
        showinfo("No Encontrado", f"No se encontró coincidencia con el título '{titulo}'.")

    ## funcion salir de la aplicacion 
    def salir_app(self):
        respuesta = askquestion("Confimación", "Está seguro que quiere salir de la aplicación?")
        if respuesta == "yes":
            self.ventana.quit()
        else:
            showinfo("INFO", "Operación cancelada!" )

    ## funcion cargar datos desde la vista
    def carga_datos_desde_tree(self, event):#(ok)
        valor = self.tree.focus() #obtiene el id de la linea seleccionada
        valores = self.tree.item(valor, "values") #recupera los valores y los asigna a la variable "valores"
       
        #asigna los valores de la fila a los campos Entry a traves del metodo "setter"
        self.var_titulo.set(valores[1])
        self.var_genero.set(valores[2])
        self.var_estado.set(valores[3])
        self.var_socio.set(valores[4])
        self.var_num_socio.set(valores[5])
        self.var_devolucion.set(valores[6])
