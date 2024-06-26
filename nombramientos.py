import sqlite3
from db import crear_conexion_bd
from conductores import *
from datetime import datetime
from colorama import Fore, Style, init
from prettytable import PrettyTable

import sqlite3

init(autoreset=True)

def crear_conexion_bd():
    try:
        return sqlite3.connect('flota.db')
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None



def solicitar_fecha():
    # Solicita al usuario una fecha y valida su formato.
    formato_fecha = "%Y-%m-%d"
    while True:
        fecha = input("Introduce la fecha (YYYY-MM-DD): ")
        try:
            datetime.strptime(fecha, formato_fecha)
            return fecha
        except ValueError:
            print("Formato de fecha incorrecto, sigue el formato YYYY-MM-DD.")

def elegir_conductor(fecha):
    conexion = crear_conexion_bd()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT id_driver, name_driver FROM conductores WHERE id_driver NOT IN (
            SELECT id_conductor FROM nombramientos WHERE fecha = ?
        )
    ''', (fecha,))
    conductores = cursor.fetchall()
    conexion.close()

    if not conductores:
        print(f"{Fore.RED}No hay conductores disponibles para esta fecha.{Style.RESET_ALL}")
        return None

    tabla_conductores = PrettyTable()
    tabla_conductores.field_names = [f"{Fore.YELLOW}ID Conductor{Style.RESET_ALL}", f"{Fore.WHITE}Nombre Conductor{Style.RESET_ALL}"]
    for conductor in conductores:
        tabla_conductores.add_row([f"{Fore.YELLOW}{conductor[0]}{Style.RESET_ALL}", f"{Fore.WHITE}{conductor[1]}{Style.RESET_ALL}"])

    print(tabla_conductores)

    conductores_dict = {str(conductor[0]): conductor[1] for conductor in conductores}

    id_conductor = None
    while id_conductor not in conductores_dict:
        id_conductor = input("Escribe el ID del conductor: ")
        if id_conductor not in conductores_dict:
            print(f"{Fore.RED}Selecciona un ID válido de la lista.{Style.RESET_ALL}")
    return id_conductor


def elegir_vehiculo(fecha):
    conexion = crear_conexion_bd()
    cursor = conexion.cursor()
    # Asegúrate de ajustar la consulta para incluir el tipo de vehículo de tu esquema de base de datos
    cursor.execute('''
        SELECT id_vehiculo, matricula_vehiculo, tipo_vehiculo FROM vehiculos WHERE id_vehiculo NOT IN (
            SELECT id_vehiculo FROM nombramientos WHERE fecha = ?
        )
    ''', (fecha,))
    vehiculos = cursor.fetchall()
    conexion.close()

    if not vehiculos:
        print(f"{Fore.RED}No hay vehículos disponibles para esta fecha.{Style.RESET_ALL}")
        return None

    tabla_vehiculos = PrettyTable()
    tabla_vehiculos.field_names = [f"{Fore.YELLOW}ID Vehículo{Style.RESET_ALL}", 
                                   f"{Fore.WHITE}Matrícula{Style.RESET_ALL}", 
                                   f"{Fore.CYAN}Tipo{Style.RESET_ALL}"]
    for vehiculo in vehiculos:
        tabla_vehiculos.add_row([f"{Fore.YELLOW}{vehiculo[0]}{Style.RESET_ALL}", 
                                 f"{Fore.WHITE}{vehiculo[1]}{Style.RESET_ALL}",
                                 f"{Fore.CYAN}{vehiculo[2]}{Style.RESET_ALL}"])

    print(tabla_vehiculos)

    vehiculos_dict = {str(vehiculo[0]): (vehiculo[1], vehiculo[2]) for vehiculo in vehiculos}

    id_vehiculo = None
    while id_vehiculo not in vehiculos_dict:
        id_vehiculo = input(f"{Fore.GREEN}Escribe el ID del vehículo: {Style.RESET_ALL}")
        if id_vehiculo not in vehiculos_dict:
            print(f"{Fore.RED}Selecciona un ID válido de la lista.{Style.RESET_ALL}")
    return id_vehiculo


def elegir_linea(fecha):
    conexion = crear_conexion_bd()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT id_linea, nombre_linea FROM lineas WHERE id_linea NOT IN (
            SELECT id_linea FROM nombramientos WHERE fecha = ?
        )
    ''', (fecha,))
    lineas = cursor.fetchall()
    conexion.close()

    if not lineas:
        print(f"{Fore.RED}No hay líneas disponibles para esta fecha.{Style.RESET_ALL}")
        return None

    tabla_lineas = PrettyTable()
    tabla_lineas.field_names = [f"{Fore.YELLOW}ID Línea{Style.RESET_ALL}", f"{Fore.WHITE}Nombre Línea{Style.RESET_ALL}"]
    for linea in lineas:
        tabla_lineas.add_row([f"{Fore.YELLOW}{linea[0]}{Style.RESET_ALL}", f"{Fore.WHITE}{linea[1]}{Style.RESET_ALL}"])

    print(tabla_lineas)

    lineas_dict = {str(linea[0]): linea[1] for linea in lineas}

    id_linea = None
    while id_linea not in lineas_dict:
        id_linea = input(f"{Fore.GREEN}Escribe el ID de la línea: {Style.RESET_ALL}")
        if id_linea not in lineas_dict:
            print(f"{Fore.RED}Selecciona un ID válido de la lista.{Style.RESET_ALL}")
    return id_linea

def agregar_nombramiento():
    fecha = solicitar_fecha()
    id_conductor = elegir_conductor(fecha)
    id_vehiculo = elegir_vehiculo(fecha)
    id_linea = elegir_linea(fecha)
    tipo_turno = input("Tipo de turno: ")
    servicio = input("Servicio: ")
    horas = input("Cantidad de horas: ")

    conexion = crear_conexion_bd()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO nombramientos (fecha, id_conductor, id_vehiculo, id_linea, tipo_turno, servicio, horas)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (fecha, id_conductor, id_vehiculo, id_linea, tipo_turno, servicio, horas))
    conexion.commit()
    id_nombramiento = cursor.lastrowid
    conexion.close()
    print(f"Nombramiento añadido exitosamente con ID: {id_nombramiento}.")


def editar_nombramiento():
    listar_nombramientos_por_fecha()
    id_nombramiento = input("Escribe el ID del nombramiento que deseas editar: ")
    
    # Obtener los detalles actuales del nombramiento para poder mantener los valores en caso de que el usuario no quiera modificar alguno
    conexion = crear_conexion_bd()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT id_vehiculo, id_linea, tipo_turno, servicio, horas
        FROM nombramientos
        WHERE id_nombramiento = ?
    ''', (id_nombramiento,))
    nombramiento_actual = cursor.fetchone()
    if nombramiento_actual is None:
        print("No se encontró el nombramiento.")
        return
    
    # Asignar valores actuales a variables para posibles modificaciones
    id_vehiculo_actual, id_linea_actual, tipo_turno_actual, servicio_actual, horas_actual = nombramiento_actual
    
    # Solicitar nuevos valores, permitir dejar en blanco para conservar el valor actual
    print("Deja en blanco cualquier campo que no desees modificar.")
    
    nuevo_id_vehiculo = input(f"Nuevo ID de vehículo (Actual: {id_vehiculo_actual}): ") or id_vehiculo_actual
    nuevo_id_linea = input(f"Nuevo ID de línea (Actual: {id_linea_actual}): ") or id_linea_actual
    nuevo_tipo_turno = input(f"Nuevo tipo de turno (Actual: {tipo_turno_actual}): ") or tipo_turno_actual
    nuevo_servicio = input(f"Nuevo servicio (Actual: {servicio_actual}): ") or servicio_actual
    nuevas_horas = input(f"Nuevas horas (Actual: {horas_actual}): ") or horas_actual
    
    # Actualizar el nombramiento en la base de datos solo con los campos modificados
    cursor.execute('''
        UPDATE nombramientos
        SET id_vehiculo = ?, id_linea = ?, tipo_turno = ?, servicio = ?, horas = ?
        WHERE id_nombramiento = ?
    ''', (nuevo_id_vehiculo, nuevo_id_linea, nuevo_tipo_turno, nuevo_servicio, nuevas_horas, id_nombramiento))
    conexion.commit()
    conexion.close()
    print("Nombramiento editado exitosamente.")


def eliminar_nombramiento():
    fecha = solicitar_fecha()  # Solicita al usuario la fecha para la cual desea ver los nombramientos
    print("Listando nombramientos para la fecha seleccionada:")
    listar_nombramientos_por_fecha(fecha)  # Lista los nombramientos para esa fecha

    id_nombramiento = input("Escribe el ID del nombramiento que deseas eliminar: ")  # Solicita el ID del nombramiento a eliminar
    
    # Confirmación de la acción por parte del usuario
    confirmacion = input("¿Estás seguro de que deseas eliminar este nombramiento? (s/n): ")
    if confirmacion.lower() == 's':
        conexion = crear_conexion_bd()
        cursor = conexion.cursor()
        try:
            cursor.execute('DELETE FROM nombramientos WHERE id_nombramiento = ?', (id_nombramiento,))
            conexion.commit()
            if cursor.rowcount > 0:
                print("Nombramiento eliminado exitosamente.")
            else:
                print("No se encontró el nombramiento con el ID proporcionado.")
        except sqlite3.Error as e:
            print(f"Ocurrió un error al intentar eliminar el nombramiento: {e}")
        finally:
            conexion.close()
    else:
        print("Operación cancelada.")

def eliminar_nombramientos_por_fecha():
    fecha = solicitar_fecha()  # Solicita al usuario la fecha para la cual desea eliminar los nombramientos
    print(f"Listando nombramientos para la fecha seleccionada: {fecha}")
    listar_nombramientos_por_fecha(fecha)  # Opcional: Listar los nombramientos para confirmación visual del usuario

    # Solicita confirmación del usuario para proceder con la eliminación
    confirmacion = input(f"¿Estás seguro de que deseas eliminar TODOS los nombramientos para {fecha}? (s/n): ")
    if confirmacion.lower() == 's':
        conexion = crear_conexion_bd()
        cursor = conexion.cursor()
        try:
            cursor.execute('DELETE FROM nombramientos WHERE fecha = ?', (fecha,))
            conexion.commit()
            if cursor.rowcount > 0:
                print(f"Todos los nombramientos para {fecha} han sido eliminados exitosamente.")
            else:
                print(f"No se encontraron nombramientos para eliminar en la fecha {fecha}.")
        except sqlite3.Error as e:
            print(f"Ocurrió un error al intentar eliminar los nombramientos: {e}")
        finally:
            conexion.close()
    else:
        print("Operación cancelada.")


def listar_nombramientos_por_fecha(fecha=None):
    if fecha is None:
        fecha = solicitar_fecha()

    conexion = crear_conexion_bd()
    cursor = conexion.cursor()
    cursor.execute('''
    SELECT nombramientos.id_nombramiento, nombramientos.fecha, conductores.id_driver, vehiculos.id_vehiculo, vehiculos.matricula_vehiculo, lineas.id_linea, lineas.nombre_linea,
       nombramientos.tipo_turno, nombramientos.servicio, nombramientos.horas
    FROM nombramientos
    INNER JOIN conductores ON nombramientos.id_conductor = conductores.id_driver
    INNER JOIN vehiculos ON nombramientos.id_vehiculo = vehiculos.id_vehiculo
    INNER JOIN lineas ON nombramientos.id_linea = lineas.id_linea
    WHERE nombramientos.fecha = ?
    ORDER BY nombramientos.fecha;
    ''', (fecha,))
    nombramientos = cursor.fetchall()
    conexion.close()

    if nombramientos:
        tabla = PrettyTable()
        tabla.field_names = ["ID", "Fecha", "ID Conductor", "ID Vehículo", "ID Línea", "Nombre Línea", "Turno", "Servicio", "Horas"]
        for nom in nombramientos:
            tabla.add_row([
                f"{Fore.YELLOW}{nom[0]}{Style.RESET_ALL}",
                f"{Fore.RED}{nom[1]}{Style.RESET_ALL}",
                f"{Fore.YELLOW}{nom[2]}{Style.RESET_ALL}",
                f"{Fore.YELLOW}{nom[3]}{Style.RESET_ALL}",
                f"{Fore.YELLOW}{nom[5]}{Style.RESET_ALL}",
                f"{Fore.WHITE}{nom[6]}{Style.RESET_ALL}",
                f"{Fore.RED}{nom[7]}{Style.RESET_ALL}",
                f"{Fore.RED}{nom[8]}{Style.RESET_ALL}",
                f"{Fore.RED}{nom[9]}{Style.RESET_ALL}"
            ])
        print(f"\nNombramientos para {fecha}:")
        print(tabla)
    else:
        print("No hay nombramientos para esta fecha.")


def listar_nombramientos_por_conductor():
    conexion = crear_conexion_bd()
    if conexion is None:
        print(f"{Fore.RED}No se pudo establecer la conexión con la base de datos.{Style.RESET_ALL}")
        return
    cursor = conexion.cursor()
    
    # Primero, listar todos los conductores para permitir al usuario elegir uno
    cursor.execute("SELECT id_driver, name_driver FROM conductores ORDER BY name_driver")
    conductores = cursor.fetchall()
    listar_conductores()
    
    id_conductor = input(f"{Fore.GREEN}Por favor, introduce el ID del conductor para ver sus nombramientos: {Style.RESET_ALL}")
    
    try:
        consulta = '''
        SELECT nombramientos.id_nombramiento, nombramientos.fecha, nombramientos.tipo_turno, nombramientos.servicio, nombramientos.horas,
               lineas.nombre_linea, vehiculos.id_vehiculo
        FROM nombramientos
        JOIN conductores ON nombramientos.id_conductor = conductores.id_driver
        JOIN vehiculos ON nombramientos.id_vehiculo = vehiculos.id_vehiculo
        JOIN lineas ON nombramientos.id_linea = lineas.id_linea
        WHERE nombramientos.id_conductor = ?
        ORDER BY nombramientos.fecha
        '''
        cursor.execute(consulta, (id_conductor,))
        nombramientos = cursor.fetchall()
        
        if nombramientos:
            tabla_nombramientos = PrettyTable()
            tabla_nombramientos.field_names = ["ID Nombramiento", "Fecha", "Turno", "Servicio", "Horas", "Línea", "ID Vehículo"]
            for nom in nombramientos:
                tabla_nombramientos.add_row([
                    f"{Fore.YELLOW}{nom[0]}{Style.RESET_ALL}",
                    f"{Fore.CYAN}{nom[1]}{Style.RESET_ALL}",
                    f"{Fore.YELLOW}{nom[2]}{Style.RESET_ALL}",
                    f"{Fore.RED}{nom[3]}{Style.RESET_ALL}",
                    f"{Fore.BLUE}{nom[4]}{Style.RESET_ALL}",
                    f"{Fore.WHITE}{nom[5]}{Style.RESET_ALL}",
                    f"{Fore.RED}{nom[6]}{Style.RESET_ALL}"
                ])
            
            print(f"{Fore.GREEN}\nNombramientos para el conductor ID {id_conductor}:{Style.RESET_ALL}")
            print(tabla_nombramientos)
        else:
            print(f"{Fore.RED}No se encontraron nombramientos para el conductor seleccionado.{Style.RESET_ALL}")
            
    except sqlite3.Error as e:
        print(f"{Fore.RED}Error al obtener los nombramientos del conductor: {e}{Style.RESET_ALL}")
        
    finally:
        conexion.close()

