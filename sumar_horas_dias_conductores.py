from db import crear_conexion_bd  # Asegúrate de que esto coincida con el nombre de la función en tu módulo db
import sqlite3


import sqlite3

def crear_conexion_bd():
    try:
        conexion = sqlite3.connect('flota.db')
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None


def sumar_horas_dias_conductores():
    conexion = crear_conexion_bd()  # Corregido para usar crear_conexion_bd
    cursor = conexion.cursor()
    
    # Consulta SQL para sumar horas y contar días trabajados por conductor
    consulta = '''
    SELECT conductores.id_driver, conductores.name_driver, SUM(nombramientos.horas) AS total_horas, COUNT(DISTINCT nombramientos.fecha) AS dias_trabajados
    FROM nombramientos
    INNER JOIN conductores ON nombramientos.id_conductor = conductores.id_driver
    GROUP BY conductores.id_driver, conductores.name_driver
    ORDER BY conductores.id_driver;
    '''
    
    try:
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        
        if resultados:
            print("Horas y días trabajados por cada conductor:")
            for resultado in resultados:
                print(f"ID Conductor: {resultado[0]}, Nombre: {resultado[1]}, Total Horas: {resultado[2]}, Días Trabajados: {resultado[3]}")
        else:
            print("No se encontraron registros de trabajo para los conductores.")
            
    except sqlite3.Error as e:
        print(f"Ocurrió un error al intentar sumar las horas y días trabajados: {e}")
        
    finally:
        conexion.close()

