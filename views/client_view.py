import tkinter as tk
from tkinter import ttk, messagebox
from controllers.client_controller import (
    consultar_todos_los_clientes,
    registrar_nuevo_cliente,
    modificar_cliente_existente,
    eliminar_cliente_existente
)

ESTADOS_CLIENTE = ["Activo", "Inactivo"]
SECTORES = ["Retail", "Salud", "Educacion", "Logistica", "Tecnologia",
            "Finanzas", "Turismo", "Construccion", "Otro"]


def abrir_ventana_clientes(ventana_padre):
    ventana_clientes = tk.Toplevel(ventana_padre)
    ventana_clientes.title("Gestion de Clientes")
    ventana_clientes.geometry("950x550")

    id_cliente_seleccionado = {"valor": None}

    # --- Funciones internas ---

    def cargar_clientes_en_tabla():
        for fila in tabla_clientes.get_children():
            tabla_clientes.delete(fila)
        lista_clientes = consultar_todos_los_clientes()
        for cliente in lista_clientes:
            tabla_clientes.insert("", "end", values=(
                cliente["id_cliente"],
                cliente["nombre"],
                cliente["apellido"],
                cliente["empresa"] or "",
                cliente["sector"],
                cliente["telefono"],
                cliente["email"],
                cliente["estado"]
            ))

    def limpiar_formulario():
        id_cliente_seleccionado["valor"] = None
        entrada_nombre.delete(0, tk.END)
        entrada_apellido.delete(0, tk.END)
        entrada_empresa.delete(0, tk.END)
        combo_sector.set(SECTORES[0])
        entrada_telefono.delete(0, tk.END)
        entrada_email.delete(0, tk.END)
        combo_estado.set(ESTADOS_CLIENTE[0])

    def cargar_datos_en_formulario(evento):
        seleccion = tabla_clientes.selection()
        if not seleccion:
            return
        valores = tabla_clientes.item(seleccion[0])["values"]
        id_cliente_seleccionado["valor"] = valores[0]
        entrada_nombre.delete(0, tk.END)
        entrada_nombre.insert(0, valores[1])
        entrada_apellido.delete(0, tk.END)
        entrada_apellido.insert(0, valores[2])
        entrada_empresa.delete(0, tk.END)
        entrada_empresa.insert(0, valores[3])
        combo_sector.set(valores[4])
        entrada_telefono.delete(0, tk.END)
        entrada_telefono.insert(0, valores[5])
        entrada_email.delete(0, tk.END)
        entrada_email.insert(0, valores[6])
        combo_estado.set(valores[7])

    def guardar_nuevo_cliente():
        exito, mensaje = registrar_nuevo_cliente(
            entrada_nombre.get().strip(),
            entrada_apellido.get().strip(),
            entrada_empresa.get().strip(),
            combo_sector.get(),
            entrada_telefono.get().strip(),
            entrada_email.get().strip(),
            combo_estado.get()
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_clientes)
            limpiar_formulario()
            cargar_clientes_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_clientes)

    def actualizar_cliente_seleccionado():
        if not id_cliente_seleccionado["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione un cliente de la tabla.", parent=ventana_clientes)
            return
        exito, mensaje = modificar_cliente_existente(
            id_cliente_seleccionado["valor"],
            entrada_nombre.get().strip(),
            entrada_apellido.get().strip(),
            entrada_empresa.get().strip(),
            combo_sector.get(),
            entrada_telefono.get().strip(),
            entrada_email.get().strip(),
            combo_estado.get()
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_clientes)
            limpiar_formulario()
            cargar_clientes_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_clientes)

    def eliminar_cliente_seleccionado():
        if not id_cliente_seleccionado["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione un cliente de la tabla.", parent=ventana_clientes)
            return
        confirmar = messagebox.askyesno("Confirmar eliminacion",
                                        "¿Esta seguro de que desea eliminar este cliente?",
                                        parent=ventana_clientes)
        if not confirmar:
            return
        exito, mensaje = eliminar_cliente_existente(id_cliente_seleccionado["valor"])
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_clientes)
            limpiar_formulario()
            cargar_clientes_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_clientes)

    # --- Construccion de la interfaz ---

    marco_formulario = tk.LabelFrame(ventana_clientes, text="Datos del Cliente", padx=10, pady=8)
    marco_formulario.pack(fill="x", padx=10, pady=5)

    tk.Label(marco_formulario, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
    entrada_nombre = tk.Entry(marco_formulario, width=20)
    entrada_nombre.grid(row=0, column=1, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Apellido:").grid(row=0, column=2, sticky="e", padx=5, pady=3)
    entrada_apellido = tk.Entry(marco_formulario, width=20)
    entrada_apellido.grid(row=0, column=3, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Empresa:").grid(row=0, column=4, sticky="e", padx=5, pady=3)
    entrada_empresa = tk.Entry(marco_formulario, width=20)
    entrada_empresa.grid(row=0, column=5, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Sector:").grid(row=1, column=0, sticky="e", padx=5, pady=3)
    combo_sector = ttk.Combobox(marco_formulario, values=SECTORES, width=18, state="readonly")
    combo_sector.grid(row=1, column=1, sticky="w", pady=3)
    combo_sector.set(SECTORES[0])

    tk.Label(marco_formulario, text="Telefono:").grid(row=1, column=2, sticky="e", padx=5, pady=3)
    entrada_telefono = tk.Entry(marco_formulario, width=20)
    entrada_telefono.grid(row=1, column=3, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Email:").grid(row=1, column=4, sticky="e", padx=5, pady=3)
    entrada_email = tk.Entry(marco_formulario, width=20)
    entrada_email.grid(row=1, column=5, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Estado:").grid(row=2, column=0, sticky="e", padx=5, pady=3)
    combo_estado = ttk.Combobox(marco_formulario, values=ESTADOS_CLIENTE, width=18, state="readonly")
    combo_estado.grid(row=2, column=1, sticky="w", pady=3)
    combo_estado.set(ESTADOS_CLIENTE[0])

    marco_botones = tk.Frame(ventana_clientes)
    marco_botones.pack(pady=5)

    tk.Button(marco_botones, text="Nuevo", width=12, command=limpiar_formulario).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Guardar", width=12, command=guardar_nuevo_cliente).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Actualizar", width=12, command=actualizar_cliente_seleccionado).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Eliminar", width=12, command=eliminar_cliente_seleccionado).pack(side="left", padx=4)

    marco_tabla = tk.LabelFrame(ventana_clientes, text="Lista de Clientes", padx=5, pady=5)
    marco_tabla.pack(fill="both", expand=True, padx=10, pady=5)

    columnas_tabla = ("ID", "Nombre", "Apellido", "Empresa", "Sector", "Telefono", "Email", "Estado")
    tabla_clientes = ttk.Treeview(marco_tabla, columns=columnas_tabla, show="headings", height=12)
    for nombre_columna in columnas_tabla:
        tabla_clientes.heading(nombre_columna, text=nombre_columna)
        tabla_clientes.column(nombre_columna, width=100 if nombre_columna not in ("Email", "Empresa") else 140)
    tabla_clientes.column("ID", width=40)

    barra_desplazamiento = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla_clientes.yview)
    tabla_clientes.configure(yscrollcommand=barra_desplazamiento.set)
    tabla_clientes.pack(side="left", fill="both", expand=True)
    barra_desplazamiento.pack(side="right", fill="y")

    tabla_clientes.bind("<<TreeviewSelect>>", cargar_datos_en_formulario)

    cargar_clientes_en_tabla()
