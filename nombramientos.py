import sqlite3
from db import crear_conexion_bd
from datetime import datetime

def crear_conexion():
    """Crea y devuelve una conexión a la base de datos."""
    return sqlite3.connect('flota.db')


def solicitar_fecha():
    """Solicita al usuario una fecha y valida su formato."""
    formato_fecha = "%Y-%m-%d"
    while True:
        fecha = input("Introduce la fecha (YYYY-MM-DD): ")
        try:
            datetime.strptime(fecha, formato_fecha)
            return fecha
        except ValueError:
            print("Formato de fecha incorrecto, sigue el formato YYYY-MM-DD.")

def elegir_conductor(fecha):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT id_driver, name_driver FROM conductores WHERE id_driver NOT IN (
            SELECT id_conductor FROM nombramientos WHERE fecha = ?
        )
    ''', (fecha,))
    conductores = cursor.fetchall()
    conexion.close()

    conductores_dict = {str(conductor[0]): conductor[1] for conductor in conductores}
    for id_conductor, nombre_conductor in conductores_dict.items():
        print(f"{id_conductor}: {nombre_conductor}")
    
    id_conductor = None
    while id_conductor not in conductores_dict:
        id_conductor = input("Escribe el ID del conductor: ")
        if id_conductor not in conductores_dict:
            print("Selecciona un ID válido de la lista.")
    return id_conductor


def elegir_vehiculo(fecha):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT id_vehiculo, matricula_vehiculo FROM vehiculos WHERE id_vehiculo NOT IN (
            SELECT id_vehiculo FROM nombramientos WHERE fecha = ?
        )
    ''', (fecha,))
    vehiculos = cursor.fetchall()
    conexion.close()

    vehiculos_dict = {str(vehiculo[0]): vehiculo[1] for vehiculo in vehiculos}
    for id_vehiculo, matricula in vehiculos_dict.items():
        print(f"{id_vehiculo}: {matricula}")
    
    id_vehiculo = None
    while id_vehiculo not in vehiculos_dict:
        id_vehiculo = input("Escribe el ID del vehículo: ")
        if id_vehiculo not in vehiculos_dict:
            print("Selecciona un ID válido de la lista.")
    return id_vehiculo


def elegir_linea(fecha):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT id_linea, nombre_linea FROM lineas WHERE id_linea NOT IN (
            SELECT id_linea FROM nombramientos WHERE fecha = ?
        )
    ''', (fecha,))
    lineas = cursor.fetchall()
    conexion.close()

    lineas_dict = {str(linea[0]): linea[1] for linea in lineas}
    for id_linea, nombre_linea in lineas_dict.items():
        print(f"{id_linea}: {nombre_linea}")
    
    id_linea = None
    while id_linea not in lineas_dict:
        id_linea = input("Escribe el ID de la línea: ")
        if id_linea not in lineas_dict:
            print("Selecciona un ID válido de la lista.")
    return id_linea


def agregar_nombramiento():
    fecha = solicitar_fecha()
    id_conductor = elegir_conductor(fecha)
    id_vehiculo = elegir_vehiculo(fecha)
    id_linea = elegir_linea(fecha)
    tipo_turno = input("Tipo de turno: ")
    servicio = input("Servicio: ")
    horas = input("Cantidad de horas: ")

    conexion = crear_conexion()
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
    id_nombramiento = input("Escribe el ID del nombramiento que deseas editar: ")
    
    # Obtener los detalles actuales del nombramiento para poder mantener los valores en caso de que el usuario no quiera modificar alguno
    conexion = crear_conexion()
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
        conexion = crear_conexion()
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
        conexion = crear_conexion()
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

    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
    SELECT nombramientos.id_nombramiento, nombramientos.fecha, conductores.id_driver, conductores.name_driver, vehiculos.id_vehiculo, vehiculos.matricula_vehiculo, lineas.id_linea, lineas.nombre_linea,
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
        print(f"\nNombramientos para {fecha}:")
        for nom in nombramientos:
            print(f"ID Nombramiento: {nom[0]}, Fecha: {nom[0]}, ID Conductor: {nom[1]}, Conductor: {nom[2]}, ID Vehículo: {nom[3]}, Vehículo: {nom[4]}, ID Línea: {nom[5]}, Línea: {nom[6]}, Turno: {nom[7]}, Servicio: {nom[8]}, Horas: {nom[9]}")
    else:
        print("No hay nombramientos para esta fecha.")
