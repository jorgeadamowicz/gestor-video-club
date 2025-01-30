"""
Módulo Vista para la aplicación de Video Club.

Este módulo implementa la vista en el patrón de diseño MVC. Es responsable de gestionar 
la interfaz de usuario utilizando Tkinter y de interactuar con el controlador para realizar 
operaciones como alquiler, devolución y gestión de películas.
"""

from tkinter import StringVar, LabelFrame, ttk
from tkinter import Label, Entry, Button, Menu
from tkinter import CENTER, W, NSEW
from tkinter.messagebox import askquestion, showerror, showinfo, showwarning
from tkcalendar import Calendar
#from validaciones import validar_campo_socio, validar_campos_alquiler, CampoInvalidoError
from validaciones import validar_socio, validar_alquiler, CampoInvalidoError  #modificacion validación con decoradores
from estilos import Temas


class VistaVideoClub:
    """
    Clase VistaVideoClub.

    Esta clase gestiona la interfaz gráfica del usuario (GUI) para la aplicación de Video Club. 
    Utiliza la librería Tkinter para construir la ventana principal, los widgets y manejar las interacciones del usuario.

    Atributos:
        ventana: Instancia de Tk que representa la ventana principal.
        controlador: Instancia del controlador para interactuar con la lógica de negocio.
    """
    def __init__(self, ventana, application) -> None:
        """
        Inicializa la ventana principal y los elementos de la interfaz gráfica y configura sus parámetros básicos.
        - Establece el título y las dimensiones de la ventana.
        - Carga el ícono de la aplicación.
        - Aplica el tema predeterminado.
        - Inicializa las variables de datos y crea los widgets de la interfaz.

        Args:
            ventana: La instancia de la ventana principal (Tk).
            application: Instancia del controlador que conecta la vista con el modelo.
        """
        
        self.ventana = ventana
        self.controlador = application
        self.ventana.title("Videoclub")
        self.ventana.geometry("1000x650")
        self.ventana.iconbitmap("icono.ico") 
        self.aplicar_temas(Temas.tema_clasico)# Aplica un tema por defecto.
        self.inicializar_datos()
        self.crear_widgets()
        self.actualizar_el_treeview()
   
    def inicializar_datos(self):
        """
        Inicializa las variables StringVar que se utilizan como modelo para los campos de entrada de la interfaz.
        - Estas variables permiten enlazar datos de la interfaz con la lógica del programa.
        """
        self.var_titulo = StringVar() #nombre
        self.var_genero = StringVar() #genero
        self.var_estado = StringVar() #estado
        self.var_socio = StringVar() #nombre socio
        self.var_num_socio = StringVar() #numero socio
        self.var_devolucion = StringVar() #fecha con tkcalendar
    
    def crear_widgets(self): 
        """
        Crea y configura todos los widgets de la interfaz gráfica, incluyendo los LabelFrames, Labels, Entrys y Botones.
        """
        self.lf_datapicker = LabelFrame(self.ventana, text ="Fecha Devolución", padx = 10, pady = 10)
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
        """
        Aplica un tema personalizado a los elementos de la interfaz gráfica.

        Args:
            tema (dict): Un diccionario que contiene las configuraciones de color y estilo.
        """
        if hasattr(self, 'lf_datapicker'): #Prueba usando funcion hasattr
            self.lf_datapicker.configure(bg=tema['fondo_datapicker'])
            self.ventana.configure(bg = tema['fondo'])
            self.lf_busqueda.configure(bg = tema['fondo_busqueda'])
            self.lf_gestion_peliculas.configure(bg = tema['fondo_gestion'])
            self.lf_treeview.configure(bg = tema["fondo_treeview"])
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
        
        
    ## menu de inicio
        menubar = Menu(self.ventana)

        menu_archivo = Menu(menubar, tearoff = 0)
        menu_archivo.add_command(label = "Mostrar base", command = lambda: self.actualizar_el_treeview())
        menu_archivo.add_separator()
        menu_archivo.add_command(label = "Salir", command = lambda: self.salir_app())
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Tema Clasico", command=lambda: self.aplicar_temas(Temas.tema_clasico))
        menu_archivo.add_command(label="Tema Claro", command=lambda: self.aplicar_temas(Temas.tema_claro))
        menu_archivo.add_command(label="Tema Oscuro", command=lambda: self.aplicar_temas(Temas.tema_dark))
        menubar.add_cascade(label = "Archivo", menu=menu_archivo)

        self.ventana.config(menu = menubar)

        self.configuracion_treeview()

    ## Vista ## Treeview ## 
    def configuracion_treeview(self):
        """
        Configura el Treeview para mostrar los resultados de las búsquedas y el catálogo.
        Incluye un scrollbar para navegación.
        """
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

    def obtener_fecha(self):
        """
        Obtiene la fecha seleccionada en el widget Calendar y la asigna al campo correspondiente.
        """
        fecha_seleccionada = self.calendario.get_date()
        self.var_devolucion.set(fecha_seleccionada)       
            
    def verificar_y_alquilar(self, titulo, genero, estado, socio, numero, devolucion):
        """
        Verifica si una película está disponible para alquiler y, de ser así, la alquila.

        Args:
            titulo (str): Título de la película.
            genero (str): Género de la película.
            estado (str): Estado de la película (e.g., "Disponible").
            socio (str): Nombre del socio.
            numero (str): Número de socio.
            devolucion (str): Fecha de devolución.
        """
        resultado = self.controlador.gestiona_verifica_catalogo(titulo, genero, estado, socio, numero, devolucion)
        self.gestionar_resultado_existe_catalogo(resultado, titulo, genero, estado, socio, numero, devolucion)

    ## funcion maneja el resultado de la verificación de existencia de una película en la base de datos.
    def gestionar_resultado_existe_catalogo(self, resultado, titulo, genero, estado, socio, numero, devolucion):
        """
        Maneja el resultado de la verificación de existencia de una película en el catálogo.
        
        Esta función gestiona el flujo según el resultado de la verificación del catálogo. Si la película 
        existe y está disponible, intenta proceder con el alquiler llamando a la función decorada 
        `alquila_pelicula`. En caso de errores de validación, captura la excepción `CampoInvalidoError` 
        y notifica al usuario. También informa al usuario si la película no está disponible o no se encuentra 
        en el catálogo.

        Args:
            resultado (bool): Indica si la película existe en el catálogo.
            titulo (str): Título de la película.
            genero (str): Género de la película.
            estado (str): Estado de la película (ej. "Disponible" o "No disponible").
            socio (str): Nombre del socio que realiza el alquiler.
            numero (int): Número de identificación del socio.
            devolucion (str): Fecha de devolución de la película.

            
        Raises:
            CampoInvalidoError: Si ocurre un error en las validaciones necesarias para el alquiler.
        """
        if resultado:
            estado_disponibilidad = resultado.get("estado")#se cambió el manejo de resultado de objeto a diccionario
            if estado_disponibilidad == "Disponible":
                try:
                    # Llamada a la función decorada y validaciones
                    self.alquila_pelicula(titulo, genero, estado, socio, numero, devolucion)
                    self.limpiar_campos()
                except CampoInvalidoError as e:                    
                    # Muestra un mensaje de error si alguna validación falla
                    showerror("Error de Validación", str(e))                        
            else:
                showwarning("Atencion", "Película No disponible en este momento!")
                self.limpiar_campos()
        else: 
            showinfo("INFO", "La película no se encuentra en catálogo!")
            
    #decorador para validaciones
    @validar_socio
    @validar_alquiler

    def alquila_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        """
        Realiza el alquiler de una película si todos los campos son válidos.
        Esta función realiza las validaciones necesarias en los campos "socio", "número de socio" 
        y "devolución" mediante los decoradores `@validar_socio` y `@validar_alquiler`. Si ambas 
        validaciones son exitosas, se procede con el registro del alquiler, mostrando un mensaje 
        de confirmación. En caso de error, se muestra el mensaje correspondiente.

        Args:
            titulo (str): Título de la película.
            genero (str): Género de la película.
            estado (str): Estado de la película (ej. disponible o alquilada).
            socio (str): Nombre del socio.
            numero (int): Número de identificación del socio.
            devolucion (str): Fecha de devolución de la película.
       
        Raises:
            CampoInvalidoError: Si alguno de los campos no pasa las validaciones necesarias.
        """
        try:
            self.controlador.gestiona_alquilar_pelicula(titulo, genero, estado, socio, numero, devolucion)
            showinfo("INFO", "Pelicula Alquilada con exito.")
            self.actualizar_el_treeview()
        
        except CampoInvalidoError as e: 
            #muestra el mensaje de error según corresponda.
            showerror("ERROR", e.mensaje)

    ## funcion devuelve pelicula.
    def devuelve_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        """
        Procesa la devolución de una película alquilada.

        Args:
            titulo, genero, estado, socio, numero, devolucion: Datos de la película.
        """
        self.controlador.gestiona_devolver_pelicula(titulo, genero, estado, socio, numero, devolucion)
        showinfo("INFO", "Devolución exitosa")
        self.limpiar_campos()
        self.actualizar_el_treeview()  

    ## funcion getter recupera valores de campos entry y realiza el alta.
    def recuperar_enviar_valores(self): 
        """
        Recupera los valores de los campos de entrada y los envía al controlador para realizar el alta de una película.
        """
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
        """
        Solicita la eliminación de una película del catálogo, previa confirmación del usuario.

        Args:
            titulo (str): Título de la película a eliminar.
        """
        
        respuesta = askquestion("Confimación", "Está seguro que quiere borrar la película del catálogo?")
        if respuesta == "yes":
            self.controlador.gestiona_baja_pelicula(titulo)
            showinfo("INFO", "Pelicula retirada del catalogo con exito.")
            self.actualizar_el_treeview()
            self.limpiar_campos()
        else:
            showinfo("INFO", "Operación cancelada!" )
            self.limpiar_campos()

    
    def buscar(self, titulo, genero, estado, socio):
        """
        Busca películas en el catálogo según los criterios ingresados y muestra los resultados en el Treeview.

        Args:
            titulo, genero, estado, socio: Criterios de búsqueda.
        """
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
