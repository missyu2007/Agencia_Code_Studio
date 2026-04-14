from models.client_model import (
    obtener_todos_los_clientes,
    obtener_clientes_activos,
    verificar_cliente_tiene_proyectos_activos,
    insertar_cliente,
    actualizar_cliente,
    eliminar_cliente
)


def consultar_todos_los_clientes():
    return obtener_todos_los_clientes()


def consultar_clientes_activos():
    return obtener_clientes_activos()


def registrar_nuevo_cliente(nombre, apellido, empresa, sector, telefono, email, estado):
    if not nombre or not apellido or not sector or not telefono or not email:
        return False, "Los campos nombre, apellido, sector, telefono y email son obligatorios."
    exito = insertar_cliente(nombre, apellido, empresa, sector, telefono, email, estado)
    if exito:
        return True, "Cliente registrado correctamente."
    return False, "Error al registrar el cliente. Verifique que el email no exista ya."


def modificar_cliente_existente(id_cliente, nombre, apellido, empresa, sector, telefono, email, estado):
    if not nombre or not apellido or not sector or not telefono or not email:
        return False, "Los campos nombre, apellido, sector, telefono y email son obligatorios."
    exito = actualizar_cliente(id_cliente, nombre, apellido, empresa, sector, telefono, email, estado)
    if exito:
        return True, "Cliente actualizado correctamente."
    return False, "Error al actualizar el cliente."


def eliminar_cliente_existente(id_cliente):
    """
    Regla de negocio: no se puede eliminar un cliente con proyectos activos.
    Solo se permite desactivarlo.
    """
    if not id_cliente:
        return False, "Debe seleccionar un cliente para eliminar."
    tiene_proyectos_activos = verificar_cliente_tiene_proyectos_activos(id_cliente)
    if tiene_proyectos_activos:
        return False, ("No se puede eliminar este cliente porque tiene proyectos activos.\n"
                       "Primero desactivelo cambiando su estado a 'Inactivo'.")
    exito = eliminar_cliente(id_cliente)
    if exito:
        return True, "Cliente eliminado correctamente."
    return False, "Error al eliminar el cliente."
