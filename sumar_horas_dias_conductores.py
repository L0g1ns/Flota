from db import crear_conexion_bd  # Asegúrate de que esto coincida con el nombre de la función en tu módulo db
import sqlite3
from colorama import Fore, Style, init

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
    SELECT 
        conductores.id_driver, 
        conductores.name_driver, 
        SUM(nombramientos.horas) AS total_horas, 
        COUNT(DISTINCT nombramientos.fecha) AS dias_trabajados
    FROM 
        nombramientos
    INNER JOIN 
        conductores 
        ON nombramientos.id_conductor = conductores.id_driver
    GROUP BY 
        conductores.id_driver

    '''
    
    try:
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        
        if resultados:
            print("Horas y días trabajados por cada conductor:")
            for resultado in resultados:
                print(f"{Fore.CYAN}ID Conductor: {Fore.YELLOW}{resultado[0]}, "
                    f"{Fore.CYAN}Nombre: {Fore.WHITE}{resultado[1]}, "
                    f"{Fore.CYAN}Total Horas: {Fore.RED}{resultado[2]}, "
                    f"{Fore.CYAN}Días Trabajados: {Fore.GREEN}{resultado[3]}{Style.RESET_ALL}")
        else:
            print("No se encontraron registros de trabajo para los conductores.")
            
    except sqlite3.Error as e:
        print(f"Ocurrió un error al intentar sumar las horas y días trabajados: {e}")
        
    finally:
        conexion.close()

