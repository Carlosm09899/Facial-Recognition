import sqlite3

def consultar_historial():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('usuarios_biometria.db')
        cursor = conn.cursor()

        # Encabezado de la tabla
        print("\n--- HISTORIAL DE ACCESOS AL LABORATORIO ---")
        print(f"{'ID':<5} | {'Usuario':<15} | {'Fecha y Hora':<20} | {'Estatus':<10}")
        print("-" * 65)

        # AJUSTE CLAVE: Consultamos 'fecha' en lugar de 'fecha_hora'
        # Y quitamos 'estatus' porque no existe en la tabla actual
        cursor.execute("SELECT id, nombre, fecha FROM historial_accesos ORDER BY id DESC LIMIT 20")
        filas = cursor.fetchall()

        if not filas:
            print("No hay registros de acceso aún.")
        else:
            for fila in filas:
                id_log, nombre, fecha = fila
                # Como solo guardamos accesos exitosos, ponemos el texto fijo
                estatus = "EXITOSO" 
                print(f"{id_log:<5} | {nombre:<15} | {fecha:<20} | {estatus:<10}")

        conn.close()
        print("-" * 65 + "\n")

    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")

if __name__ == "__main__":
    consultar_historial()