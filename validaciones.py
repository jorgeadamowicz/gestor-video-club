import re

# Clase mi excepcion personalizada para manejo de error "campo invalido".
class CampoInvalidoError(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje
        
def validar_campo_socio(socio):
    # valida que el campo "socio" no se encuentre vacío al realizar el alquiler utilizando regex
    patron = r"\S"
    if not re.match(patron,socio):
        raise CampoInvalidoError("El campo 'socio' debe ser completado.")
    return True

def validar_campos_alquiler(numero, devolucion):
    if not numero.isdigit(): #comprueba si el numero de socio es entero
        raise CampoInvalidoError("El campo 'número de socio' debe contener solo números.")
    if not devolucion.strip(): # comprueba si el campo devolucion no está vacio.
        raise CampoInvalidoError("El campo 'devolución' debe ser completado.")
    return True

