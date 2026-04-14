import mysql.connector
from mysql.connector import Error


def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sena2025*",
            database="agenciacode_studio"
        )
        return conexion
    except Error as error:
        print(f"Error al conectar a la base de datos: {error}")
        return None


def cerrar_conexion(conexion):
    if conexion and conexion.is_connected():
        conexion.close()
