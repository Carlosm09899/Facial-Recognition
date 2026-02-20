import cv2
import face_recognition
import sqlite3
import numpy as np
import io
from scipy.spatial import distance as dist

# ==========================================
# CONFIGURACIÓN DE SEGURIDAD (Liveness)
# ==========================================
EYE_AR_THRESH = 0.20        # Umbral para detectar ojo cerrado
EYE_AR_CONSEC_FRAMES = 3    # Frames seguidos para validar un parpadeo
COUNTER = 0
PARPADEO_DETECTADO = False

def eye_aspect_ratio(eye):
    """Calcula la relación de aspecto del ojo para detectar parpadeo"""
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# ==========================================
# GESTIÓN DE BASE DE DATOS
# ==========================================
def convertir_array(blob):
    """Convierte el BLOB de SQLite a un array de NumPy utilizable"""
    out = io.BytesIO(blob)
    out.seek(0)
    # Forzamos float64 para evitar errores de resta en np.linalg.norm
    return np.load(out).astype(np.float64)

def registrar_acceso_en_db(nombre):
    """Guarda el log de acceso en la tabla de historial"""
    try:
        conn = sqlite3.connect('usuarios_biometria.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO historial_accesos (nombre) VALUES (?)", (nombre,))
        conn.commit()
        conn.close()
        print(f"LOG: Acceso guardado para {nombre}")
    except Exception as e:
        print(f"Error al escribir historial: {e}")

# ==========================================
# NÚCLEO DEL SISTEMA
# ==========================================
def iniciar_sistema():
    global COUNTER, PARPADEO_DETECTADO
    
    # Cargar usuarios desde SQLite
    conn = sqlite3.connect('usuarios_biometria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, encoding FROM rostros")
    filas = cursor.fetchall()
    
    nombres_db = []
    encodings_db = []
    
    for fila in filas:
        nombres_db.append(fila[0])
        encodings_db.append(convertir_array(fila[1]))
    
    conn.close()

    if not nombres_db:
        print("Error: La base de datos está vacía. Registra usuarios primero.")
        return

    # Convertir a array de NumPy para cálculos matemáticos rápidos
    encodings_db = np.array(encodings_db)
    
    cam = cv2.VideoCapture(0)
    ultimo_reconocido = ""
    print("Sistema de Seguridad ITSOEH Activo. Esperando parpadeo...")

    while True:
        ok, frame = cam.read()
        if not ok: break

        # Reducir imagen para mejorar el rendimiento del i5 11400H
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        small_frame = cv2.resize(frame_rgb, (0, 0), fx=0.25, fy=0.25)
        
        # 1. Buscar landmarks faciales para el parpadeo
        face_landmarks_list = face_recognition.face_landmarks(small_frame)

        for face_landmarks in face_landmarks_list:
            leftEye = face_landmarks['left_eye']
            rightEye = face_landmarks['right_eye']
            
            ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0

            if ear < EYE_AR_THRESH:
                COUNTER += 1
            else:
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    PARPADEO_DETECTADO = True
                COUNTER = 0

        # 2. Solo si se detectó vida, procedemos al reconocimiento
        if PARPADEO_DETECTADO:
            locs = face_recognition.face_locations(small_frame)
            encs = face_recognition.face_encodings(small_frame, locs)

            for encoding, location in zip(encs, locs):
                # Comparación matemática
                distancias = face_recognition.face_distance(encodings_db, encoding)
                nombre = "DESCONOCIDO"

                if len(distancias) > 0:
                    idx = np.argmin(distancias)
                    if distancias[idx] < 0.5:
                        nombre = nombres_db[idx]
                        if nombre != ultimo_reconocido:
                            registrar_acceso_en_db(nombre)
                            ultimo_reconocido = nombre

                # Dibujar resultados (escalando de nuevo a tamaño original)
                top, right, bottom, left = [v * 4 for v in location]
                color = (0, 255, 0)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, f"{nombre} - REAL", (left, top - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # Resetear estado si ya no hay nadie frente a la cámara
            if not locs:
                PARPADEO_DETECTADO = False
        else:
            # Estado de espera (Antispoofing activo)
            cv2.putText(frame, "VALIDANDO: PARPADEE PARA ENTRAR", (30, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Acceso Biometrico Seguro - TICs", frame)
        
        if cv2.waitKey(1) == 27: # Tecla ESC para salir
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_sistema()