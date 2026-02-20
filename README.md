# 🛡️ Sistema de Acceso Biométrico con Detección de Vida (Liveness Detection)

Este proyecto es un sistema de seguridad biométrica avanzado desarrollado en Python. Utiliza reconocimiento facial y un algoritmo de **detección de parpadeo (Antispoofing)** para prevenir el acceso no autorizado mediante el uso de fotografías o videos de usuarios registrados.

## 🚀 Características del Proyecto
- **Reconocimiento Facial**: Basado en la librería `face_recognition` y modelos de dlib con alta precisión.
- **Detección de Vida (Liveness Detection)**: Cálculo de la relación de aspecto del ojo (**EAR - Eye Aspect Ratio**) para validar que el usuario es una persona real.
- **Persistencia en SQLite**: Almacenamiento seguro de encodings faciales y un historial completo de accesos.
- **Interfaz Gráfica (GUI)**: Panel de control centralizado desarrollado en Tkinter.
- **Optimización de Hardware**: Procesamiento escalado para ejecución fluida en equipos con procesadores modernos (como Intel i5 11400H).

## 🛠️ Tecnologías y Librerías
- **Lenguaje**: Python 3.11+
- **Librerías principales**: OpenCV, face_recognition, NumPy, SciPy.
- **Base de Datos**: SQLite3.
- **Entorno**: Visual Studio Code.

---

## ⚙️ Instrucciones de Instalación (Paso a Paso)

Sigue este orden estrictamente para evitar errores de compilación en Windows:

### 1. Requisitos Previos del Sistema
Antes de tocar el código, tu PC debe tener:
1. **Visual Studio Build Tools**: Con la carga de trabajo **"Desarrollo para el escritorio con C++"**.
2. **CMake**: Versión oficial instalada y agregada al PATH del sistema.

### 2. Configuración del Proyecto
Abre la carpeta del proyecto en VS Code y ejecuta en la terminal:

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
.\venv\Scripts\activate

# Instalar dependencias
pip install cmake
pip install dlib
pip install face-recognition opencv-python numpy scipy
```

### 3. Preparación de la Base de Datos
Debes crear la estructura de tablas antes de iniciar el sistema por primera vez:

```
python init_db.py
```
## 🖥️ Modo de Uso (Paso a Paso)
Para una experiencia completa y profesional, utiliza el panel de control centralizado:
```
python app_biometrica.py
```


## 4. Flujo de Trabajo Recomendado:
Registro de Usuario: Haz clic en el botón "REGISTRAR USUARIO". Se abrirá la cámara; ingresa tu nombre en la terminal y presiona la tecla 'S' cuando tu rostro esté encuadrado para guardar tu firma biométrica en la base de datos.

Monitor de Acceso: Haz clic en "INICIAR MONITOR". El sistema mostrará un aviso en color rojo: "VALIDANDO: PARPADEE PARA ENTRAR".

Validación (Antispoofing): Parpadea de forma natural frente a la cámara. El algoritmo detectará el movimiento de tus párpados, el recuadro cambiará a VERDE y mostrará tu nombre con la etiqueta "REAL".

Registro de Log: Al ser reconocido, el sistema guardará automáticamente tu entrada en la tabla de historial de SQLite.

Historial: Haz clic en "VER HISTORIAL" para consultar la lista de personas que han accedido con su respectiva fecha y hora.

💡 Nota Importante: Para cerrar las ventanas de la cámara de forma segura, presiona la tecla ESC.

### Desarrollado por: Carlos Granados Montoya

### Institución: Tecnológico Superior del Occidente del Estado de Hidalgo (ITSOEH)

### Carrera: Ingeniería en Tecnologías de la Información y Comunicaciones