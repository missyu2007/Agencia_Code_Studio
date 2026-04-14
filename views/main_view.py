import tkinter as tk
from tkinter import messagebox
from views.client_view import abrir_ventana_clientes
from views.collaborator_view import abrir_ventana_colaboradores
from views.project_view import abrir_ventana_proyectos
from views.task_view import abrir_ventana_tareas
from views.assignment_view import abrir_ventana_asignaciones
from views.user_view import abrir_ventana_usuarios
from views.report_view import abrir_ventana_reportes


def abrir_ventana_principal(usuario_autenticado):
    ventana_principal = tk.Tk()
    ventana_principal.title("AgenciaCode Studio - Sistema de Gestion de Proyectos")
    ventana_principal.geometry("700x460")
    ventana_principal.resizable(False, False)

    nombre_completo_usuario = (
        f"{usuario_autenticado['nombre_colaborador']} "
        f"{usuario_autenticado['apellido_colaborador']}"
    )
    rol_actual = usuario_autenticado["rol_sistema"]

    def confirmar_cierre_sesion():
        confirmar = messagebox.askyesno("Cerrar sesion",
                                        "¿Esta seguro de que desea cerrar la sesion?",
                                        parent=ventana_principal)
        if confirmar:
            ventana_principal.destroy()

    # --- Encabezado ---
    marco_encabezado = tk.Frame(ventana_principal, relief="groove", bd=1, pady=8)
    marco_encabezado.pack(fill="x", padx=10, pady=(10, 5))

    tk.Label(marco_encabezado, text="AgenciaCode Studio",
             font=("Arial", 16, "bold")).pack()
    tk.Label(marco_encabezado,
             text=f"Sistema de Gestion de Proyectos de Desarrollo",
             font=("Arial", 10)).pack()
    tk.Label(marco_encabezado,
             text=f"Usuario: {nombre_completo_usuario}  |  Rol: {rol_actual}",
             font=("Arial", 9)).pack(pady=(4, 0))

    # --- Menu de modulos ---
    marco_menu = tk.LabelFrame(ventana_principal, text="Modulos del Sistema", padx=20, pady=15)
    marco_menu.pack(fill="both", expand=True, padx=10, pady=5)

    def crear_boton_modulo(marco_padre, texto_boton, comando, fila, columna):
        tk.Button(
            marco_padre,
            text=texto_boton,
            width=28,
            height=2,
            command=comando
        ).grid(row=fila, column=columna, padx=8, pady=6)

    crear_boton_modulo(marco_menu, "Gestion de Clientes",
                       lambda: abrir_ventana_clientes(ventana_principal), 0, 0)

    crear_boton_modulo(marco_menu, "Gestion de Colaboradores",
                       lambda: abrir_ventana_colaboradores(ventana_principal), 0, 1)

    crear_boton_modulo(marco_menu, "Gestion de Proyectos",
                       lambda: abrir_ventana_proyectos(ventana_principal), 1, 0)

    crear_boton_modulo(marco_menu, "Gestion de Tareas",
                       lambda: abrir_ventana_tareas(ventana_principal), 1, 1)

    crear_boton_modulo(marco_menu, "Asignaciones (Colaboradores a Proyectos)",
                       lambda: abrir_ventana_asignaciones(ventana_principal), 2, 0)

    crear_boton_modulo(marco_menu, "Consultas y Reportes",
                       lambda: abrir_ventana_reportes(ventana_principal), 2, 1)

    if rol_actual == "Admin":
        crear_boton_modulo(marco_menu, "Gestion de Usuarios del Sistema",
                           lambda: abrir_ventana_usuarios(ventana_principal), 3, 0)

    # --- Pie ---
    marco_pie = tk.Frame(ventana_principal)
    marco_pie.pack(fill="x", padx=10, pady=(0, 10))
    tk.Button(marco_pie, text="Cerrar Sesion", width=18,
              command=confirmar_cierre_sesion).pack(side="right")

    ventana_principal.protocol("WM_DELETE_WINDOW", confirmar_cierre_sesion)
    ventana_principal.mainloop()
