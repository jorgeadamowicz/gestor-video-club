class Temas:
        """
        Clase que define los temas de personalización visual de la aplicación.

        Cada tema es representado por un diccionario que contiene pares clave-valor.
        Las claves representan elementos de la interfaz de usuario (como el fondo o los botones),
        y los valores especifican los colores o estilos asociados.

        Temas disponibles:
            - `tema_clasico`: Un estilo tradicional con colores cálidos.
            - `tema_claro`: Un estilo moderno y luminoso.
            - `tema_dark`: Un estilo oscuro y elegante.

        Atributos Estáticos:
            tema_clasico (dict): 
                Configuración del tema clásico.
            tema_claro (dict): 
                Configuración del tema claro.
            tema_dark (dict): 
                Configuración del tema oscuro.
        """
    
        tema_clasico = {  
            "fondo" : "AntiqueWhite1",
            "fondo_datapicker" : "white smoke",
            "fondo_busqueda": "white smoke",
            "fondo_gestion": "white smoke",
            "fondo_treeview" : "white smoke",
            "boton" : "snow2",
            "fondo_label": "white smoke",
            }
        """dict: Configuración del tema clásico con tonos cálidos y suaves."""

        tema_claro = {
            "fondo" : "azure",
            "fondo_datapicker" : "azure2",
            "fondo_busqueda": "azure2",
            "fondo_gestion": "azure2",
            "fondo_treeview" : "azure2",
            "boton" : "ghost white",
            "fondo_label": "azure2",
        }
        """dict: Configuración del tema claro con tonos luminosos y modernos."""
        
        tema_dark = {
            "fondo" : "snow4",
            "fondo_datapicker" : "snow3",
            "fondo_busqueda": "snow3",
            "fondo_gestion": "snow3",
            "fondo_treeview" : "snow3",
            "boton" : "snow2",
            "fondo_label": "snow3",
        }
        """dict: Configuración del tema oscuro con tonos sobrios y elegantes."""