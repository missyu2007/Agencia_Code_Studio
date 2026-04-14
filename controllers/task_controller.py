from datetime import datetime, date
from models.task_model import (
    obtener_todas_las_tareas,
    obtener_tareas_por_proyecto,
    obtener_tareas_por_colaborador,
    obtener_tareas_por_estado,
    verificar_tarea_tiene_subtareas_pendientes,
    obtener_reporte_avance_por_proyecto,
    insertar_tarea,
    actualizar_tarea,
    eliminar_tarea,
    obtener_subtareas_por_tarea,
    insertar_sub_tarea,
    actualizar_sub_tarea,
    eliminar_sub_tarea
)
from models.project_model import obtener_todos_los_proyectos
from models.collaborator_model import obtener_colaboradores_activos


def _convertir_a_fecha(valor):
    """
    Convierte cualquier representacion de fecha a un objeto date de Python.
    Acepta: str 'YYYY-MM-DD', datetime, date, o None.
    Retorna un objeto date o None si no puede convertir.
    """
    if valor is None or valor == "":
        return None
    if isinstance(valor, date):
        return valor
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, str):
        texto = valor.strip()
        for formato in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(texto, formato).date()
            except ValueError:
                continue
    return None


def consultar_todas_las_tareas():
    return obtener_todas_las_tareas()


def consultar_tareas_por_proyecto(id_proyecto):
    return obtener_tareas_por_proyecto(id_proyecto)


def consultar_tareas_por_colaborador(id_colaborador):
    return obtener_tareas_por_colaborador(id_colaborador)


def consultar_tareas_por_estado(estado):
    return obtener_tareas_por_estado(estado)


def consultar_reporte_avance_proyectos():
    return obtener_reporte_avance_por_proyecto()


def _verificar_proyecto_no_completado(id_proyecto):
    """
    Retorna (True, None) si el proyecto NO está completado y se puede operar.
    Retorna (False, mensaje) si el proyecto está completado o no se encuentra.
    """
    proyectos = obtener_todos_los_proyectos()
    proyecto = next((p for p in proyectos if p["id_proyecto"] == id_proyecto), None)
    if proyecto and proyecto.get("estado") == "Completado":
        return False, (
            f"No se puede asignar una tarea al proyecto '{proyecto['nombre_proyecto']}' "
            "porque ya está marcado como Completado."
        )
    return True, None


def registrar_nueva_tarea(nombre_tarea, descripcion, prioridad, estado, fecha_inicio,
                          fecha_entrega, id_proyecto, id_colaborador, fecha_fin_proyecto):
    """
    Reglas de negocio:
    - Campos obligatorios completos.
    - El proyecto no puede estar en estado 'Completado'.
    - fecha_inicio no puede ser posterior a fecha_entrega.
    - fecha_entrega no puede ser posterior a fecha_fin del proyecto.
    - Debe haber proyecto y colaborador seleccionados.
    """
    if not nombre_tarea or not descripcion:
        return False, "El nombre y la descripcion de la tarea son obligatorios."
    if not fecha_inicio or not fecha_entrega:
        return False, "Las fechas de inicio y entrega son obligatorias (formato YYYY-MM-DD)."
    if not id_proyecto:
        return False, "Debe seleccionar un proyecto."
    if not id_colaborador:
        return False, "Debe seleccionar un colaborador responsable."

    permitido, mensaje_bloqueo = _verificar_proyecto_no_completado(id_proyecto)
    if not permitido:
        return False, mensaje_bloqueo

    # Convertir fechas a objetos date para comparacion segura
    fecha_inicio_date    = _convertir_a_fecha(fecha_inicio)
    fecha_entrega_date   = _convertir_a_fecha(fecha_entrega)
    fecha_fin_proyecto_date = _convertir_a_fecha(fecha_fin_proyecto)

    if fecha_inicio_date is None:
        return False, f"Formato de fecha de inicio invalido: '{fecha_inicio}'. Use YYYY-MM-DD."
    if fecha_entrega_date is None:
        return False, f"Formato de fecha de entrega invalido: '{fecha_entrega}'. Use YYYY-MM-DD."

    if fecha_inicio_date > fecha_entrega_date:
        return False, "La fecha de inicio no puede ser posterior a la fecha de entrega."

    if fecha_fin_proyecto_date is not None:
        if fecha_entrega_date > fecha_fin_proyecto_date:
            return False, (
                f"La fecha de entrega de la tarea ({fecha_entrega}) no puede ser posterior "
                f"a la fecha de finalizacion del proyecto ({fecha_fin_proyecto})."
            )

    exito = insertar_tarea(
        nombre_tarea, descripcion, prioridad, estado,
        fecha_inicio, fecha_entrega, id_proyecto, id_colaborador
    )
    if exito:
        return True, "Tarea registrada correctamente."
    return False, "Error al registrar la tarea en la base de datos."


def modificar_tarea_existente(id_tarea, nombre_tarea, descripcion, prioridad, estado,
                               fecha_inicio, fecha_entrega, id_proyecto, id_colaborador,
                               fecha_fin_proyecto):
    if not nombre_tarea or not descripcion:
        return False, "El nombre y la descripcion de la tarea son obligatorios."
    if not fecha_inicio or not fecha_entrega:
        return False, "Las fechas de inicio y entrega son obligatorias (formato YYYY-MM-DD)."

    permitido, mensaje_bloqueo = _verificar_proyecto_no_completado(id_proyecto)
    if not permitido:
        return False, mensaje_bloqueo

    fecha_inicio_date       = _convertir_a_fecha(fecha_inicio)
    fecha_entrega_date      = _convertir_a_fecha(fecha_entrega)
    fecha_fin_proyecto_date = _convertir_a_fecha(fecha_fin_proyecto)

    if fecha_inicio_date is None:
        return False, f"Formato de fecha de inicio invalido: '{fecha_inicio}'. Use YYYY-MM-DD."
    if fecha_entrega_date is None:
        return False, f"Formato de fecha de entrega invalido: '{fecha_entrega}'. Use YYYY-MM-DD."

    if fecha_inicio_date > fecha_entrega_date:
        return False, "La fecha de inicio no puede ser posterior a la fecha de entrega."

    if fecha_fin_proyecto_date is not None:
        if fecha_entrega_date > fecha_fin_proyecto_date:
            return False, (
                f"La fecha de entrega de la tarea ({fecha_entrega}) no puede ser posterior "
                f"a la fecha de finalizacion del proyecto ({fecha_fin_proyecto})."
            )

    if estado == "Completada":
        tiene_subtareas_pendientes = verificar_tarea_tiene_subtareas_pendientes(id_tarea)
        if tiene_subtareas_pendientes:
            return False, (
                "No se puede marcar la tarea como 'Completada' porque tiene subtareas pendientes.\n"
                "Complete todas las subtareas primero."
            )

    exito = actualizar_tarea(
        id_tarea, nombre_tarea, descripcion, prioridad, estado,
        fecha_inicio, fecha_entrega, id_proyecto, id_colaborador
    )
    if exito:
        return True, "Tarea actualizada correctamente."
    return False, "Error al actualizar la tarea."


def eliminar_tarea_existente(id_tarea):
    if not id_tarea:
        return False, "Debe seleccionar una tarea para eliminar."
    exito = eliminar_tarea(id_tarea)
    if exito:
        return True, "Tarea eliminada correctamente."
    return False, "Error al eliminar la tarea."


# ── Subtareas ─────────────────────────────────────────────────────

def consultar_subtareas_por_tarea(id_tarea):
    return obtener_subtareas_por_tarea(id_tarea)


def registrar_nueva_sub_tarea(descripcion, estado, id_tarea):
    if not descripcion:
        return False, "La descripcion de la subtarea es obligatoria."
    if not id_tarea:
        return False, "Debe seleccionar una tarea padre."
    exito = insertar_sub_tarea(descripcion, estado, id_tarea)
    if exito:
        return True, "Subtarea registrada correctamente."
    return False, "Error al registrar la subtarea."


def modificar_sub_tarea_existente(id_sub_tarea, descripcion, estado):
    if not descripcion:
        return False, "La descripcion de la subtarea es obligatoria."
    exito = actualizar_sub_tarea(id_sub_tarea, descripcion, estado)
    if exito:
        return True, "Subtarea actualizada correctamente."
    return False, "Error al actualizar la subtarea."


def eliminar_sub_tarea_existente(id_sub_tarea):
    if not id_sub_tarea:
        return False, "Debe seleccionar una subtarea para eliminar."
    exito = eliminar_sub_tarea(id_sub_tarea)
    if exito:
        return True, "Subtarea eliminada correctamente."
    return False, "Error al eliminar la subtarea."