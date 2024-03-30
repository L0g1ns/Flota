
import sqlite3

def crear_conexion_bd():
    conexion = sqlite3.connect('flota.db')
    cursor = conexion.cursor()

    # Crear tabla de conductores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conductores (
            id_driver TEXT PRIMARY KEY,
            name_driver TEXT,
            grupo_driver TEXT,
            id_pareja TEXT
        )
    ''')

    # Crear tabla de vehículos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehiculos (
            id_vehiculo TEXT PRIMARY KEY,
            matricula_vehiculo TEXT,
            tipo_vehiculo TEXT,
            combustible TEXT
        )
    ''')

    # Crear tabla de líneas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lineas (
            id_linea TEXT PRIMARY KEY,
            nombre_linea TEXT,
            tipo_linea TEXT,
            tipo_bus TEXT
        )
    ''')

    # Crear tabla de nombramientos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nombramientos (
            id_nombramiento INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            id_conductor INTEGER NOT NULL,
            id_vehiculo INTEGER NOT NULL,
            id_linea INTEGER NOT NULL,
            tipo_turno TEXT NOT NULL,
            servicio TEXT NOT NULL,
            horas INTEGER NOT NULL,
            FOREIGN KEY (id_conductor) REFERENCES conductores (id_driver),
            FOREIGN KEY (id_vehiculo) REFERENCES vehiculos (id_vehiculo),
            FOREIGN KEY (id_linea) REFERENCES lineas (id_linea)
        )
    ''')

    conexion.commit()
    conexion.close()

    


    

