from db import crear_conexion_bd
from prettytable import PrettyTable
from lineas import *
from colorama import Fore, Style, init
import sqlite3

# Inicialización de colorama
init(autoreset=True)

def crear_conexion_bd():
    return sqlite3.connect('flota.db')

def ejecutar_conexion(func):
    def wrapper(*args, **kwargs):
        with crear_conexion_bd() as conexion:
            cursor = conexion.cursor()
            resultado = func(cursor, *args, **kwargs)
            conexion.commit()
        return resultado
    return wrapper

@ejecutar_conexion
def crear_tabla_asignacion(cursor):
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asignacion_buses_lineas (
            id_asignacion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_vehiculo TEXT NOT NULL,
            id_linea TEXT NOT NULL,
            cantidad_buses DEFAULT NULL,       
            fecha_asignacion DATE,
            FOREIGN KEY (id_vehiculo) REFERENCES vehiculos (id_vehiculo),
            FOREIGN KEY (id_linea) REFERENCES lineas (id_linea)
        )
    ''')
    conexion.commit()
    conexion.close()

@ejecutar_conexion
def agregar_columna_cantidad_buses(cursor):
    cursor.execute('''
        ALTER TABLE lineas
        ADD COLUMN cantidad_buses INTEGER DEFAULT NULL
    ''')

@ejecutar_conexion
def asignar_bus_a_linea(cursor):
    listar_lineas()  # Esta función debería estar definida en alguna parte del código.
    id_linea = input("Selecciona el ID de la línea a la que deseas asignar un bus: ")
    cursor.execute('SELECT id_vehiculo, matricula_vehiculo, tipo_vehiculo FROM vehiculos')
    for vehiculo in cursor.fetchall():
        print(f"{Fore.YELLOW}{vehiculo[0]} | {Fore.RED}{vehiculo[1]} | {Fore.CYAN}{vehiculo[2]}{Style.RESET_ALL}")
    id_vehiculo = input("Selecciona el ID del vehículo que deseas asignar a la línea: ")
    cursor.execute('UPDATE vehiculos SET id_linea = ? WHERE id_vehiculo = ?', (id_linea, id_vehiculo))
    print(f"Vehículo {id_vehiculo} asignado a la línea {id_linea}.")

@ejecutar_conexion
def quitar_bus_de_linea(cursor):
    listar_lineas_y_vehiculos()  # Esta función debería estar definida en alguna parte del código.
    id_linea = input("Selecciona el ID de la línea de la que deseas quitar un bus: ").strip()
    cursor.execute('SELECT * FROM lineas WHERE id_linea = ?', (id_linea,))
    if not cursor.fetchone():
        print("La línea seleccionada no existe.")
        return
    cursor.execute('SELECT id_vehiculo, matricula_vehiculo, tipo_vehiculo FROM vehiculos WHERE id_linea = ?', (id_linea,))
    vehiculos = cursor.fetchall()
    if not vehiculos:
        print("No hay vehículos asignados a esta línea.")
        return
    for vehiculo in vehiculos:
        print(f"ID Vehículo: {vehiculo[0]}, Matrícula: {vehiculo[1]}, Tipo vehiculo: {vehiculo[2]}")
    id_vehiculo = input("Selecciona el ID del vehículo que deseas quitar de la línea: ").strip()
    cursor.execute('UPDATE vehiculos SET id_linea = NULL WHERE id_vehiculo = ? AND id_linea = ?', (id_vehiculo, id_linea))
    if cursor.rowcount == 0:
        print("No se pudo quitar el vehículo de la línea.")
    else:
        print(f"Vehículo {id_vehiculo} quitado de la línea {id_linea}.")

@ejecutar_conexion
def listar_lineas_y_vehiculos(cursor):
    cursor.execute('''
        SELECT l.id_linea, l.nombre_linea, COUNT(v.id_vehiculo) AS cantidad_buses,
            GROUP_CONCAT(v.id_vehiculo, ', ') AS vehiculos_asignados,
            GROUP_CONCAT(v.tipo_vehiculo, ', ') AS tipo_vehiculo
        FROM lineas l
        LEFT JOIN vehiculos v ON l.id_linea = v.id_linea
        GROUP BY l.id_linea
        ORDER BY l.id_linea
    ''')
    lineas = cursor.fetchall()

    # Creación de la tabla con cabeceras
    tabla = PrettyTable()
    tabla.field_names = [
        Fore.GREEN + "ID Línea" + Style.RESET_ALL, 
        Fore.CYAN + "Nombre Línea" + Style.RESET_ALL, 
        Fore.YELLOW + "Cantidad Buses" + Style.RESET_ALL, 
        Fore.RED + "Vehículos Asignados" + Style.RESET_ALL, 
        Fore.WHITE + "Tipos de Vehículo" + Style.RESET_ALL
    ]

    # Rellenar la tabla con los datos de cada línea, agregando colores a cada elemento
    for linea in lineas:
        tabla.add_row([
            Fore.GREEN + str(linea[0]) + Style.RESET_ALL,
            Fore.CYAN + linea[1] + Style.RESET_ALL,
            Fore.YELLOW + str(linea[2] if linea[2] != None else 0) + Style.RESET_ALL,
            Fore.RED + (linea[3] if linea[3] else 'N/A') + Style.RESET_ALL,
            Fore.WHITE + (linea[4] if linea[4] else 'N/A') + Style.RESET_ALL
        ])

    # Imprimir la tabla
    print(tabla)
