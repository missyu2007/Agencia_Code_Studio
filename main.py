import sys
import os

# Agregar el directorio raiz del proyecto al path de Python
directorio_raiz_proyecto = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, directorio_raiz_proyecto)

from views.login_view import abrir_ventana_login
from views.main_view import abrir_ventana_principal


def iniciar_aplicacion():
    """
    Punto de entrada principal del sistema AgenciaCode Studio.
    Abre la ventana de login y, si el usuario se autentica correctamente,
    abre la ventana principal del sistema.
    """
    usuario_autenticado = abrir_ventana_login()

    if usuario_autenticado:
        abrir_ventana_principal(usuario_autenticado)
    else:
        print("Acceso denegado. La aplicacion se cerrara.")


if __name__ == "__main__":
    iniciar_aplicacion()
