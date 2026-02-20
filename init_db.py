import sqlite3

def crear_base_de_datos():
    # Conectamos (esto crea el archivo .db si no existe)
    conn = sqlite3.connect('usuarios_biometria.db')
    cursor = conn.cursor()

    print("Creando tablas en la base de datos...")

    # 1. Tabla de Usuarios (Biometría)
    # Usamos el tipo 'BLOB' para guardar el array numérico del rostro
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rostros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            encoding BLOB NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Tabla de Historial (Logs de Acceso)
    # Aquí guardaremos quién entró y a qué hora
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial_accesos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estatus TEXT DEFAULT 'EXITOSO'
        )
    ''')

    conn.commit()
    conn.close()
    print("¡Base de datos 'usuarios_biometria.db' creada y configurada con éxito!")

if __name__ == "__main__":
    crear_base_de_datos()