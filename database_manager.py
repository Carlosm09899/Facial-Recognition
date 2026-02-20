import cv2
import face_recognition
import sqlite3
import numpy as np
import io

# Configuración para guardar arrays de numpy en SQLite
def adaptar_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

sqlite3.register_adapter(np.ndarray, adaptar_array)

def registrar_usuario():
    nombre = input("Introduce el nombre del usuario a registrar: ")
    print("Buscando cámara...")
    
    cam = cv2.VideoCapture(0)
    while True:
        ok, frame = cam.read()
        cv2.imshow("Presiona 'S' para capturar o 'ESC' para salir", frame)
        
        key = cv2.waitKey(1)
        if key == ord('s'): # Tecla S para salvar
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb)
            
            if encodings:
                conn = sqlite3.connect('usuarios_biometria.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO rostros (nombre, encoding) VALUES (?, ?)", 
                               (nombre, encodings[0]))
                conn.commit()
                conn.close()
                print(f"¡{nombre} registrado con éxito!")
                break
            else:
                print("No se detectó rostro, intenta de nuevo.")
        elif key == 27:
            break
            
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    registrar_usuario()