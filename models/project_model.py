from config.database_connection import obtener_conexion, cerrar_conexion


def obtener_todos_los_proyectos():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id_proyecto, p.nombre_proyecto, p.descripcion,
                   p.fecha_inicio, p.fecha_fin_estimada, p.fecha_fin_real,
                   p.estado, p.id_cliente,
                   CONCAT(c.nombre, ' ', c.apellido) AS nombre_cliente
            FROM proyecto p
            JOIN cliente c ON c.id_cliente = p.id_cliente
            ORDER BY p.id_proyecto
        """)
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def obtener_proyectos_por_cliente(id_cliente):
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id_proyecto, p.nombre_proyecto, p.estado
            FROM proyecto p
            WHERE p.id_cliente = %s
            ORDER BY p.nombre_proyecto
        """, (id_cliente,))
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def obtener_proyectos_por_estado(estado):
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id_proyecto, p.nombre_proyecto, p.descripcion,
                   p.fecha_inicio, p.fecha_fin_estimada, p.estado,
                   CONCAT(c.nombre, ' ', c.apellido) AS nombre_cliente
            FROM proyecto p
            JOIN cliente c ON c.id_cliente = p.id_cliente
            WHERE p.estado = %s
            ORDER BY p.nombre_proyecto
        """, (estado,))
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def obtener_proyectos_por_rango_de_fechas(fecha_inicio, fecha_fin):
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id_proyecto, p.nombre_proyecto, p.descripcion,
                   p.fecha_inicio, p.fecha_fin_estimada, p.estado,
                   CONCAT(c.nombre, ' ', c.apellido) AS nombre_cliente
            FROM proyecto p
            JOIN cliente c ON c.id_cliente = p.id_cliente
            WHERE p.fecha_inicio BETWEEN %s AND %s
            ORDER BY p.fecha_inicio
        """, (fecha_inicio, fecha_fin))
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def verificar_proyecto_tiene_tareas_en_progreso(id_proyecto):
    conexion = obtener_conexion()
    if not conexion:
        return True
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM tarea
            WHERE id_proyecto = %s AND estado = 'En Progreso'
        """, (id_proyecto,))
        resultado = cursor.fetchone()
        return resultado[0] > 0
    finally:
        cerrar_conexion(conexion)


def verificar_proyecto_tiene_tareas_pendientes(id_proyecto):
    conexion = obtener_conexion()
    if not conexion:
        return True
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM tarea
            WHERE id_proyecto = %s AND estado NOT IN ('Completada', 'Cancelada')
        """, (id_proyecto,))
        resultado = cursor.fetchone()
        return resultado[0] > 0
    finally:
        cerrar_conexion(conexion)


def calcular_avance_porcentual_proyecto(id_proyecto):
    conexion = obtener_conexion()
    if not conexion:
        return 0
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) AS total_tareas,
                SUM(CASE WHEN estado = 'Completada' THEN 1 ELSE 0 END) AS tareas_completadas
            FROM tarea
            WHERE id_proyecto = %s
        """, (id_proyecto,))
        resultado = cursor.fetchone()
        total_tareas = resultado[0]
        tareas_completadas = resultado[1] or 0
        if total_tareas == 0:
            return 0
        return round((tareas_completadas / total_tareas) * 100, 1)
    finally:
        cerrar_conexion(conexion)


def insertar_proyecto(nombre_proyecto, descripcion, fecha_inicio, fecha_fin_estimada, estado, id_cliente):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO proyecto (nombre_proyecto, descripcion, fecha_inicio,
                                  fecha_fin_estimada, estado, id_cliente)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre_proyecto, descripcion, fecha_inicio, fecha_fin_estimada, estado, id_cliente))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al insertar proyecto: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def actualizar_proyecto(id_proyecto, nombre_proyecto, descripcion, fecha_inicio,
                        fecha_fin_estimada, fecha_fin_real, estado, id_cliente):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE proyecto
            SET nombre_proyecto = %s, descripcion = %s, fecha_inicio = %s,
                fecha_fin_estimada = %s, fecha_fin_real = %s, estado = %s, id_cliente = %s
            WHERE id_proyecto = %s
        """, (nombre_proyecto, descripcion, fecha_inicio, fecha_fin_estimada,
              fecha_fin_real, estado, id_cliente, id_proyecto))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al actualizar proyecto: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def eliminar_proyecto(id_proyecto):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM proyecto WHERE id_proyecto = %s", (id_proyecto,))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al eliminar proyecto: {error}")
        return False
    finally:
        cerrar_conexion(conexion)
