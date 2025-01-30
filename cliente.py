import tkinter as tk
from tkinter import messagebox,  LabelFrame, Entry, Button
import socket
import json

class ClienteGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente")
        self.root.geometry("500x400")
        self.root.iconbitmap("icono.ico")
    
    #Label Frame
        self.lf_busqueda = LabelFrame(self.root, text = "Consulta de catálogo reomto", padx = 10, pady = 10)
        self.lf_busqueda.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)
    
    #Label y campo de entrada para el nombre de la pelicula
        tk.Label(self.lf_busqueda, text = "Titulo de la Consulta:").grid(row = 0, column = 0, padx = 10, pady = 10)
        self.entry_titulo = Entry(self.lf_busqueda, width= 30)
        self.entry_titulo.grid(row = 0, column = 1, padx = 10, pady = 10)
    
    #boton de busqueda
        self.boton_busqueda = Button(self.lf_busqueda, text = "Buscar", command = self.consulta_pelicula)
        self.boton_busqueda.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 10)
    
    #boton limpiar campo de busqueda
        self.boton_limpiar = Button(self.lf_busqueda, text = "Limpiar", command = self.limpiar_campos)  
        self.boton_limpiar.grid(row =1, column = 1, columnspan = 2, padx = 10, pady = 10)
        
    #muestra resultados
        self.lf_resultados = LabelFrame(self.root, text = "Resultados", padx = 10, pady = 10)
        self.lf_resultados.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 10)
        
        self.resultado_texto = tk.Text(self.lf_resultados, width = 50, height = 10)
        self.resultado_texto.grid(row = 0, column = 0, padx = 10, pady = 10)

    def consulta_pelicula(self):
        titulo = self.entry_titulo.get().strip()
        if not titulo:
            messagebox.showwarning("Advertencia", "Debe ingresar el nombre del titulo a consultar") 
            return
        #crea un socket cliente y se conecta al servidor
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = '127.0.0.1'  
            port = 12345 
            client_socket.connect((host, port))
            messagebox.showinfo("Info", "Conexion establecida con el servidor.")
        
            #crea la consulta en formato json
            request = {
                "action": "get_movie",
                "querry": titulo,
                "modo": "remoto" #indica que la solicitud proviene del cliente 'remoto'
            }
            #envia la consulta al servidor
            client_socket.send(json.dumps(request).encode('utf-8'))# json.dumps() convierte el diccionario a json
            messagebox.showinfo("Info", "Solicitud enviada al servidor...")
        
            #recibe la respuesta del servidor
            response = client_socket.recv(1024).decode('utf-8')
            response_data = json.loads(response) # Convierte la cadena JSON a un diccionario con json.loads
        
            #limpia el widget Text y muestra los resultados
            self.resultado_texto.config(state = tk.NORMAL)#hojaldre aca puede ser sin el .tk
            self.resultado_texto.delete(1.0, tk.END)
            
            if response_data.get("status") == "success":
                data = response_data.get("data", {})# de response_data recupero los valores de la clave "data". 
                resultado = "\n".join(f"{key} : {value}"for key, value in data.items())#obtiene clave-valor de data y los concatena en un cadena
                self.resultado_texto.insert(tk.END, resultado)  #inserta la cadena en el widget Text  
            else:
                messagebox.showerror("Error: ", response_data.get('message', 'Error desconocido'))
            self.resultado_texto.config(state = "disabled")   
                
        except ConnectionRefusedError:
            messagebox.showerror("Error", "No se pudo establecer conexión con el servidor. ") 
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))
        finally:
            #cerrar la conexion
            client_socket.close()
            messagebox.showinfo("Info","Conexion cerrada.")
    
    #limpia los campos de entrada y la vista de resultados    
    def limpiar_campos(self):
        self.entry_titulo.delete(0, tk.END)
        self.resultado_texto.config(state = tk.NORMAL)
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.config(state = "disabled")
            
#lanza la aplicacion
if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteGui(root)
    root.mainloop()