import socket
import json

#direccion y puerto donde escuchará el servidor
host = '127.0.0.1'  # Dirección local
port = 12345  # Puerto que el servidor escuchará
buffer_size = 1024 #tamaño del buffer para recibir datos

#metodo que procesa el request recibido
def procesa_request(request):
    
    try:
        request_data = json.loads(request)#convierte el json en diccionario de python
        action = request_data.get("action")
        
        if action == "get_movie":
            #aca irá logica que invoca al metodo que realiza la consulta a bd a travez del controlador.
            #ver como manejar los datos resultantes para pasarlos a json
            movie_data = {
                "title": "las rubias",
                "genre": "risa",
                "status": "disponible"
            }
            return {"status": "success", "data": movie_data}
        else:
            return {"status": "error", "message": "Accion Inválida."}
        
    except json.JSONDecodeError:
        # Si el request no es un JSON válido
        return {"status": "error", "message": "Invalid JSON format"}
        
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
