from models.project_model import (
    obtener_todos_los_proyectos,
    obtener_proyectos_por_cliente,
    obtener_proyectos_por_estado,
    obtener_proyectos_por_rango_de_fechas,
    verificar_proyecto_tiene_tareas_en_progreso,
    verificar_proyecto_tiene_tareas_pendientes,
    calcular_avance_porcentual_proyecto,
    insertar_proyecto,
    actualizar_proyecto,
    eliminar_proyecto
)


def consultar_todos_los_proyectos():
    return obtener_todos_los_proyectos()


def consultar_proyectos_por_cliente(id_cliente):
    return obtener_proyectos_por_cliente(id_cliente)


def consultar_proyectos_por_estado(estado):
    return obtener_proyectos_por_estado(estado)


def consultar_proyectos_por_rango_de_fechas(fecha_inicio, fecha_fin):
    if not fecha_inicio or not fecha_fin:
        return []
    return obtener_proyectos_por_rango_de_fechas(fecha_inicio, fecha_fin)


def consultar_avance_porcentual_de_proyecto(id_proyecto):
    return calcular_avance_porcentual_proyecto(id_proyecto)


def registrar_nuevo_proyecto(nombre_proyecto, descripcion, fecha_inicio, fecha_fin_estimada, estado, id_cliente):
    if not nombre_proyecto or not descripcion or not fecha_inicio or not fecha_fin_estimada:
        return False, "Los campos nombre, descripcion, fecha inicio y fecha fin son obligatorios."
    if not id_cliente:
        return False, "Debe seleccionar un cliente para el proyecto."
    if fecha_inicio > fecha_fin_estimada:
        return False, "La fecha de inicio no puede ser posterior a la fecha de finalizacion."
    exito = insertar_proyecto(nombre_proyecto, descripcion, fecha_inicio, fecha_fin_estimada, estado, id_cliente)
    if exito:
        return True, "Proyecto registrado correctamente."
    return False, "Error al registrar el proyecto."


def modificar_proyecto_existente(id_proyecto, nombre_proyecto, descripcion, fecha_inicio,
                                  fecha_fin_estimada, fecha_fin_real, estado, id_cliente):
    if not nombre_proyecto or not descripcion or not fecha_inicio or not fecha_fin_estimada:
        return False, "Los campos nombre, descripcion, fecha inicio y fecha fin son obligatorios."
    if fecha_inicio > fecha_fin_estimada:
        return False, "La fecha de inicio no puede ser posterior a la fecha de finalizacion."
    if estado == "Completado":
        tiene_tareas_pendientes = verificar_proyecto_tiene_tareas_pendientes(id_proyecto)
        if tiene_tareas_pendientes:
            return False, ("No se puede marcar el proyecto como 'Completado' porque tiene tareas pendientes.\n"
                           "Complete o cancele todas las tareas primero.")
    exito = actualizar_proyecto(id_proyecto, nombre_proyecto, descripcion, fecha_inicio,
                                fecha_fin_estimada, fecha_fin_real, estado, id_cliente)
    if exito:
        return True, "Proyecto actualizado correctamente."
    return False, "Error al actualizar el proyecto."


def eliminar_proyecto_existente(id_proyecto):
    """
    Regla de negocio: no se puede eliminar un proyecto con tareas en progreso.
    """
    if not id_proyecto:
        return False, "Debe seleccionar un proyecto para eliminar."
    tiene_tareas_en_progreso = verificar_proyecto_tiene_tareas_en_progreso(id_proyecto)
    if tiene_tareas_en_progreso:
        return False, ("No se puede eliminar este proyecto porque tiene tareas 'En Progreso'.\n"
                       "Complete o cancele todas las tareas primero.")
    exito = eliminar_proyecto(id_proyecto)
    if exito:
        return True, "Proyecto eliminado correctamente."
    return False, "Error al eliminar el proyecto."
