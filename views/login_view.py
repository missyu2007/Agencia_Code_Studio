import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import validar_inicio_de_sesion


def abrir_ventana_login():
    ventana_login = tk.Tk()
    ventana_login.title("AgenciaCode Studio - Inicio de Sesion")
    ventana_login.geometry("380x260")
    ventana_login.resizable(False, False)

    datos_usuario_autenticado = {"usuario": None}

    def ejecutar_inicio_de_sesion():
        nombre_usuario = entrada_nombre_usuario.get().strip()
        contrasena = entrada_contrasena.get().strip()
        usuario, mensaje_error = validar_inicio_de_sesion(nombre_usuario, contrasena)
        if usuario:
            datos_usuario_autenticado["usuario"] = usuario
            ventana_login.destroy()
        else:
            messagebox.showerror("Error de acceso", mensaje_error, parent=ventana_login)

    def presionar_enter(evento):
        ejecutar_inicio_de_sesion()

    marco_principal = tk.Frame(ventana_login, padx=30, pady=20)
    marco_principal.pack(expand=True, fill="both")

    tk.Label(marco_principal, text="AgenciaCode Studio", font=("Arial", 14, "bold")).grid(
        row=0, column=0, columnspan=2, pady=(0, 15))

    tk.Label(marco_principal, text="Usuario:").grid(row=1, column=0, sticky="e", pady=5)
    entrada_nombre_usuario = tk.Entry(marco_principal, width=25)
    entrada_nombre_usuario.grid(row=1, column=1, sticky="w", padx=(5, 0), pady=5)

    tk.Label(marco_principal, text="Contrasena:").grid(row=2, column=0, sticky="e", pady=5)
    entrada_contrasena = tk.Entry(marco_principal, width=25, show="*")
    entrada_contrasena.grid(row=2, column=1, sticky="w", padx=(5, 0), pady=5)
    entrada_contrasena.bind("<Return>", presionar_enter)

    tk.Button(marco_principal, text="Iniciar Sesion", width=20,
              command=ejecutar_inicio_de_sesion).grid(row=3, column=0, columnspan=2, pady=15)

    entrada_nombre_usuario.focus()
    ventana_login.mainloop()
    return datos_usuario_autenticado["usuario"]
