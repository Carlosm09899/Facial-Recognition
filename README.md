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