from db import crear_conexion_bd
from colorama import Fore, Style, init

import sqlite3

init(autoreset=True)

def crear_conexion_bd():
    conexion = sqlite3.connect('flota.db')
    return conexion

def crear_tabla_asignacion():
    conexion = crear_conexion_bd()
    cursor = conexion.cursor()

    conexion.commit()
    conexion.close()

def agregar_columna_cantidad_buses():
    conexion = crear_conexion_bd()
    cursor = conexion.cursor()

    # Agregar una nueva columna 'cantidad_buses' a la tabla 'lineas'
    # Si la columna ya existe, SQLite ignorará esta instrucción
    cursor.execute('''
        ALTER TABLE lineas
        ADD COLUMN cantidad_buses INTEGER DEFAULT 0
       
    ''')

    conexion.commit()
    conexion.close()

    agregar_columna_cantidad_buses()

# Llama a la función para crear la tabla
crear_tabla_asignacion()

def asignar_bus_a_linea():
    listar_lineas_y_vehiculos()
    id_linea = input("Selecciona el ID de la línea a la que deseas asignar un bus: ")

    conexion = crear_conexion_bd()
    cursor = conexion.cursor()

    # Mostrar buses no asignados
    cursor.execute('SELECT id_vehiculo, matricula_vehiculo, tipo_vehiculo FROM vehiculos WHERE id_linea IS NULL')
    for vehiculo in cursor.fetchall():
        print(f"{Fore.CYAN}ID Vehículo: {Fore.YELLOW}{vehiculo[0]}, {Fore.CYAN}Matrícula: {Fore.RED}{vehiculo[1]}, {Fore.CYAN}Tipo vehiculo: {Fore.RED}{vehiculo[2]}")
    
    id_vehiculo = input("Selecciona el ID del vehículo que deseas asignar a la línea: ")
    
    # Asignar el vehículo a la línea
    cursor.execute('UPDATE vehiculos SET id_linea = ? WHERE id_vehiculo = ?', (id_linea, id_vehiculo))

    conexion.commit()
    conexion.close()

    print(f"Vehículo {id_vehiculo} asignado a la línea {id_linea}.")

def listar_lineas_y_vehiculos():
    conexion = crear_conexion_bd()
    cursor = conexion.cursor()

    cursor.execute('''
        SELECT l.id_linea, l.nombre_linea, COUNT(v.id_vehiculo) AS cantidad_buses, GROUP_CONCAT(v.id_vehiculo, ', ') AS vehiculos_asignados, GROUP_CONCAT(v.tipo_vehiculo, ', ') AS tipo_vehiculo
        FROM lineas l
        LEFT JOIN vehiculos v ON l.id_linea = v.id_linea
        GROUP BY l.id_linea
    ''')

    lineas = cursor.fetchall()

    # Definir los nombres de las cabeceras
    headers = ["ID Línea", "Nombre Línea", "Cantidad de Buses", "IDs Vehículos", "Tipo Vehículo"]

    # Calculando el ancho máximo de cada columna considerando tanto los datos como las cabeceras
    max_id_len = max(max(len(str(linea[0])) for linea in lineas), len(headers[0]))
    max_nombre_len = max(max(len(linea[1]) for linea in lineas), len(headers[1]))
    max_cantidad_buses_len = max(max(len(str(linea[2])) for linea in lineas), len(headers[2]))
    max_vehiculos_asignados_len = max(max(len(linea[3]) if linea[3] else 0 for linea in lineas), len(headers[3]))
    max_tipo_vehiculo_len = max(max(len(linea[4]) if linea[4] else 0 for linea in lineas), len(headers[4]))

    # Imprimir las cabeceras ajustadas
    print(f"{Fore.CYAN}{headers[0].ljust(max_id_len)} | {headers[1].ljust(max_nombre_len)} | {headers[2].ljust(max_cantidad_buses_len)} | {headers[3].ljust(max_vehiculos_asignados_len)} | {headers[4].ljust(max_tipo_vehiculo_len)}{Style.RESET_ALL}")

    # Imprimir los datos ajustados a la anchura calculada
    for linea in lineas:
        id_linea, nombre_linea, cantidad_buses, vehiculos_asignados, tipo_vehiculo = linea
        vehiculos_asignados = vehiculos_asignados if vehiculos_asignados else "N/A"
        tipo_vehiculo = tipo_vehiculo if tipo_vehiculo else "N/A"
        print(f"{Fore.YELLOW}{str(id_linea).ljust(max_id_len)} | {Fore.WHITE}{nombre_linea.ljust(max_nombre_len)} | {Fore.RED}{str(cantidad_buses).ljust(max_cantidad_buses_len)} | {Fore.YELLOW}{vehiculos_asignados.ljust(max_vehiculos_asignados_len)} | {Fore.CYAN}{tipo_vehiculo.ljust(max_tipo_vehiculo_len)}{Style.RESET_ALL}")

    conexion.close()

def quitar_bus_de_linea():
    # Asumimos que listar_lineas_y_vehiculos() imprime las líneas y los vehículos asignados correctamente.
    listar_lineas_y_vehiculos()

    id_linea = input("Selecciona el ID de la línea de la que deseas quitar un bus: ").strip()

    # Asumimos que crear_conexion_bd() establece y devuelve una conexión válida a la base de datos.
    conexion = crear_conexion_bd()
    cursor = conexion.cursor()

    # Intentamos convertir el id_linea a int para asegurarnos que sea numérico y válido.
    try:
        id_linea_int = int(id_linea)
    except ValueError:
        print("El ID de la línea debe ser un número.")
        conexion.close()
        return

    # Verificar si la línea existe antes de intentar quitar un vehículo.
    cursor.execute('SELECT * FROM lineas WHERE id_linea = ?', (id_linea_int,))
    if not cursor.fetchone():
        print("La línea seleccionada no existe.")
        conexion.close()
        return

    # Mostrar buses asignados a la línea seleccionada.
    cursor.execute('SELECT id_vehiculo, matricula_vehiculo, tipo_vehiculo FROM vehiculos WHERE id_linea = ?', (id_linea_int,))
    vehiculos_asignados = cursor.fetchall()
    
    if not vehiculos_asignados:
        print(f"No hay vehículos asignados a la línea {id_linea}.")
        conexion.close()
        return
    
    for vehiculo in vehiculos_asignados:
        print(f"ID Vehículo: {vehiculo[0]}, Matrícula: {vehiculo[1]}, Tipo vehiculo: {vehiculo[2]}")
    
    id_vehiculo = input("Selecciona el ID del vehículo que deseas quitar de la línea: ").strip()

    # Intentamos convertir el id_vehiculo a int para asegurarnos que sea numérico y válido.
    try:
        id_vehiculo_int = int(id_vehiculo)
    except ValueError:
        print("El ID del vehículo debe ser un número.")
        conexion.close()
        return

    # Quitar el vehículo de la línea
    cursor.execute('UPDATE vehiculos SET id_linea = NULL WHERE id_vehiculo = ? AND id_linea = ?', (id_vehiculo_int, id_linea_int))

    if cursor.rowcount == 0:
        print(f"No se pudo quitar el vehículo {id_vehiculo} de la línea {id_linea}. Asegúrate de que el ID del vehículo sea correcto y esté asignado a la línea indicada.")
    else:
        print(f"Vehículo {id_vehiculo} quitado de la línea {id_linea}.")
    
    conexion.commit()
    conexion.close()







def listar_lineas_con_buses():
    conexion = crear_conexion_bd()
    cursor = conexion.cursor()

    cursor.execute('''
        SELECT id_linea, nombre_linea, cantidad_buses, tipo_bus
        FROM lineas
        ORDER BY id_linea
    ''')

    lineas = cursor.fetchall()

    # Nombres de las cabeceras
    headers = ["ID Línea", "Nombre Línea", "Cantidad de Buses", "Tipo Vehículo"]

    # Calcula el ancho máximo para cada columna basado en los datos y los encabezados
    max_id_linea = max(max(len(str(linea[0])) for linea in lineas), len(headers[0])) + 2
    max_nombre_linea = max(max(len(str(linea[1])) for linea in lineas), len(headers[1])) + 2
    max_cantidad_buses = max(max(len(str(linea[2])) for linea in lineas), len(headers[2])) + 2
    max_tipo_vehiculo = max(max(len(str(linea[3])) for linea in lineas), len(headers[3])) + 2

    # Imprime los encabezados con el ancho ajustado
    print(f"{Fore.GREEN}{headers[0]:<{max_id_linea}}| {headers[1]:<{max_nombre_linea}}| {headers[2]:<{max_cantidad_buses}}| {headers[3]:<{max_tipo_vehiculo}}{Style.RESET_ALL}")

    # Imprimir cada línea de datos con el mismo ancho ajustado
    for linea in lineas:
        id_linea, nombre_linea, cantidad_buses, tipo_vehiculo = linea
        print(f"{Fore.YELLOW}{id_linea:<{max_id_linea}}{Fore.GREEN}| {Fore.WHITE}{nombre_linea:<{max_nombre_linea}}{Fore.GREEN}| {Fore.RED}{str(cantidad_buses):<{max_cantidad_buses}}{Fore.GREEN}| {Fore.YELLOW}{tipo_vehiculo:<{max_tipo_vehiculo}}{Style.RESET_ALL}")

    conexion.close()


def asignar_buses_a_linea():
    # Primero, listamos las líneas disponibles
    listar_lineas_con_buses()

    id_linea = input("Introduce el ID de la línea a la que deseas asignar buses: ")
    cantidad_buses = int(input("Introduce la cantidad de buses para asignar a esta línea: "))

    conexion = crear_conexion_bd()
    cursor = conexion.cursor()

    cursor.execute('''
        UPDATE lineas
        SET cantidad_buses = ?
        WHERE id_linea = ?
    ''', (cantidad_buses, id_linea))

    conexion.commit()
    conexion.close()

    print("Cantidad de buses actualizada exitosamente.")
