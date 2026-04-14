from config.database_connection import obtener_conexion, cerrar_conexion


def buscar_usuario_por_credenciales(nombre_usuario, contrasena):
    conexion = obtener_conexion()
    if not conexion:
        return None
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT u.id_usuario, u.nombre_usuario, u.email, u.rol_sistema,
                   c.nombre AS nombre_colaborador, c.apellido AS apellido_colaborador
            FROM usuario u
            JOIN colaborador c ON c.id_colaborador = u.id_colaborador
            WHERE u.nombre_usuario = %s AND u.contrasena = %s
        """
        cursor.execute(consulta, (nombre_usuario, contrasena))
        usuario = cursor.fetchone()
        return usuario
    finally:
        cerrar_conexion(conexion)


def obtener_todos_los_usuarios():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT u.id_usuario, u.nombre_usuario, u.email, u.rol_sistema,
                   c.nombre AS nombre_colaborador, c.apellido AS apellido_colaborador,
                   c.estado_disponibilidad
            FROM usuario u
            JOIN colaborador c ON c.id_colaborador = u.id_colaborador
            ORDER BY u.id_usuario
        """
        cursor.execute(consulta)
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def insertar_usuario(nombre_usuario, email, contrasena, rol_sistema, id_colaborador):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO usuario (nombre_usuario, email, contrasena, rol_sistema, id_colaborador)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(consulta, (nombre_usuario, email, contrasena, rol_sistema, id_colaborador))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al insertar usuario: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def actualizar_usuario(id_usuario, nombre_usuario, email, contrasena, rol_sistema):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        consulta = """
            UPDATE usuario
            SET nombre_usuario = %s, email = %s, contrasena = %s, rol_sistema = %s
            WHERE id_usuario = %s
        """
        cursor.execute(consulta, (nombre_usuario, email, contrasena, rol_sistema, id_usuario))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al actualizar usuario: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def eliminar_usuario(id_usuario):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al eliminar usuario: {error}")
        return False
    finally:
        cerrar_conexion(conexion)
