import re

class CampoInvalidoError(Exception):
    """
    Excepción personalizada para manejar errores relacionados con campos inválidos.
    
    Esta excepción se utiliza para indicar que un campo obligatorio no cumple con los
    criterios esperados, como estar vacío o contener datos inválidos.

    Args:
        mensaje (str): Mensaje descriptivo del error.

    Atributos:
        mensaje (str): Mensaje descriptivo del error.
    """
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje
        
def validar_socio(funcion):#define la funcion decoradora. recibe alquilar_pelicula como argumento
    """
        Decorador para validar el campo "socio" al realizar un alquiler.
        Valida que el campo "socio" no esté vacío al realizar un alquiler.

        Este decorador garantiza que el campo "socio" no esté vacío, utilizando
        una expresión regular para garantizar que el campo contenga al menos
        un carácter no vacío.

        Args:
            funcion (Callable): La función a decorar.

        Raises:
            CampoInvalidoError: Si el campo "socio" está vacío.

        Returns:
            Callable: La función decorada que incluye la validación.
        """
    def wrapper(*args, **kwargs):#funcion modificada recibe los argumentos de la funcion orifinal (socio)
        
        socio = args[4] # Posición de 'socio' en la función original
        patron = r"\S"
        if not re.match(patron,socio):
            raise CampoInvalidoError("El campo 'socio' debe ser completado.")
        #return True
        return funcion(*args, **kwargs)  # Llama a la función original con los mismos argumentos
    return wrapper

def validar_alquiler(funcion):
    """
        Decorador que valida los campos relacionados con el alquiler de una película.

        Este decorador verifica que el número de socio sea un valor numérico y
        que el campo de devolución no esté vacío.

        Args:
            funcion (Callable): La función a decorar.

        Raises:
            CampoInvalidoError: Si el número de socio contiene caracteres no numéricos
                                o si el campo de devolución está vacío.

        Returns:
            Callable: La función decorada que incluye la validación.
        """
    def wrapper(*args, **kwargs):#funcion modificada recibe los argumentos de la funcion orifinal (numero, devolucion)
        
        numero = args[5]
        devolucion = args[6]
        if not numero.isdigit(): #comprueba si el numero de socio es entero
            raise CampoInvalidoError("El campo 'número de socio' debe contener solo números.")
        if not devolucion.strip(): # comprueba si el campo devolucion no está vacio.
            raise CampoInvalidoError("El campo 'devolución' debe ser completado.")
        #return True #retorno original
        return funcion(*args, **kwargs)  # Llama a la función original con los mismos argumentos
    return wrapper

