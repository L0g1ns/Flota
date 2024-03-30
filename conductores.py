from db import crear_conexion_bd
from colorama import Fore, Style, init
import sqlite3


def crear_conexion_bd():
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS" conductores (
            id_driver TEXT PRIMARY KEY,
            name_driver TEXT,
            grupo_driver TEXT,
            id_pareja TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

# Agregar un conductor
def agregar_conductor():
    id_driver = input(f"\n[+] Escribe el id del conductor:\n")
    name_driver = input(f"\n[+] Escribe el nombre del conductor:\n")
    grupo_driver = input(f"\n[+] Escribe el tipo de conductor (Fijo, Móvil, Incidencias, Prejubilado):\n")
    id_pareja = input(f"\n[+] Escribe el id pareja si tuviera:\n")

    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO conductores (id_driver, name_driver, grupo_driver, id_pareja)
        VALUES (?, ?, ?, ?)
    ''', (id_driver, name_driver, grupo_driver, id_pareja))
    conexion.commit()
    conexion.close()
    print("Conductor añadido exitosamente.")

# Eliminar un conductor
def eliminar_conductor():
    id_driver = input("\n[+] Escribe el id del conductor a eliminar:\n")
    
    # Conectarse a la base de datos
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()

    # Primero, verificar si el conductor existe
    cursor.execute("SELECT * FROM conductores WHERE id_driver = ?", (id_driver,))
    if cursor.fetchone() is None:
        print("No se encontró un conductor con ese ID.")
    else:
        # Eliminar el conductor
        cursor.execute("DELETE FROM conductores WHERE id_driver = ?", (id_driver,))
        conexion.commit()
        print("Conductor eliminado exitosamente.")

    conexion.close()

def editar_conductor():
    id_driver = input("\n[+] Escribe el ID del conductor a editar:\n")

    # Conectarse a la base de datos
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()

    # Verificar si el conductor existe
    cursor.execute("SELECT * FROM conductores WHERE id_driver = ?", (id_driver,))
    conductor = cursor.fetchone()

    if conductor is None:
        print("No se encontró un conductor con ese ID.")
        conexion.close()
        return

    # Mostrar la información actual del conductor
    print(f"Editando Conductor: ID: {conductor[0]}, Nombre: {conductor[1]}, Tipo: {conductor[2]}, ID Pareja: {conductor[3]}")

    # Pedir al usuario los nuevos valores, permitiendo dejar en blanco para no cambiar
    nuevo_nombre = input("Nuevo nombre del conductor (deja en blanco para no cambiar): ")
    nuevo_grupo = input("Nuevo tipo de conductor (Fijo, Móvil, Incidencias, Prejubilado) (deja en blanco para no cambiar): ")
    nuevo_id_pareja = input("Nuevo ID pareja (deja en blanco para no cambiar): ")

    # Preparar los nuevos valores, usando los actuales si se deja el campo en blanco
    nombre_final = nuevo_nombre if nuevo_nombre.strip() != "" else conductor[1]
    grupo_final = nuevo_grupo if nuevo_grupo.strip() != "" else conductor[2]
    id_pareja_final = nuevo_id_pareja if nuevo_id_pareja.strip() != "" else conductor[3]

    # Actualizar el conductor en la base de datos
    cursor.execute("UPDATE conductores SET name_driver = ?, grupo_driver = ?, id_pareja = ? WHERE id_driver = ?", 
                   (nombre_final, grupo_final, id_pareja_final, id_driver))
    conexion.commit()
    print("Conductor actualizado exitosamente.")

    conexion.close()


# Listar los conductores
def listar_conductores():
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM conductores')
    conductores = cursor.fetchall()

    if not conductores:
        print("No hay conductores registrados.")
    else:
        print("\nLista de conductores:")
        for conductor in conductores:
            print(f"{Fore.CYAN}ID: {Fore.YELLOW}{conductor[0]}, "
                  f"{Fore.CYAN}Nombre: {Fore.WHITE}{conductor[1]}, "
                  f"{Fore.CYAN}Tipo: {Fore.RED}{conductor[2]}, "
                  f"{Fore.CYAN}ID Pareja: {Fore.YELLOW}{conductor[3]}{Style.RESET_ALL}")
                
    conexion.close()

