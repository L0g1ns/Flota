from db import crear_conexion_bd
from colorama import Fore, Style, init
import sqlite3
from prettytable import PrettyTable

init(autoreset=True)

class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    RESET = '\033[0m'

def crear_conexion_bd():
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lineas (
            id_linea TEXT PRIMARY KEY,
            nombre_linea TEXT,
            tipo_linea TEXT,
            tipo_bus TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

# Agregar un linea
def agregar_linea():
    id_linea = input(f"\n[+] Escribe el id del linea:\n")
    nombre_linea = input(f"\n[+] Escribe el nombre del linea:\n")
    tipo_linea= input(f"\n[+] Escribe el tipo de linea (Normal, Alta Capacidad, Urbanas Micro, Preferencia Micro, Aeropuerto):\n")
    tipo_bus = input(f"\n[+] Tipo de tipo_bus (standard, articulado, micro):\n")

    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO lineas (id_linea, nombre_linea, tipo_linea, tipo_bus)
        VALUES (?, ?, ?, ?)
    ''', (id_linea, nombre_linea, tipo_linea, tipo_bus))
    conexion.commit()
    conexion.close()
    print("linea añadido exitosamente.")

# Eliminar un linea
def eliminar_linea():
    id_linea = input("\n[+] Escribe el id del linea a eliminar:\n")
    
    # Conectarse a la base de datos
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()

    # Primero, verificar si el linea existe
    cursor.execute("SELECT * FROM lineas WHERE id_linea = ?", (id_linea,))
    if cursor.fetchone() is None:
        print("No se encontró un linea con ese ID.")
    else:
    # Eliminar el linea
        cursor.execute("DELETE FROM lineas WHERE id_linea = ?", (id_linea,))
        conexion.commit()
        print("linea eliminado exitosamente.")

    conexion.close()

def editar_linea():
    id_linea = input("\n[+] Escribe el ID del linea a editar:\n")

    # Conectarse a la base de datos
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()

    # Verificar si el linea existe
    cursor.execute("SELECT * FROM lineas WHERE id_linea = ?", (id_linea,))
    linea = cursor.fetchone()

    if linea is None:
        print("No se encontró un linea con ese ID.")
        conexion.close()
        return

    # Mostrar la información actual del linea
    print(f"Editando linea: ID: {linea[0]}, nombre: {linea[1]}, tipo_linea: {linea[2]}, tipo_bus: {linea[3]}")

    # Pedir al usuario los nuevos valores, permitiendo dejar en blanco para no cambiar
    nuevo_nombre = input("Nueva nombre del linea (deja en blanco para no cambiar): ")
    nuevo_tipo_linea = input("Nuevo tipo de linea (Normal, Alta Capacidad, Urbanas Micro, Preferencia Micro, Aeropuerto) (deja en blanco para no cambiar): ")
    nuevo_tipo_linea_bus = input("Nuevo tipo tipo_bus (deja en blanco para no cambiar): ")

    # Preparar los nuevos valores, usando los actuales si se deja el campo en blanco
    nombre_final = nuevo_nombre if nuevo_nombre.strip() != "" else linea[1]
    tipo_linea_final = nuevo_tipo_linea if nuevo_tipo_linea.strip() != "" else linea[2]
    tipo_vehiculo_final = nuevo_tipo_linea_bus if nuevo_tipo_linea_bus.strip() != "" else linea[3]

    # Actualizar el linea en la base de datos
    cursor.execute("UPDATE lineas SET nombre_linea = ?, tipo_linea= ?, tipo_bus = ? WHERE id_linea = ?", 
                   (nombre_final, tipo_linea_final, tipo_vehiculo_final, id_linea))
    conexion.commit()
    print("linea actualizado exitosamente.")

    conexion.close()


# Listar los lineas
def listar_lineas():
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM lineas')
    lineas = cursor.fetchall()

    # Creando la tabla y asignando los nombres de las columnas con colores
    tabla = PrettyTable()
    tabla.field_names = [f"{Color.GREEN}ID{Color.RESET}",
                         f"{Color.GREEN}Nombre{Color.RESET}",
                         f"{Color.GREEN}Tipo de Línea{Color.RESET}",
                         f"{Color.GREEN}Tipo de Bus{Color.RESET}"]

    if not lineas:
        print("No hay líneas registradas.")
    else:
        print("\nLista de líneas:")
        for linea in lineas:
            tabla.add_row([
                f"{Color.YELLOW}{linea[0]}{Color.RESET}",
                f"{Color.WHITE}{linea[1]}{Color.RESET}",
                f"{Color.CYAN}{linea[2]}{Color.RESET}",
                f"{Color.RED}{linea[3]}{Color.RESET}"
            ])
        
        print(tabla)
                
    conexion.close()


