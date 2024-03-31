from db import crear_conexion_bd
from datetime import datetime, timedelta
from colorama import Fore, Style, init
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
    secuencia_actual = 0
    max_secuencia = 0
    fecha_anterior = None

    for id_conductor, fecha_str in fechas_por_conductor:
        if fecha_str is None:
            continue  # Ignorar si la fecha está vacía o es None
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")

        if id_conductor != conductor_actual:
            # Si cambiamos de conductor, imprimimos la secuencia máxima del anterior y reseteamos contadores
            if conductor_actual is not None:
                print(f"{Fore.WHITE}Conductor {Fore.YELLOW}{conductor_actual} {Fore.WHITE}tiene una secuencia máxima de {Fore.RED}{max_secuencia} {Fore.WHITE}días seguidos de trabajo.{Style.RESET_ALL}")
            conductor_actual = id_conductor
            max_secuencia = secuencia_actual = 1
            fecha_anterior = fecha
        else:
            # Si estamos en el mismo conductor, comparamos las fechas
            if fecha - fecha_anterior == timedelta(days=1):
                secuencia_actual += 1
                max_secuencia = max(max_secuencia, secuencia_actual)
            else:
                secuencia_actual = 1
            fecha_anterior = fecha

    # Imprimir la secuencia del último conductor después del bucle
    if conductor_actual is not None:
        print(f"{Fore.WHITE}Conductor {Fore.YELLOW}{conductor_actual} {Fore.WHITE}tiene una secuencia máxima de {Fore.RED}{max_secuencia} {Fore.WHITE}días seguidos de trabajo.{Style.RESET_ALL}")


