import re

class CampoInvalidoError(Exception):
    """
    Excepción personalizada para manejar errores relacionados con campos inválidos.

    Args:
        mensaje (str): Mensaje descriptivo del error.

    Atributos:
        mensaje (str): Mensaje descriptivo del error.
    """
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje
        
def validar_campo_socio(socio):
    """
    Valida que el campo "socio" no esté vacío al realizar un alquiler.

    Utiliza una expresión regular para garantizar que el campo contenga al menos
    un carácter no vacío.

    Args:
        socio (str): Campo correspondiente al nombre o identificación del socio.

    Raises:
        CampoInvalidoError: Si el campo "socio" está vacío.

    Returns:
        bool: `True` si la validación es exitosa.
    """
    patron = r"\S"
    if not re.match(patron,socio):
        raise CampoInvalidoError("El campo 'socio' debe ser completado.")
    return True

def validar_campos_alquiler(numero, devolucion):
    """
    Valida los campos relacionados con el alquiler de una película.

    Verifica que el número de socio contenga únicamente dígitos y que
    el campo de devolución no esté vacío.

    Args:
        numero (str): Número de socio asociado al alquiler.
        devolucion (str): Fecha de devolución esperada.

    Raises:
        CampoInvalidoError: Si el número de socio contiene caracteres no numéricos
                            o si el campo de devolución está vacío.

    Returns:
        bool: `True` si la validación es exitosa.
    """
    if not numero.isdigit(): #comprueba si el numero de socio es entero
        raise CampoInvalidoError("El campo 'número de socio' debe contener solo números.")
    if not devolucion.strip(): # comprueba si el campo devolucion no está vacio.
        raise CampoInvalidoError("El campo 'devolución' debe ser completado.")
    return True

