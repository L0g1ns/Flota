from db import crear_conexion_bd
from colorama import Fore, Style, init
import sqlite3
from prettytable import PrettyTable

class Color:
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def crear_conexion_bd():
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehiculos (
            id_vehiculo TEXT PRIMARY KEY,
            matricula_vehiculo TEXT,
            tipo_vehiculo TEXT,
            combustible TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

# Agregar un vehiculo
def agregar_vehiculo():
    id_vehiculo = input(f"\n[+] Escribe el id del vehiculo:\n")
    matricula_vehiculo = input(f"\n[+] Escribe la matrícula del vehiculo:\n")
    tipo_vehiculo= input(f"\n[+] Escribe el tipo de vehiculo (articulado, standard, micro):\n")
    combustible = input(f"\n[+] Tipo de combustible:\n")

    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO vehiculos (id_vehiculo, matricula_vehiculo, tipo_vehiculo, combustible)
        VALUES (?, ?, ?, ?)
    ''', (id_vehiculo, matricula_vehiculo, tipo_vehiculo, combustible))
    conexion.commit()
    conexion.close()
    print("Vehiculo añadido exitosamente.")

# Eliminar un vehiculo
def eliminar_vehiculo():
    id_vehiculo = input("\n[+] Escribe el id del vehiculo a eliminar:\n")
    
    # Conectarse a la base de datos
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()

    # Primero, verificar si el vehiculo existe
    cursor.execute("SELECT * FROM vehiculos WHERE id_vehiculo = ?", (id_vehiculo,))
    if cursor.fetchone() is None:
        print("No se encontró un vehiculo con ese ID.")
    else:
        # Eliminar el vehiculo
        cursor.execute("DELETE FROM vehiculos WHERE id_vehiculo = ?", (id_vehiculo,))
        conexion.commit()
        print("Vehiculo eliminado exitosamente.")

    conexion.close()

def editar_vehiculo():
    id_vehiculo = input("\n[+] Escribe el ID del vehiculo a editar:\n")

    # Conectarse a la base de datos
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()

    # Verificar si el vehiculo existe
    cursor.execute("SELECT * FROM vehiculos WHERE id_vehiculo = ?", (id_vehiculo,))
    vehiculo = cursor.fetchone()

    if vehiculo is None:
        print("No se encontró un vehiculo con ese ID.")
        conexion.close()
        return

    # Mostrar la información actual del vehiculo
    print(f"Editando Vehiculo: ID: {vehiculo[0]}, matricula: {vehiculo[1]}, tipo_vehiculo: {vehiculo[2]}, combustible: {vehiculo[3]}")

    # Pedir al usuario los nuevos valores, permitiendo dejar en blanco para no cambiar
    nuevo_matricula = input("Nueva matricula del vehiculo (deja en blanco para no cambiar): ")
    nuevo_tipo_vehiculo = input("Nuevo tipo de vehiculo (articulado, standard, micro) (deja en blanco para no cambiar): ")
    nuevo_combustible = input("Nuevo tipo combustible (deja en blanco para no cambiar): ")

    # Preparar los nuevos valores, usando los actuales si se deja el campo en blanco
    matricula_final = nuevo_matricula if nuevo_matricula.strip() != "" else vehiculo[1]
    tipo_final = nuevo_tipo_vehiculo if nuevo_tipo_vehiculo.strip() != "" else vehiculo[2]
    combustible_final = nuevo_combustible if nuevo_combustible.strip() != "" else vehiculo[3]

    # Actualizar el vehiculo en la base de datos
    cursor.execute("UPDATE vehiculos SET matricula_vehiculo = ?, tipo_vehiculo = ?, combustible = ? WHERE id_vehiculo = ?", 
               (matricula_final, tipo_final, combustible_final, id_vehiculo))
    conexion.commit()
    print("Vehiculo actualizado exitosamente.")

    conexion.close()


# Listar los vehiculos
def listar_vehiculos():
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM vehiculos')
    vehiculos = cursor.fetchall()

    # Creando la tabla y asignando los nombres de las columnas con colores
    tabla = PrettyTable()
    tabla.field_names = [f"{Color.CYAN}ID{Color.RESET}",
                         f"{Color.CYAN}Matrícula{Color.RESET}",
                         f"{Color.CYAN}Tipo de Vehículo{Color.RESET}",
                         f"{Color.CYAN}Combustible{Color.RESET}"]

    if not vehiculos:
        print("No hay vehículos registrados.")
    else:
        print("\nLista de vehículos:")
        for vehiculo in vehiculos:
            tabla.add_row([
                f"{Color.YELLOW}{vehiculo[0]}{Color.RESET}",
                f"{Color.WHITE}{vehiculo[1]}{Color.RESET}",
                f"{Color.RED}{vehiculo[2]}{Color.RESET}",
                f"{Color.BLUE}{vehiculo[3]}{Color.RESET}"
            ])
        
        print(tabla)
                
    conexion.close()
