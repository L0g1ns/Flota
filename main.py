from conductores import *
from vehiculos import *
from lineas import *
from nombramientos import *
from sumar_horas_dias_conductores import *
from dias_de_trabajo_seguido import *
from exportar_importar import *
from db import crear_conexion_bd
from colorama import Fore, Style, init

import os

def limpiar_pantalla():
    # Comando dependiendo del sistema operativo
    comando = 'cls' if os.name == 'nt' else 'clear'
    os.system(comando)

# Luego, simplemente llama a esta función cuando necesites limpiar la pantalla
limpiar_pantalla()

def menu_conductores():
    while True:
        print(Fore.CYAN + "\n-- Menú de Conductores --")
        print(Fore.GREEN + "[1] Agregar conductor")
        print(Fore.GREEN + "[2] Listar conductores")
        print(Fore.YELLOW + "[3] Eliminar conductor")
        print(Fore.YELLOW + "[4] Editar conductor")
        print(Fore.MAGENTA + "[5] Volver al menú principal")
        opcion = input(Fore.BLUE + "Elige una opción: ")

        if opcion == "1":
            limpiar_pantalla()
            agregar_conductor()
        elif opcion == "2":
            limpiar_pantalla()
            listar_conductores()
        elif opcion == "3":
            limpiar_pantalla()
            eliminar_conductor()
        elif opcion == "4":
            limpiar_pantalla()
            editar_conductor()
        elif opcion == "5":
            limpiar_pantalla()
            break
        else:
            print(Fore.RED + "Opción no válida. Por favor, intenta de nuevo.")


def menu_vehiculos():
    while True:
        print(Fore.CYAN + "\n-- Menú de Vehículos --")
        print(Fore.GREEN + "[1] Agregar vehiculo")
        print(Fore.GREEN + "[2] Listar vehiculos")
        print(Fore.YELLOW + "[3] Eliminar vehiculo")
        print(Fore.YELLOW + "[4] Editar vehiculo")
        print(Fore.MAGENTA + "[5] Volver al menú principal")
        opcion = input(Fore.BLUE + "Elige una opción: ")

        if opcion == "1":
            limpiar_pantalla()
            agregar_vehiculo()
        elif opcion == "2":
            limpiar_pantalla()
            listar_vehiculos()
        elif opcion == "3":
            limpiar_pantalla()
            eliminar_vehiculo()
        elif opcion == "4":
            limpiar_pantalla()
            editar_vehiculo()
        elif opcion == "5":
            limpiar_pantalla()
            break
        else:
            print(Fore.RED + "Opción no válida. Por favor, intenta de nuevo.")


def menu_lineas():
    while True:
        print(Fore.CYAN + "\n-- Menú de Líneas --")
        print(Fore.GREEN + "[1] Agregar Línea")
        print(Fore.GREEN + "[2] Listar Líneas")
        print(Fore.YELLOW + "[3] Eliminar Línea")
        print(Fore.YELLOW + "[4] Editar Línea")
        print(Fore.MAGENTA +"[5] Volver al menú principal")
        opcion = input(Fore.BLUE + "Elige una opción: ")

        if opcion == "1":
            limpiar_pantalla()
            agregar_linea()
        elif opcion == "2":
            limpiar_pantalla()
            listar_lineas()
        elif opcion == "3":
            limpiar_pantalla()
            eliminar_linea()
        elif opcion == "4":
            limpiar_pantalla()
            editar_linea()
        elif opcion == "5":
            limpiar_pantalla()
            break
        else:
            print(Fore.RED + "Opción no válida. Por favor, intenta de nuevo.")


def menu_nombramientos():
    while True:
        print(Fore.CYAN + "\n-- Menú de Nombramientos --")
        print(Fore.GREEN + "[1] Agregar Nombramiento")
        print(Fore.GREEN + "[2] Listar Nombramientos por Fecha")
        print(Fore.WHITE + "[3] Editar Nombramiento")
        print(Fore.YELLOW + "[4] Eliminar Nombramiento por conductor")
        print(Fore.YELLOW + "[5] Eliminar Nombramiento por fecha")
        print(Fore.YELLOW + "[6] Nombramientos por Conductor")
        print(Fore.MAGENTA + "[7] Volver al menú principal")
        opcion = input(Fore.BLUE + "Elige una opción: ")

        if opcion == "1":
            limpiar_pantalla()
            agregar_nombramiento()
        elif opcion == "2":
            limpiar_pantalla()
            listar_nombramientos_por_fecha()
        elif opcion == "3":
            limpiar_pantalla()
            editar_nombramiento()
        elif opcion == "4":
            limpiar_pantalla()
            eliminar_nombramiento()
        elif opcion == "5":
            limpiar_pantalla()
            eliminar_nombramientos_por_fecha()
        elif opcion == "6":
            limpiar_pantalla()
            listar_nombramientos_por_conductor()
        elif opcion == "7":
            limpiar_pantalla()
            break
        else:
            print(Fore.RED + "Opción no válida. Por favor, intenta de nuevo.")


def menu_dias_de_trabajo_seguido():
    while True:
        print(Fore.CYAN + "\n-- Menú de Dias seguidos de trabajo --")
        print(Fore.GREEN + "[1] Analizar días consecutivos")
        print(Fore.MAGENTA + "[2] Volver al menú principal")
        opcion = input(Fore.BLUE + "Elige una opción: ")

        if opcion == "1":
            limpiar_pantalla()
            # Primero obtenemos las fechas de trabajo para todos los conductores
            fechas_por_conductor = obtener_fechas_trabajo_conductor()
            # Luego, pasamos esas fechas a la función para analizar
            analizar_dias_consecutivos(fechas_por_conductor)
        elif opcion == "2":
            limpiar_pantalla()
            break
        else:
            print(Fore.RED + "Opción no válida. Por favor, intenta de nuevo.")


def menu_exportar_importar():
    while True:
        print(Fore.CYAN + "\n-- Menú de Dias seguidos de trabajo --")
        print(Fore.GREEN + "[1] Importar")
        print(Fore.MAGENTA + "[2] Exportar")
        print(Fore.MAGENTA + "[3] Volver al menú principal")
        opcion = input(Fore.BLUE + "Elige una opción: ")

        if opcion == "1":
            limpiar_pantalla()
            importar_datos_excel()
        elif opcion == "2":
            limpiar_pantalla()
            exportar_datos_excel()
        elif opcion == "3":
            limpiar_pantalla()
            break
        else:
            print(Fore.RED + "Opción no válida. Por favor, intenta de nuevo.")

        

def main():
    while True:
        

        print(Fore.CYAN + "\n-- Menú Principal --")
        print(Fore.WHITE + "[1] Conductores")
        print(Fore.WHITE + "[2] Vehículos")
        print(Fore.WHITE + "[3] Líneas")
        print(Fore.WHITE + "[4] Nombramientos")  # Añadir opción para Nombramientos
        print(Fore.WHITE + "[5] Suma Días y horas totales de trabajo")  # Añadir opción para Nombramientos
        print(Fore.WHITE + "[6] Menú Días seguidos de trabajo")
        print(Fore.WHITE + "[7] Menú Importar/Exportar")  
        print(Fore.MAGENTA + "[8] Salir")
        opcion = input(Fore.BLUE + "Elige una opción: ")

        if opcion == "1":
            limpiar_pantalla()
            menu_conductores()
        elif opcion == "2":
            limpiar_pantalla()
            menu_vehiculos()
        elif opcion == "3":
            limpiar_pantalla()
            menu_lineas()
        elif opcion == "4":  # Llama al menú de Nombramientos
            limpiar_pantalla()
            menu_nombramientos()
        elif opcion == "5":
            limpiar_pantalla()
            sumar_horas_dias_conductores()
        elif opcion == "6":
            limpiar_pantalla()
            menu_dias_de_trabajo_seguido()
        elif opcion == "7": 
            limpiar_pantalla()
            menu_exportar_importar()
        elif opcion == "8":
            limpiar_pantalla()
            print(Fore.LIGHTYELLOW_EX + "Saliendo del programa...")
            break
        else:
            print(Fore.RED + " Opción no válida. Por favor, intenta de nuevo.")

if __name__ == '__main__':
    crear_conexion_bd()
    main()


