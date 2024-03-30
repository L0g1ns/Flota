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
    conductor_actual = None
    secuencia_actual = 1
    max_secuencia = 0
    fecha_anterior = None

    resultados = {}  # Para almacenar la secuencia máxima de cada conductor

    for id_conductor, fecha_str in fechas_por_conductor + [(None, None)]:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d") if fecha_str else None

        if id_conductor != conductor_actual:
            if conductor_actual is not None:
                # Guardar el resultado de secuencia máxima para el conductor actual antes de reiniciar para el nuevo conductor
                max_secuencia = max(max_secuencia, secuencia_actual)
                resultados[conductor_actual] = max_secuencia
            
            # Reiniciar para el nuevo conductor
            conductor_actual = id_conductor
            secuencia_actual = 1
            max_secuencia = 0
        elif fecha - fecha_anterior == timedelta(days=1):
            # Día consecutivo de trabajo
            secuencia_actual += 1
        else:
            # Interrupción en la secuencia, reinicia el conteo
            max_secuencia = max(max_secuencia, secuencia_actual)
            secuencia_actual = 1

        fecha_anterior = fecha

    # Imprimir los resultados
    for conductor, max_dias in resultados.items():
        print(f"Conductor {conductor} tiene una secuencia máxima de {max_dias} días seguidos de trabajo.")
