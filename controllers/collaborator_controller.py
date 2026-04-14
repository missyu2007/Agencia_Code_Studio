from models.collaborator_model import (
    obtener_todos_los_colaboradores,
    obtener_colaboradores_activos,
    obtener_colaboradores_sin_usuario,
    contar_proyectos_activos_por_colaborador,
    insertar_colaborador,
    actualizar_colaborador,
    eliminar_colaborador
)
from models.assignment_model import (
    obtener_todas_las_asignaciones,
    obtener_asignaciones_por_proyecto,
    insertar_asignacion,
    actualizar_asignacion,
    eliminar_asignacion
)


# --- Colaboradores ---

def consultar_todos_los_colaboradores():
    return obtener_todos_los_colaboradores()


def consultar_colaboradores_activos():
    return obtener_colaboradores_activos()


def consultar_colaboradores_sin_usuario():
    return obtener_colaboradores_sin_usuario()


def registrar_nuevo_colaborador(nombre, apellido, rol_colaborador, especialidad, estado_disponibilidad):
    if not nombre or not apellido or not rol_colaborador or not especialidad:
        return False, "Los campos nombre, apellido, rol y especialidad son obligatorios."
    exito = insertar_colaborador(nombre, apellido, rol_colaborador, especialidad, estado_disponibilidad)
    if exito:
        return True, "Colaborador registrado correctamente."
    return False, "Error al registrar el colaborador."


def modificar_colaborador_existente(id_colaborador, nombre, apellido, rol_colaborador,
                                     especialidad, estado_disponibilidad):
    if not nombre or not apellido or not rol_colaborador or not especialidad:
        return False, "Los campos nombre, apellido, rol y especialidad son obligatorios."
    exito = actualizar_colaborador(id_colaborador, nombre, apellido, rol_colaborador,
                                   especialidad, estado_disponibilidad)
    if exito:
        return True, "Colaborador actualizado correctamente."
    return False, "Error al actualizar el colaborador."


def eliminar_colaborador_existente(id_colaborador):
    if not id_colaborador:
        return False, "Debe seleccionar un colaborador para eliminar."
    exito = eliminar_colaborador(id_colaborador)
    if exito:
        return True, "Colaborador eliminado correctamente."
    return False, "Error al eliminar el colaborador. Puede tener tareas o asignaciones asociadas."


# --- Asignaciones proyecto-colaborador ---

def consultar_todas_las_asignaciones():
    return obtener_todas_las_asignaciones()


def consultar_asignaciones_por_proyecto(id_proyecto):
    return obtener_asignaciones_por_proyecto(id_proyecto)


def registrar_nueva_asignacion(id_proyecto, id_colaborador, fecha_vinculacion,
                                rol_en_proyecto, estado_asignacion):
    """
    Regla de negocio: un colaborador no puede tener más de 3 proyectos activos.
    """
    if not id_proyecto or not id_colaborador or not fecha_vinculacion:
        return False, "Proyecto, colaborador y fecha de vinculacion son obligatorios."
    cantidad_proyectos_activos = contar_proyectos_activos_por_colaborador(id_colaborador)
    if cantidad_proyectos_activos >= 3:
        return False, ("Este colaborador ya tiene 3 proyectos activos asignados.\n"
                       "No se puede asignar a mas proyectos activos.")
    exito = insertar_asignacion(id_proyecto, id_colaborador, fecha_vinculacion,
                                rol_en_proyecto, estado_asignacion)
    if exito:
        return True, "Asignacion registrada correctamente."
    return False, "Error al registrar la asignacion. El colaborador puede ya estar asignado a este proyecto."


def modificar_asignacion_existente(id_asignacion, rol_en_proyecto, estado_asignacion):
    if not id_asignacion:
        return False, "Debe seleccionar una asignacion para modificar."
    exito = actualizar_asignacion(id_asignacion, rol_en_proyecto, estado_asignacion)
    if exito:
        return True, "Asignacion actualizada correctamente."
    return False, "Error al actualizar la asignacion."


def eliminar_asignacion_existente(id_asignacion):
    if not id_asignacion:
        return False, "Debe seleccionar una asignacion para eliminar."
    exito = eliminar_asignacion(id_asignacion)
    if exito:
        return True, "Asignacion eliminada correctamente."
    return False, "Error al eliminar la asignacion."
