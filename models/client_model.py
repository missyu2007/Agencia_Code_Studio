from config.database_connection import obtener_conexion, cerrar_conexion


def obtener_todos_los_clientes():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_cliente, nombre, apellido, empresa, sector,
                   telefono, email, estado
            FROM cliente
            ORDER BY id_cliente
        """)
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def obtener_clientes_activos():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_cliente, nombre, apellido, empresa, sector,
                   telefono, email, estado
            FROM cliente
            WHERE estado = 'Activo'
            ORDER BY nombre
        """)
        return cursor.fetchall()
    finally:
        cerrar_conexion(conexion)


def verificar_cliente_tiene_proyectos_activos(id_cliente):
    conexion = obtener_conexion()
    if not conexion:
        return True
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM proyecto
            WHERE id_cliente = %s AND estado = 'En Proceso'
        """, (id_cliente,))
        resultado = cursor.fetchone()
        return resultado[0] > 0
    finally:
        cerrar_conexion(conexion)


def insertar_cliente(nombre, apellido, empresa, sector, telefono, email, estado):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO cliente (nombre, apellido, empresa, sector, telefono, email, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, empresa, sector, telefono, email, estado))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al insertar cliente: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def actualizar_cliente(id_cliente, nombre, apellido, empresa, sector, telefono, email, estado):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE cliente
            SET nombre = %s, apellido = %s, empresa = %s, sector = %s,
                telefono = %s, email = %s, estado = %s
            WHERE id_cliente = %s
        """, (nombre, apellido, empresa, sector, telefono, email, estado, id_cliente))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al actualizar cliente: {error}")
        return False
    finally:
        cerrar_conexion(conexion)


def eliminar_cliente(id_cliente):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))
        conexion.commit()
        return True
    except Exception as error:
        print(f"Error al eliminar cliente: {error}")
        return False
    finally:
        cerrar_conexion(conexion)
