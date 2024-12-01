import sqlite3


## MODELO ##

## funcion crea base de datos sqlite ## (mvc ok)
class BaseDeDatos:
    def __init__(self):
        try:
            self.con = sqlite3.connect("video_base.db")
            self.cursor = self.con.cursor()
            self.crear_tabla()
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
          
## funcion crea tabla sqlite ##

    def crear_tabla(self,):
        sql = """CREATE TABLE IF NOT EXISTS video_base (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT,
                    genero TEXT,
                    estado TEXT,
                    socio TEXT,
                    numero TEXT,
                    devolucion TEXT
                )"""
        self.cursor.execute(sql)
        self.con.commit()

    # con = crea_base_datos()
    # crea_tabla(con)

## funcion Alta Pelicula ingresa una película a la base de datos. 
    def alta_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        estado = "Disponible"
        data = (titulo, genero, estado, socio, numero, devolucion)
        sql = """INSERT INTO video_base (
                    titulo,
                    genero, 
                    estado,
                    socio,
                    numero,
                    devolucion)
                VALUES (?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(sql,data)
        self.con.commit()

## funcion Baja Pelicula de la base de datos.
    def elimina_pelicula_de_bd(self, titulo):
        sql = "DELETE FROM video_base WHERE LOWER(titulo) = LOWER(?)"
        data = (titulo, )
        self.cursor.execute(sql, data)
        self.con.commit()

## funcion consulta la base de datos y retorna info para actualizar vista
    def consulta_base_datos(self):
        sql = "SELECT * FROM video_base"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

## funcion verifica si la pelicula existe en la base de datos

    def verifica_catalogo_en_bd(self, titulo, genero, estado, socio, numero, devolucion):
        data = (titulo, )
        sql = "SELECT * FROM video_base WHERE LOWER(titulo) = LOWER(?)" 
        self.cursor.execute(sql,data)
        resultado = self.cursor.fetchone()
        return resultado
    
    
## funcion modifica registro alquiler en la base de datos

    def alquilar_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        
        estado = "Alquilada"
        data = (genero, estado, socio, numero, devolucion, titulo)
        sql = """UPDATE video_base SET
                    genero = ?,
                    estado = ?,
                    socio = ?,
                    numero = ?,
                    devolucion = ?
                WHERE LOWER(titulo) = LOWER(?)"""
        self.cursor.execute(sql,data)
        self.con.commit()
    

## funcion modifica registro devolucion en bd y actualiza la vista

    def devolver_pelicula(self, titulo, genero, estado, socio, numero, devolucion):
        
        estado = "Disponible"
        socio = ""
        numero = ""
        devolucion = ""
        sql = "UPDATE video_base SET  estado = ?, socio = ?, numero = ?, devolucion = ?  WHERE LOWER(titulo) =LOWER(?)"
        data = (estado, socio, numero, devolucion, titulo)
        self.cursor.execute(sql,data)
        self.con.commit()

## funcion busca en la base de datos

    def buscar_en_bd(self, titulo, genero, estado, socio):
        
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
        
        data = (titulo,genero, estado, socio)
        self.cursor.execute(sql,data)
        return self.cursor.fetchall()
    
    def close(self):
        if self.con:
            self.con.close()

