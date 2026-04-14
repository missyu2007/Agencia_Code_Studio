import tkinter as tk
from tkinter import ttk, messagebox
from controllers.user_controller import (
    consultar_todos_los_usuarios,
    registrar_nuevo_usuario,
    modificar_usuario_existente,
    eliminar_usuario_existente
)
from controllers.collaborator_controller import consultar_colaboradores_sin_usuario

ROLES_SISTEMA = ["Admin", "Estandar"]


def abrir_ventana_usuarios(ventana_padre):
    ventana_usuarios = tk.Toplevel(ventana_padre)
    ventana_usuarios.title("Gestion de Usuarios del Sistema")
    ventana_usuarios.geometry("860x500")

    id_usuario_seleccionado = {"valor": None}
    lista_colaboradores_sin_usuario = []

    def obtener_colaboradores_disponibles():
        nonlocal lista_colaboradores_sin_usuario
        lista_colaboradores_sin_usuario = consultar_colaboradores_sin_usuario()
        return [f"{c['nombre']} {c['apellido']}" for c in lista_colaboradores_sin_usuario]

    def obtener_id_colaborador():
        indice = combo_colaborador_usuario.current()
        if indice < 0 or indice >= len(lista_colaboradores_sin_usuario):
            return None
        return lista_colaboradores_sin_usuario[indice]["id_colaborador"]

    def cargar_usuarios_en_tabla():
        for fila in tabla_usuarios.get_children():
            tabla_usuarios.delete(fila)
        for usuario in consultar_todos_los_usuarios():
            tabla_usuarios.insert("", "end", values=(
                usuario["id_usuario"],
                usuario["nombre_usuario"],
                usuario["email"],
                usuario["rol_sistema"],
                f"{usuario['nombre_colaborador']} {usuario['apellido_colaborador']}"
            ))

    def limpiar_formulario():
        id_usuario_seleccionado["valor"] = None
        entrada_nombre_usuario.delete(0, tk.END)
        entrada_email_usuario.delete(0, tk.END)
        entrada_contrasena.delete(0, tk.END)
        entrada_confirmar_contrasena.delete(0, tk.END)
        combo_rol_sistema.set(ROLES_SISTEMA[1])
        combo_colaborador_usuario["values"] = obtener_colaboradores_disponibles()
        combo_colaborador_usuario.set("")

    def cargar_datos_en_formulario(evento):
        seleccion = tabla_usuarios.selection()
        if not seleccion:
            return
        valores = tabla_usuarios.item(seleccion[0])["values"]
        id_usuario_seleccionado["valor"] = valores[0]
        entrada_nombre_usuario.delete(0, tk.END)
        entrada_nombre_usuario.insert(0, valores[1])
        entrada_email_usuario.delete(0, tk.END)
        entrada_email_usuario.insert(0, valores[2])
        combo_rol_sistema.set(valores[3])
        entrada_contrasena.delete(0, tk.END)
        entrada_confirmar_contrasena.delete(0, tk.END)

    def guardar_nuevo_usuario():
        exito, mensaje = registrar_nuevo_usuario(
            entrada_nombre_usuario.get().strip(),
            entrada_email_usuario.get().strip(),
            entrada_contrasena.get().strip(),
            entrada_confirmar_contrasena.get().strip(),
            combo_rol_sistema.get(),
            obtener_id_colaborador()
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_usuarios)
            limpiar_formulario()
            cargar_usuarios_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_usuarios)

    def actualizar_usuario_seleccionado():
        if not id_usuario_seleccionado["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione un usuario de la tabla.", parent=ventana_usuarios)
            return
        exito, mensaje = modificar_usuario_existente(
            id_usuario_seleccionado["valor"],
            entrada_nombre_usuario.get().strip(),
            entrada_email_usuario.get().strip(),
            entrada_contrasena.get().strip(),
            entrada_confirmar_contrasena.get().strip(),
            combo_rol_sistema.get()
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_usuarios)
            limpiar_formulario()
            cargar_usuarios_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_usuarios)

    def eliminar_usuario_seleccionado():
        if not id_usuario_seleccionado["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione un usuario de la tabla.", parent=ventana_usuarios)
            return
        confirmar = messagebox.askyesno("Confirmar eliminacion",
                                        "¿Esta seguro de que desea eliminar este usuario?",
                                        parent=ventana_usuarios)
        if not confirmar:
            return
        exito, mensaje = eliminar_usuario_existente(id_usuario_seleccionado["valor"])
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_usuarios)
            limpiar_formulario()
            cargar_usuarios_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_usuarios)

    # --- Interfaz ---
    marco_formulario = tk.LabelFrame(ventana_usuarios, text="Datos del Usuario", padx=10, pady=8)
    marco_formulario.pack(fill="x", padx=10, pady=5)

    tk.Label(marco_formulario, text="Nombre Usuario:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
    entrada_nombre_usuario = tk.Entry(marco_formulario, width=20)
    entrada_nombre_usuario.grid(row=0, column=1, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Email:").grid(row=0, column=2, sticky="e", padx=5, pady=3)
    entrada_email_usuario = tk.Entry(marco_formulario, width=24)
    entrada_email_usuario.grid(row=0, column=3, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Rol:").grid(row=0, column=4, sticky="e", padx=5, pady=3)
    combo_rol_sistema = ttk.Combobox(marco_formulario, values=ROLES_SISTEMA, width=10, state="readonly")
    combo_rol_sistema.set(ROLES_SISTEMA[1])
    combo_rol_sistema.grid(row=0, column=5, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Contrasena:").grid(row=1, column=0, sticky="e", padx=5, pady=3)
    entrada_contrasena = tk.Entry(marco_formulario, width=20, show="*")
    entrada_contrasena.grid(row=1, column=1, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Confirmar Contrasena:").grid(row=1, column=2, sticky="e", padx=5, pady=3)
    entrada_confirmar_contrasena = tk.Entry(marco_formulario, width=20, show="*")
    entrada_confirmar_contrasena.grid(row=1, column=3, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Colaborador:").grid(row=1, column=4, sticky="e", padx=5, pady=3)
    combo_colaborador_usuario = ttk.Combobox(marco_formulario,
                                             values=obtener_colaboradores_disponibles(),
                                             width=20, state="readonly")
    combo_colaborador_usuario.grid(row=1, column=5, sticky="w", pady=3)

    marco_botones = tk.Frame(ventana_usuarios)
    marco_botones.pack(pady=5)
    tk.Button(marco_botones, text="Nuevo", width=12, command=limpiar_formulario).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Guardar", width=12, command=guardar_nuevo_usuario).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Actualizar", width=12, command=actualizar_usuario_seleccionado).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Eliminar", width=12, command=eliminar_usuario_seleccionado).pack(side="left", padx=4)

    marco_tabla = tk.LabelFrame(ventana_usuarios, text="Lista de Usuarios", padx=5, pady=5)
    marco_tabla.pack(fill="both", expand=True, padx=10, pady=5)

    columnas_tabla = ("ID", "Nombre Usuario", "Email", "Rol", "Colaborador Asociado")
    tabla_usuarios = ttk.Treeview(marco_tabla, columns=columnas_tabla, show="headings", height=12)
    anchos = [40, 160, 200, 80, 200]
    for nombre_columna, ancho in zip(columnas_tabla, anchos):
        tabla_usuarios.heading(nombre_columna, text=nombre_columna)
        tabla_usuarios.column(nombre_columna, width=ancho)

    barra_desplazamiento = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla_usuarios.yview)
    tabla_usuarios.configure(yscrollcommand=barra_desplazamiento.set)
    tabla_usuarios.pack(side="left", fill="both", expand=True)
    barra_desplazamiento.pack(side="right", fill="y")

    tabla_usuarios.bind("<<TreeviewSelect>>", cargar_datos_en_formulario)
    cargar_usuarios_en_tabla()
