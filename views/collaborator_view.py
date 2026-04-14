import tkinter as tk
from tkinter import ttk, messagebox
from controllers.collaborator_controller import (
    consultar_todos_los_colaboradores,
    registrar_nuevo_colaborador,
    modificar_colaborador_existente,
    eliminar_colaborador_existente
)

ROLES_COLABORADOR = ["Desarrollador", "Diseñador", "Analista", "Tester", "DevOps"]
ESTADOS_DISPONIBILIDAD = ["Activo", "Inactivo"]


def abrir_ventana_colaboradores(ventana_padre):
    ventana_colaboradores = tk.Toplevel(ventana_padre)
    ventana_colaboradores.title("Gestion de Colaboradores")
    ventana_colaboradores.geometry("900x520")

    id_colaborador_seleccionado = {"valor": None}

    def cargar_colaboradores_en_tabla():
        for fila in tabla_colaboradores.get_children():
            tabla_colaboradores.delete(fila)
        lista_colaboradores = consultar_todos_los_colaboradores()
        for colaborador in lista_colaboradores:
            tabla_colaboradores.insert("", "end", values=(
                colaborador["id_colaborador"],
                colaborador["nombre"],
                colaborador["apellido"],
                colaborador["rol_colaborador"],
                colaborador["especialidad"],
                colaborador["estado_disponibilidad"]
            ))

    def limpiar_formulario():
        id_colaborador_seleccionado["valor"] = None
        entrada_nombre.delete(0, tk.END)
        entrada_apellido.delete(0, tk.END)
        combo_rol.set(ROLES_COLABORADOR[0])
        entrada_especialidad.delete(0, tk.END)
        combo_estado.set(ESTADOS_DISPONIBILIDAD[0])

    def cargar_datos_en_formulario(evento):
        seleccion = tabla_colaboradores.selection()
        if not seleccion:
            return
        valores = tabla_colaboradores.item(seleccion[0])["values"]
        id_colaborador_seleccionado["valor"] = valores[0]
        entrada_nombre.delete(0, tk.END)
        entrada_nombre.insert(0, valores[1])
        entrada_apellido.delete(0, tk.END)
        entrada_apellido.insert(0, valores[2])
        combo_rol.set(valores[3])
        entrada_especialidad.delete(0, tk.END)
        entrada_especialidad.insert(0, valores[4])
        combo_estado.set(valores[5])

    def guardar_nuevo_colaborador():
        exito, mensaje = registrar_nuevo_colaborador(
            entrada_nombre.get().strip(),
            entrada_apellido.get().strip(),
            combo_rol.get(),
            entrada_especialidad.get().strip(),
            combo_estado.get()
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_colaboradores)
            limpiar_formulario()
            cargar_colaboradores_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_colaboradores)

    def actualizar_colaborador_seleccionado():
        if not id_colaborador_seleccionado["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione un colaborador de la tabla.", parent=ventana_colaboradores)
            return
        exito, mensaje = modificar_colaborador_existente(
            id_colaborador_seleccionado["valor"],
            entrada_nombre.get().strip(),
            entrada_apellido.get().strip(),
            combo_rol.get(),
            entrada_especialidad.get().strip(),
            combo_estado.get()
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_colaboradores)
            limpiar_formulario()
            cargar_colaboradores_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_colaboradores)

    def eliminar_colaborador_seleccionado():
        if not id_colaborador_seleccionado["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione un colaborador de la tabla.", parent=ventana_colaboradores)
            return
        confirmar = messagebox.askyesno("Confirmar eliminacion",
                                        "¿Esta seguro de que desea eliminar este colaborador?",
                                        parent=ventana_colaboradores)
        if not confirmar:
            return
        exito, mensaje = eliminar_colaborador_existente(id_colaborador_seleccionado["valor"])
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_colaboradores)
            limpiar_formulario()
            cargar_colaboradores_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_colaboradores)

    # --- Interfaz ---
    marco_formulario = tk.LabelFrame(ventana_colaboradores, text="Datos del Colaborador", padx=10, pady=8)
    marco_formulario.pack(fill="x", padx=10, pady=5)

    tk.Label(marco_formulario, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
    entrada_nombre = tk.Entry(marco_formulario, width=22)
    entrada_nombre.grid(row=0, column=1, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Apellido:").grid(row=0, column=2, sticky="e", padx=5, pady=3)
    entrada_apellido = tk.Entry(marco_formulario, width=22)
    entrada_apellido.grid(row=0, column=3, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Rol:").grid(row=1, column=0, sticky="e", padx=5, pady=3)
    combo_rol = ttk.Combobox(marco_formulario, values=ROLES_COLABORADOR, width=20, state="readonly")
    combo_rol.grid(row=1, column=1, sticky="w", pady=3)
    combo_rol.set(ROLES_COLABORADOR[0])

    tk.Label(marco_formulario, text="Especialidad:").grid(row=1, column=2, sticky="e", padx=5, pady=3)
    entrada_especialidad = tk.Entry(marco_formulario, width=22)
    entrada_especialidad.grid(row=1, column=3, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Estado:").grid(row=2, column=0, sticky="e", padx=5, pady=3)
    combo_estado = ttk.Combobox(marco_formulario, values=ESTADOS_DISPONIBILIDAD, width=20, state="readonly")
    combo_estado.grid(row=2, column=1, sticky="w", pady=3)
    combo_estado.set(ESTADOS_DISPONIBILIDAD[0])

    marco_botones = tk.Frame(ventana_colaboradores)
    marco_botones.pack(pady=5)

    tk.Button(marco_botones, text="Nuevo", width=12, command=limpiar_formulario).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Guardar", width=12, command=guardar_nuevo_colaborador).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Actualizar", width=12, command=actualizar_colaborador_seleccionado).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Eliminar", width=12, command=eliminar_colaborador_seleccionado).pack(side="left", padx=4)

    marco_tabla = tk.LabelFrame(ventana_colaboradores, text="Lista de Colaboradores", padx=5, pady=5)
    marco_tabla.pack(fill="both", expand=True, padx=10, pady=5)

    columnas_tabla = ("ID", "Nombre", "Apellido", "Rol", "Especialidad", "Estado")
    tabla_colaboradores = ttk.Treeview(marco_tabla, columns=columnas_tabla, show="headings", height=12)
    for nombre_columna in columnas_tabla:
        tabla_colaboradores.heading(nombre_columna, text=nombre_columna)
        tabla_colaboradores.column(nombre_columna, width=130)
    tabla_colaboradores.column("ID", width=40)

    barra_desplazamiento = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla_colaboradores.yview)
    tabla_colaboradores.configure(yscrollcommand=barra_desplazamiento.set)
    tabla_colaboradores.pack(side="left", fill="both", expand=True)
    barra_desplazamiento.pack(side="right", fill="y")

    tabla_colaboradores.bind("<<TreeviewSelect>>", cargar_datos_en_formulario)
    cargar_colaboradores_en_tabla()
