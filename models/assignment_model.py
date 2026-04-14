from config.database_connection import obtener_conexion, cerrar_conexion


def obtener_todas_las_asignaciones():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT ap.id_asignacion, ap.fecha_vinculacion, ap.rol_en_proyecto, ap.estado_asignacion,
                   p.nombre_proyecto, ap.id_proyecto,
                   CONCAT(c.nombre, ' ', c.apellido) AS nombre_colaborador,
                   ap.id_colaborador
            FROM asignacion_proyecto ap
            JOIN proyecto p ON p.id_proyecto = ap.id_proyecto
            JOIN colaborador c ON c.id_colaborador = ap.id_colaborador
            ORDER BY ap.id_asignacion
        """)
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def obtener_asignaciones_por_proyecto(id_proyecto):
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT ap.id_asignacion, ap.rol_en_proyecto, ap.estado_asignacion,
                   ap.fecha_vinculacion,
                   CONCAT(c.nombre, ' ', c.apellido) AS nombre_colaborador,
                   c.rol_colaborador, c.especialidad, ap.id_colaborador
            FROM asignacion_proyecto ap
            JOIN colaborador c ON c.id_colaborador = ap.id_colaborador
            WHERE ap.id_proyecto = %s
            ORDER BY ap.id_asignacion
        """, (id_proyecto,))
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def insertar_asignacion(id_proyecto, id_colaborador, fecha_vinculacion, rol_en_proyecto, estado_asignacion):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO asignacion_proyecto
                (id_proyecto, id_colaborador, fecha_vinculacion, rol_en_proyecto, estado_asignacion)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_proyecto, id_colaborador, fecha_vinculacion, rol_en_proyecto, estado_asignacion))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al insertar asignacion: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def actualizar_asignacion(id_asignacion, rol_en_proyecto, estado_asignacion):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE asignacion_proyecto
            SET rol_en_proyecto = %s, estado_asignacion = %s
            WHERE id_asignacion = %s
        """, (rol_en_proyecto, estado_asignacion, id_asignacion))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al actualizar asignacion: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def eliminar_asignacion(id_asignacion):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM asignacion_proyecto WHERE id_asignacion = %s", (id_asignacion,))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al eliminar asignacion: {error}")
        return False
    finally:
        cerrar_conexion(conexion)
