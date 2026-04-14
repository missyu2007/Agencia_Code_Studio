from config.database_connection import obtener_conexion, cerrar_conexion


def obtener_todas_las_tareas():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.id_tarea, t.nombre_tarea, t.descripcion, t.prioridad,
                   t.estado, t.fecha_inicio, t.fecha_entrega,
                   t.id_proyecto, p.nombre_proyecto,
                   t.id_colaborador,
                   CONCAT(c.nombre, ' ', c.apellido) AS nombre_colaborador
            FROM tarea t
            JOIN proyecto p ON p.id_proyecto = t.id_proyecto
            JOIN colaborador c ON c.id_colaborador = t.id_colaborador
            ORDER BY t.id_tarea
        """)
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def obtener_tareas_por_proyecto(id_proyecto):
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.id_tarea, t.nombre_tarea, t.descripcion, t.prioridad,
                   t.estado, t.fecha_inicio, t.fecha_entrega,
                   CONCAT(c.nombre, ' ', c.apellido) AS nombre_colaborador
            FROM tarea t
            JOIN colaborador c ON c.id_colaborador = t.id_colaborador
            WHERE t.id_proyecto = %s
            ORDER BY t.id_tarea
        """, (id_proyecto,))
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def obtener_tareas_por_colaborador(id_colaborador):
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.id_tarea, t.nombre_tarea, t.descripcion, t.prioridad,
                   t.estado, t.fecha_inicio, t.fecha_entrega,
                   p.nombre_proyecto
            FROM tarea t
            JOIN proyecto p ON p.id_proyecto = t.id_proyecto
            WHERE t.id_colaborador = %s
            ORDER BY t.id_tarea
        """, (id_colaborador,))
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def obtener_tareas_por_estado(estado):
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.id_tarea, t.nombre_tarea, t.descripcion, t.prioridad,
                   t.estado, t.fecha_inicio, t.fecha_entrega,
                   p.nombre_proyecto,
                   CONCAT(c.nombre, ' ', c.apellido) AS nombre_colaborador
            FROM tarea t
            JOIN proyecto p ON p.id_proyecto = t.id_proyecto
            JOIN colaborador c ON c.id_colaborador = t.id_colaborador
            WHERE t.estado = %s
            ORDER BY t.id_tarea
        """, (estado,))
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def verificar_tarea_tiene_subtareas_pendientes(id_tarea):
    conexion = obtener_conexion()
    if not conexion:
        return True
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM sub_tarea
            WHERE id_tarea = %s AND estado = 'Pendiente'
        """, (id_tarea,))
        resultado = cursor.fetchone()
        return resultado[0] > 0
    finally:
        cerrar_conexion(conexion)


def obtener_reporte_avance_por_proyecto():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id_proyecto, p.nombre_proyecto, p.estado AS estado_proyecto,
                   COUNT(t.id_tarea) AS total_tareas,
                   SUM(CASE WHEN t.estado = 'Completada' THEN 1 ELSE 0 END) AS tareas_completadas,
                   SUM(CASE WHEN t.estado = 'Pendiente' THEN 1 ELSE 0 END) AS tareas_pendientes,
                   SUM(CASE WHEN t.estado = 'En Progreso' THEN 1 ELSE 0 END) AS tareas_en_progreso,
                   IFNULL(ROUND(
                       SUM(CASE WHEN t.estado = 'Completada' THEN 1 ELSE 0 END)
                       * 100.0 / NULLIF(COUNT(t.id_tarea), 0), 1
                   ), 0) AS porcentaje_avance
            FROM proyecto p
            LEFT JOIN tarea t ON t.id_proyecto = p.id_proyecto
            GROUP BY p.id_proyecto, p.nombre_proyecto, p.estado
            ORDER BY p.id_proyecto
        """)
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def insertar_tarea(nombre_tarea, descripcion, prioridad, estado, fecha_inicio,
                   fecha_entrega, id_proyecto, id_colaborador):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO tarea (nombre_tarea, descripcion, prioridad, estado,
                               fecha_inicio, fecha_entrega, id_proyecto, id_colaborador)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre_tarea, descripcion, prioridad, estado, fecha_inicio,
              fecha_entrega, id_proyecto, id_colaborador))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al insertar tarea: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def actualizar_tarea(id_tarea, nombre_tarea, descripcion, prioridad, estado,
                     fecha_inicio, fecha_entrega, id_proyecto, id_colaborador):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE tarea
            SET nombre_tarea = %s, descripcion = %s, prioridad = %s, estado = %s,
                fecha_inicio = %s, fecha_entrega = %s, id_proyecto = %s, id_colaborador = %s
            WHERE id_tarea = %s
        """, (nombre_tarea, descripcion, prioridad, estado, fecha_inicio,
              fecha_entrega, id_proyecto, id_colaborador, id_tarea))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al actualizar tarea: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def eliminar_tarea(id_tarea):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM sub_tarea WHERE id_tarea = %s", (id_tarea,))
        cursor.execute("DELETE FROM tarea WHERE id_tarea = %s", (id_tarea,))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al eliminar tarea: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def obtener_subtareas_por_tarea(id_tarea):
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_sub_tarea, descripcion, estado, id_tarea
            FROM sub_tarea
            WHERE id_tarea = %s
            ORDER BY id_sub_tarea
        """, (id_tarea,))
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def insertar_sub_tarea(descripcion, estado, id_tarea):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO sub_tarea (descripcion, estado, id_tarea)
            VALUES (%s, %s, %s)
        """, (descripcion, estado, id_tarea))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al insertar sub tarea: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def actualizar_sub_tarea(id_sub_tarea, descripcion, estado):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE sub_tarea SET descripcion = %s, estado = %s
            WHERE id_sub_tarea = %s
        """, (descripcion, estado, id_sub_tarea))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al actualizar sub tarea: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def eliminar_sub_tarea(id_sub_tarea):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM sub_tarea WHERE id_sub_tarea = %s", (id_sub_tarea,))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al eliminar sub tarea: {error}")
        return False
    finally:
        cerrar_conexion(conexion)
