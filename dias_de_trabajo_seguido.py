from db import crear_conexion_bd
from datetime import datetime, timedelta
import sqlite3

def crear_conexion_bd():
    try:
        conexion = sqlite3.connect('flota.db')
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def obtener_fechas_trabajo_conductor():
    conexion = crear_conexion_bd()
    cursor = conexion.cursor()
    
    consulta = '''
    SELECT id_conductor, fecha
    FROM nombramientos
    ORDER BY id_conductor, fecha;
    '''
    
    try:
        cursor.execute(consulta)
        fechas_por_conductor = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener las fechas de trabajo por conductor: {e}")
        fechas_por_conductor = []
    finally:
        conexion.close()

    return fechas_por_conductor



def analizar_dias_consecutivos(fechas_por_conductor):
    # Supongamos que 'fechas_por_conductor' es una lista de tuplas (id_conductor, 'fecha')
    conductor_actual = None
    secuencia_actual = 1
    max_secuencia = 0
    fecha_anterior = None

    for id_conductor, fecha_str in fechas_por_conductor:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        if id_conductor != conductor_actual:
            # Nuevo conductor, reinicia el conteo
            conductor_actual = id_conductor
            max_secuencia = max(max_secuencia, secuencia_actual)
            secuencia_actual = 1
        elif fecha - fecha_anterior == timedelta(days=1):
            # Día consecutivo de trabajo
            secuencia_actual += 1
        else:
            # Interrupción en la secuencia, reinicia el conteo
            max_secuencia = max(max_secuencia, secuencia_actual)
            secuencia_actual = 1
        fecha_anterior = fecha

        print(f"Conductor {id_conductor} tiene una secuencia máxima de {max_secuencia} días seguidos de trabajo.")

# Llamar a la función con los resultados obtenidos de la base de datos
fechas_trabajo = obtener_fechas_trabajo_conductor()
analizar_dias_consecutivos(fechas_trabajo)