import sqlite3


## MODELO ##

## funcion crea base de datos sqlite ## (mvc ok) SE PODRIA AGREGAR UN TRY/EXCEPT POR SI FALLA LA CONEXION. 

def crea_base_datos():
    con = sqlite3.connect("video_base.db")
    return con

## funcion crea tabla sqlite ##

def crea_tabla(con):
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS video_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Titulo TEXT,
                Genero TEXT,
                Estado TEXT,
                Socio TEXT,
                Numero TEXT,
                Devolucion TEXT
            )"""
    cursor.execute(sql)
    con.commit()

con = crea_base_datos()
crea_tabla(con)

## funcion Alta Pelicula ingresa una película a la base de datos. 
def alta_pelicula(con, titulo, genero, estado, socio, numero, devolucion):
    cursor = con.cursor()
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
    cursor.execute(sql,data)
    con.commit()

## funcion Baja Pelicula de la base de datos.
def elimina_pelicula_de_bd(con, titulo):
    cursor = con.cursor()
    sql = "DELETE FROM video_base WHERE LOWER(titulo) = LOWER(?)"
    data = (titulo, )
    cursor.execute(sql, data)
    con.commit()

## funcion consulta la base de datos y retorna info para actualizar vista
def consulta_base_datos(con):
    cursor = con.cursor()
    sql = "SELECT * FROM video_base"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

## funcion verifica si la pelicula existe en la base de datos

def verifica_catalogo_en_bd(con, titulo, genero, estado, socio, numero, devolucion):
    cursor = con.cursor()
    data = (titulo, )
    sql = "SELECT * FROM video_base WHERE LOWER(Titulo) = LOWER(?)" 
    cursor.execute(sql,data)
    resultado = cursor.fetchone()
    return resultado
    
    
## funcion modifica registro alquiler en la base de datos

def alquilar_pelicula(con, titulo, genero, estado, socio, numero, devolucion):
    
    cursor = con.cursor()
    estado = "Alquilada"
    data = (genero, estado, socio, numero, devolucion, titulo)
    sql = """UPDATE video_base SET
                genero = ?,
                estado = ?,
                socio = ?,
                numero = ?,
                devolucion = ?
            WHERE LOWER(titulo) = LOWER(?)"""
    cursor.execute(sql,data)
    con.commit()
    

## funcion modifica registro devolucion en bd y actualiza la vista

def devolver_pelicula(con, titulo, genero, estado, socio, numero, devolucion):

    cursor = con.cursor()
    estado = "Disponible"
    socio = ""
    numero = ""
    devolucion = ""
    sql = "UPDATE video_base SET  estado = ?, socio = ?, numero = ?, devolucion = ?  WHERE LOWER(titulo) =LOWER(?)"
    data = (estado, socio, numero, devolucion, titulo)
    cursor.execute(sql,data)
    con.commit()

## funcion busca en la base de datos

def buscar_en_bd(con, titulo, genero, estado, socio):
    
    cursor = con.cursor()
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
    cursor.execute(sql,data)
    return cursor.fetchall()

    