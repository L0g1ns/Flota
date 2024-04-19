from db import crear_conexion_bd
import pandas as pd
import sqlite3

def exportar_datos_excel(nombre_archivo='datos_flota.xlsx'):
    # Establecer conexión a la base de datos
    conexion = sqlite3.connect('flota.db')
    
    # Utilizar un contexto para manejar el archivo Excel
    with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
        # Definir las tablas para exportar
        tablas = ['conductores', 'vehiculos', 'lineas', 'nombramientos', 'asignacion_buses_lineas']
        
        for tabla in tablas:
            # Leer los datos de cada tabla
            df = pd.read_sql_query(f"SELECT * FROM {tabla}", conexion)
            
            # Escribir los datos en una hoja de Excel
            df.to_excel(writer, sheet_name=tabla, index=False)
    
    # No es necesario llamar a writer.save()
    print(f"Datos exportados exitosamente a '{nombre_archivo}'.")


def importar_o_actualizar(tabla, df, conexion, clave_unica):
    cursor = conexion.cursor()
    for _, fila in df.iterrows():
        # Verificar si el registro ya existe
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM {tabla} WHERE {clave_unica} = ? LIMIT 1)", (fila[clave_unica],))
        existe = cursor.fetchone()[0]
        
        # Preparar la lista de columnas y valores para la sentencia SQL
        columnas = ', '.join(fila.index)
        placeholders = ', '.join(['?'] * len(fila))
        valores = tuple(fila.values)
        
        if existe:
            # Actualizar el registro existente
            updates = ', '.join([f"{col} = ?" for col in fila.index])
            cursor.execute(f"UPDATE {tabla} SET {updates} WHERE {clave_unica} = ?", (*valores, fila[clave_unica]))
        else:
            # Insertar el nuevo registro
            cursor.execute(f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})", valores)

def importar_datos_excel(nombre_archivo='datos_flota.xlsx'):
    conexion = sqlite3.connect('flota.db')

    tablas_clave_unica = {
        'conductores': 'id_driver',
        'vehiculos': 'id_vehiculo',
        'lineas': 'id_linea',
        'nombramientos': 'id_nombramiento',
        'asignacion_buses_lineas': 'id_asignacion'
    }

    for tabla, clave_unica in tablas_clave_unica.items():
        df = pd.read_excel(nombre_archivo, sheet_name=tabla)
        importar_o_actualizar(tabla, df, conexion, clave_unica)
    
    conexion.commit()
    conexion.close()
    print("Datos importados y actualizados exitosamente desde el archivo Excel.")

