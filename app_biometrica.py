import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import os

class AppBiometrica:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Acceso Biométrico - ITSOEH")
        self.root.geometry("400x500")
        self.root.configure(bg="#2c3e50")

        # Título principal
        label_titulo = tk.Label(root, text="Panel de Control", font=("Helvetica", 18, "bold"), 
                                fg="white", bg="#2c3e50", pady=20)
        label_titulo.pack()

        # Botón para Iniciar Monitor de Acceso
        btn_monitor = tk.Button(root, text="▶ INICIAR MONITOR", command=self.ejecutar_monitor,
                                font=("Helvetica", 12, "bold"), bg="#27ae60", fg="white", 
                                width=25, height=2, bd=0)
        btn_monitor.pack(pady=10)

        # Botón para Registrar Nuevo Usuario
        btn_registro = tk.Button(root, text="👤 REGISTRAR USUARIO", command=self.ejecutar_registro,
                                 font=("Helvetica", 12, "bold"), bg="#2980b9", fg="white", 
                                 width=25, height=2, bd=0)
        btn_registro.pack(pady=10)

        # Botón para Ver Historial
        btn_historial = tk.Button(root, text="📋 VER HISTORIAL", command=self.ejecutar_historial,
                                  font=("Helvetica", 12, "bold"), bg="#f39c12", fg="white", 
                                  width=25, height=2, bd=0)
        btn_historial.pack(pady=10)

        # Botón para Salir
        btn_salir = tk.Button(root, text="❌ SALIR", command=root.quit,
                              font=("Helvetica", 12, "bold"), bg="#c0392b", fg="white", 
                              width=25, height=2, bd=0)
        btn_salir.pack(pady=30)

        # Pie de página
        label_footer = tk.Label(root, text="Ingeniería en TICs - 2026", font=("Helvetica", 8), 
                                fg="#bdc3c7", bg="#2c3e50")
        label_footer.pack(side="bottom", pady=10)

    def ejecutar_monitor(self):
        try:
            # Ejecuta el script del monitor en un proceso independiente
            subprocess.Popen(["python", "main_access.py"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el monitor: {e}")

    def ejecutar_registro(self):
        try:
            subprocess.Popen(["python", "database_manager.py"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el registro: {e}")

    def ejecutar_historial(self):
        try:
            # Para el historial, abriremos una ventana de texto con los datos
            subprocess.Popen(["python", "ver_historial.py"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el historial: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppBiometrica(root)
    root.mainloop()