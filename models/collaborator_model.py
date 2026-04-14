from config.database_connection import obtener_conexion, cerrar_conexion


def obtener_todos_los_colaboradores():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_colaborador, nombre, apellido, rol_colaborador,
                   especialidad, estado_disponibilidad
            FROM colaborador
            ORDER BY id_colaborador
        """)
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def obtener_colaboradores_activos():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_colaborador, nombre, apellido, rol_colaborador,
                   especialidad, estado_disponibilidad
            FROM colaborador
            WHERE estado_disponibilidad = 'Activo'
            ORDER BY nombre
        """)
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def obtener_colaboradores_sin_usuario():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id_colaborador, c.nombre, c.apellido
            FROM colaborador c
            WHERE c.id_colaborador NOT IN (SELECT id_colaborador FROM usuario)
        """)
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def contar_proyectos_activos_por_colaborador(id_colaborador):
    conexion = obtener_conexion()
    if not conexion:
        return 0
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM asignacion_proyecto ap
            JOIN proyecto p ON p.id_proyecto = ap.id_proyecto
            WHERE ap.id_colaborador = %s
              AND ap.estado_asignacion = 'Activo'
              AND p.estado = 'En Proceso'
        """, (id_colaborador,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0
    finally:
        cerrar_conexion(conexion)


def insertar_colaborador(nombre, apellido, rol_colaborador, especialidad, estado_disponibilidad):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO colaborador (nombre, apellido, rol_colaborador, especialidad, estado_disponibilidad)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellido, rol_colaborador, especialidad, estado_disponibilidad))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al insertar colaborador: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def actualizar_colaborador(id_colaborador, nombre, apellido, rol_colaborador, especialidad, estado_disponibilidad):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE colaborador
            SET nombre = %s, apellido = %s, rol_colaborador = %s,
                especialidad = %s, estado_disponibilidad = %s
            WHERE id_colaborador = %s
        """, (nombre, apellido, rol_colaborador, especialidad, estado_disponibilidad, id_colaborador))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al actualizar colaborador: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def eliminar_colaborador(id_colaborador):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM colaborador WHERE id_colaborador = %s", (id_colaborador,))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al eliminar colaborador: {error}")
        return False
    finally:
        cerrar_conexion(conexion)
