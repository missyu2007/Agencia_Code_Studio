from models.user_model import (
    buscar_usuario_por_credenciales,
    obtener_todos_los_usuarios,
    insertar_usuario,
    actualizar_usuario,
    eliminar_usuario
)


def validar_inicio_de_sesion(nombre_usuario, contrasena):
    if not nombre_usuario or not contrasena:
        return None, "El nombre de usuario y la contrasena son obligatorios."
    usuario = buscar_usuario_por_credenciales(nombre_usuario, contrasena)
    if not usuario:
        return None, "Usuario o contrasena incorrectos."
    return usuario, None


def consultar_todos_los_usuarios():
    return obtener_todos_los_usuarios()


def registrar_nuevo_usuario(nombre_usuario, email, contrasena, confirmar_contrasena, rol_sistema, id_colaborador):
    if not nombre_usuario or not email or not contrasena:
        return False, "Los campos nombre, email y contrasena son obligatorios."
    if contrasena != confirmar_contrasena:
        return False, "Las contrasenas no coinciden."
    if len(contrasena) < 4:
        return False, "La contrasena debe tener al menos 4 caracteres."
    if not id_colaborador:
        return False, "Debe seleccionar un colaborador."
    exito = insertar_usuario(nombre_usuario, email, contrasena, rol_sistema, id_colaborador)
    if exito:
        return True, "Usuario registrado correctamente."
    return False, "Error al registrar el usuario. Verifique que el email o usuario no existan ya."


def modificar_usuario_existente(id_usuario, nombre_usuario, email, contrasena, confirmar_contrasena, rol_sistema):
    if not nombre_usuario or not email or not contrasena:
        return False, "Los campos nombre, email y contrasena son obligatorios."
    if contrasena != confirmar_contrasena:
        return False, "Las contrasenas no coinciden."
    exito = actualizar_usuario(id_usuario, nombre_usuario, email, contrasena, rol_sistema)
    if exito:
        return True, "Usuario actualizado correctamente."
    return False, "Error al actualizar el usuario."


def eliminar_usuario_existente(id_usuario):
    if not id_usuario:
        return False, "Debe seleccionar un usuario para eliminar."
    exito = eliminar_usuario(id_usuario)
    if exito:
        return True, "Usuario eliminado correctamente."
    return False, "Error al eliminar el usuario."
