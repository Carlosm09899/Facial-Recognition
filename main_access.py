import cv2
import face_recognition
import sqlite3
import numpy as np
import io
from scipy.spatial import distance as dist
from datetime import datetime 

# ==========================================
# CONFIGURACIÓN DE OPTIMIZACIÓN
# ==========================================
EYE_AR_THRESH = 0.20
EYE_AR_CONSEC_FRAMES = 3
COUNTER = 0
PARPADEO_DETECTADO = False
PROCESAR_ESTE_FRAME = 0
ULTIMA_UBICACION = [] 
ULTIMO_NOMBRE = "DESCONOCIDO"

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def convertir_array(blob):
    out = io.BytesIO(blob)
    out.seek(0)
    return np.load(out).astype(np.float64)

def registrar_acceso_en_db(nombre):
    """Guarda el log de acceso con la hora local de México"""
    try:
        # Obtenemos la hora exacta de tu MSI
        ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = sqlite3.connect('usuarios_biometria.db')
        cursor = conn.cursor()
        
        # Enviamos 'ahora' manualmente para evitar el horario de Londres (UTC)
        cursor.execute("INSERT INTO historial_accesos (nombre, fecha) VALUES (?, ?)", 
                       (nombre, ahora))
        
        conn.commit()
        conn.close()
        print(f"LOG: Acceso guardado para {nombre} a las {ahora}")
    except Exception as e:
        print(f"Error al escribir historial: {e}")

# ==========================================
# NÚCLEO CON CUADRO SÓLIDO Y AUTO-REPARACIÓN
# ==========================================
def iniciar_sistema():
    global COUNTER, PARPADEO_DETECTADO, PROCESAR_ESTE_FRAME, ULTIMA_UBICACION, ULTIMO_NOMBRE
    
    # --- BLOQUE DE AUTO-REPARACIÓN DE DB ---
    try:
        conn = sqlite3.connect('usuarios_biometria.db')
        cursor = conn.cursor()
        # Intentamos agregar la columna fecha por si no existe
        cursor.execute("ALTER TABLE historial_accesos ADD COLUMN fecha TEXT")
        conn.commit()
        conn.close()
    except:
        pass # Si ya existe, no hace nada

    # Carga de datos
    conn = sqlite3.connect('usuarios_biometria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, encoding FROM rostros")
    filas = cursor.fetchall()
    nombres_db = [f[0] for f in filas]
    encodings_db = [convertir_array(f[1]) for f in filas]
    conn.close()

    cam = cv2.VideoCapture(0)
    ultimo_log = ""

    while True:
        ok, frame = cam.read()
        if not ok: break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # 1. DETECCIÓN DE PARPADEO
        face_landmarks_list = face_recognition.face_landmarks(rgb_small_frame)
        for face_landmarks in face_landmarks_list:
            ear = (eye_aspect_ratio(face_landmarks['left_eye']) + 
                   eye_aspect_ratio(face_landmarks['right_eye'])) / 2.0
            if ear < EYE_AR_THRESH:
                COUNTER += 1
            else:
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    PARPADEO_DETECTADO = True
                COUNTER = 0

        # 2. RECONOCIMIENTO (Lógica de Persistencia)
        if PARPADEO_DETECTADO:
            if PROCESAR_ESTE_FRAME % 3 == 0:
                locs = face_recognition.face_locations(rgb_small_frame, model="hog")
                encs = face_recognition.face_encodings(rgb_small_frame, locs)
                
                if locs:
                    ULTIMA_UBICACION = locs 
                    for encoding in encs:
                        distancias = face_recognition.face_distance(encodings_db, encoding)
                        if len(distancias) > 0:
                            idx = np.argmin(distancias)
                            if distancias[idx] < 0.5:
                                ULTIMO_NOMBRE = nombres_db[idx]
                                if ULTIMO_NOMBRE != ultimo_log:
                                    registrar_acceso_en_db(ULTIMO_NOMBRE)
                                    ultimo_log = ULTIMO_NOMBRE
                            else:
                                ULTIMO_NOMBRE = "DESCONOCIDO"

            for (top, right, bottom, left) in ULTIMA_UBICACION:
                top, right, bottom, left = top*4, right*4, bottom*4, left*4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, f"{ULTIMO_NOMBRE} - REAL", (left, top - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if not face_landmarks_list:
                PARPADEO_DETECTADO = False
                ULTIMA_UBICACION = [] 
        else:
            cv2.putText(frame, "VALIDANDO: PARPADEE PARA ENTRAR", (30, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        PROCESAR_ESTE_FRAME += 1
        cv2.imshow("Acceso ITSOEH - Solido", frame)
        if cv2.waitKey(1) == 27: break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_sistema()