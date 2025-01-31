"""
Módulo Servidor para la gestión remota del catálogo de películas.

Este módulo implementa un servidor basado en sockets que recibe solicitudes
JSON desde clientes remotos, consulta la base de datos a través del
controlador y devuelve los resultados en formato JSON.

Dependencias:
    - socket: Para la comunicación entre cliente y servidor.
    - json: Para la serialización y deserialización de datos.
    - BaseDeDatos (modelo.py): Gestor de la base de datos.
    - ControladorVideoClub (controlador.py): Controlador de la aplicación.

Ejemplo de uso:
    Ejecutar este script para iniciar el servidor:
    python servidor.py
"""

import socket
import json
from modelo import BaseDeDatos  # Importa la clase del modelo
from controlador import ControladorVideoClub

# Crear la instancia del modelo y luego del controlador
inventario = "video_base_orm.db"  # acceso a la base de datos
modelo = BaseDeDatos(inventario)  # Instancia del modelo y se pasa la ruta como argumento
controlador = ControladorVideoClub(modelo) #  # Instancia del controlador que recibe el modelo como argumento


#direccion y puerto donde escuchará el servidor
host = '127.0.0.1'  # Dirección local
port = 12345  # Puerto que el servidor escuchará
buffer_size = 1024 #tamaño del buffer para recibir datos

#metodo que procesa el request recibido
def procesa_request(request):
    """
    Procesa una solicitud recibida en formato JSON y devuelve una respuesta JSON.

    Args:
        request (str): Solicitud JSON enviada por el cliente.

    Returns:
        dict: Respuesta en formato JSON con los resultados o un mensaje de error.

    Excepciones:
        json.JSONDecodeError: Si el request no es un JSON válido.
    """
    
    try:
        request_data = json.loads(request)#convierte el json en diccionario de python
        action = request_data.get("action")
        modo = request_data.get("modo", "local") #por defecto el modo debe ser 'local'
        
        if action == "get_movie":
            titulo = request_data.get("query")
            #aca irá logica que invoca al metodo que realiza la consulta a bd a travez del controlador.
            #ver como manejar los datos resultantes para pasarlos a json
            resultado = controlador.gestiona_verifica_catalogo(
                titulo = titulo,
                genero = None,
                estado = None,
                socio = None,
                numero = None,
                devolucion = None,
                modo = modo
            )
            return {"status": "success", "data": resultado} if resultado else {"status": "error", "message": "Película no encontrada en catálogo."}
        else:
            return {"status": "error", "message": "Accion Inválida."}
        
    except json.JSONDecodeError:
        # Si el request no es un JSON válido
        return {"status": "error", "message": "Invalid JSON format"}

def iniciar_servidor():
    """ Configura y ejecuta el servidor de sockets. """        
    #configuracion del socket del servidor 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #vincula el socket con la direciión y el puerto
    server_socket.bind((host, port))
    #metodo listen()
    server_socket.listen(5)
    print(f"Esperando la conexion en: {host} : {port}... ")

    while True: #mantiene el servidor abierto
        client_socket, client_adress = server_socket.accept()#aceptar la conexion
        print(f"Conexion establecida con: {client_adress}")
        
        try:
            #recibe el mensaje del cliente
            data = client_socket.recv(buffer_size).decode("utf-8")
            print(f" Request recibido: {data}")

            #envia respesta al cliente
            response = procesa_request(data) #llama a la funcion encargada de procesar el requerimiento del cliente que nos retornará la respuesta
            client_socket.send(json.dumps(response).encode("utf-8"))#envía la respuesta en formato json
            print(f"Respuesta enviada al cliente: {json.dumps(response)}")

        except Exception as e: 
            print(f"Error al procesar la conexion: {e}")
        finally:
            #cerrar la conexion
            client_socket.close()

if __name__ == "__main__":
    iniciar_servidor() #inicia el servidor


