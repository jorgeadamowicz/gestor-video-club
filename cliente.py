import socket
import json

#crea un socket cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# configuracion del cliente. direccion y puerto del servidor al que conectará
host = '127.0.0.1'  
port = 12345 

try:
    #conectarse al servidor
    client_socket.connect((host, port))
    print(f"Conexion establecida con el servidor.\n")
    
    #solicita al uuario en nombre de la pelicula para hacer la consulta
    querry = input("Ingrese el nombre de la pelicula a consultar: \n")
    
    #crea la consulta en formato json
    request = {
        "action": "get_movie",
        "querry": querry
    }

    #en vez de enviar un mensaje enviamos la solicitud al sercidor
    # message = "Hola maquinola!... estas por ahi?"
    # client_socket.send(message.encode())
    client_socket.send(json.dumps(request).encode('utf-8'))# json.dumps() convierte el diccionario a json
    print(f"Solicitud enviada al servidor...\n")

    #recibe la respuesta del servidor
    response = client_socket.recv(1024).decode('utf-8')
    response_data = json.loads(response) # Convierte la cadena JSON a un diccionario con json.loads
    
    #mostrar la respuesta al usuario
    if response_data.get("status") == "success":
        print(f"\nDatos de la película colicitda: ")
        data = response_data.get("data", {})# de response_data recupero los valores de la clave "data". 
        for key, value in data.items():#obtiene clave-valor de data
            print(f"{key}: {value}")
    else:
        print(f"\nError: ", {response_data.get('message', 'Error desconocido')})
except ConnectionRefusedError:
    print(f"No se pudo establecer conexión con el servidor. Asegúrate de que esté en ejecución.") 
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    #cerrar la conexion
    client_socket.close()
    print("\nConexion cerrada.")