import sqlite3
from datetime import datetime

def consultar_historial():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('usuarios_biometria.db')
        cursor = conn.cursor()

        # Consultar los últimos 20 registros de acceso
        print("\n--- HISTORIAL DE ACCESOS AL LABORATORIO ---")
        print(f"{'ID':<5} | {'Usuario':<15} | {'Fecha y Hora':<20} | {'Estatus':<10}")
        print("-" * 60)

        cursor.execute("SELECT id, nombre, fecha_hora, estatus FROM historial_accesos ORDER BY fecha_hora DESC LIMIT 20")
        filas = cursor.fetchall()

        if not filas:
            print("No hay registros de acceso aún.")
        else:
            for fila in filas:
                # Formatear la fecha para que se vea mejor
                # fila[2] suele venir como '2026-02-19 22:15:00'
                id_log, nombre, fecha, estatus = fila
                print(f"{id_log:<5} | {nombre:<15} | {fecha:<20} | {estatus:<10}")

        conn.close()
        print("-" * 60 + "\n")

    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")

if __name__ == "__main__":
    consultar_historial()