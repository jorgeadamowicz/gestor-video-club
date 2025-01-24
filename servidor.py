import socket

#crea un socket 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#direccion y puerto donde escuchará el servidor
host = '127.0.0.1'  # Dirección local
port = 12345  # Puerto que el servidor escuchará

#vincula el socket con la direciión y el puerto
server_socket.bind((host, port))

#metodo listen()
server_socket.listen(1)
print(f"Esperando la conexion en: {host} : {port}... ")

#aceptar la conexion
client_socket, client_adress = server_socket.accept()
print(f"Conexion establecida con: {client_adress}")

#recibe el mensaje del cliente
message = client_socket.recv(1024).decode()
print(f" Mensaje recibido: {message}")

#envia respesta al cliente
response = "Mensaje Recibido"
client_socket.send(response.encode())

#cerrar la conexion
client_socket.close()
server_socket.close()