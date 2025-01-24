import socket

#crea un socket cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#direccion y puerto del servidor al que conectará
host = '127.0.0.1'  
port = 12345 

#conectarse al servidor
client_socket.connect((host, port))

#enviar un mensaje al sercidor
message = "Hola maquinola!... estas por ahi?"
client_socket.send(message.encode())

#recibe la respuesta del servidor
response = client_socket.recv(1024).decode()
print(f"Respuesta del servidor: {response}")

#cerrar la conexion
client_socket.close()