import tkinter as tk
from tkinter import ttk, messagebox
from controllers.project_controller import (
    consultar_todos_los_proyectos,
    consultar_proyectos_por_estado,
    registrar_nuevo_proyecto,
    modificar_proyecto_existente,
    eliminar_proyecto_existente
)
from controllers.client_controller import consultar_clientes_activos

ESTADOS_PROYECTO = ["En Proceso", "Completado", "Cancelado"]


def abrir_ventana_proyectos(ventana_padre):
    ventana_proyectos = tk.Toplevel(ventana_padre)
    ventana_proyectos.title("Gestion de Proyectos")
    ventana_proyectos.geometry("1000x600")

    id_proyecto_seleccionado = {"valor": None}
    fecha_fin_proyecto_seleccionado = {"valor": None}
    lista_clientes_cargados = []

    def obtener_nombres_clientes():
        nonlocal lista_clientes_cargados
        lista_clientes_cargados = consultar_clientes_activos()
        return [f"{c['nombre']} {c['apellido']} - {c['empresa'] or c['sector']}"
                for c in lista_clientes_cargados]

    def obtener_id_cliente_seleccionado():
        indice = combo_cliente.current()
        if indice < 0 or indice >= len(lista_clientes_cargados):
            return None
        return lista_clientes_cargados[indice]["id_cliente"]

    def cargar_proyectos_en_tabla(lista_proyectos=None):
        for fila in tabla_proyectos.get_children():
            tabla_proyectos.delete(fila)
        if lista_proyectos is None:
            lista_proyectos = consultar_todos_los_proyectos()
        for proyecto in lista_proyectos:
            tabla_proyectos.insert("", "end", values=(
                proyecto["id_proyecto"],
                proyecto["nombre_proyecto"],
                proyecto["nombre_cliente"],
                proyecto["estado"],
                proyecto["fecha_inicio"],
                proyecto["fecha_fin_estimada"],
                proyecto["fecha_fin_real"] or ""
            ))

    def limpiar_formulario():
        id_proyecto_seleccionado["valor"] = None
        fecha_fin_proyecto_seleccionado["valor"] = None
        entrada_nombre_proyecto.delete(0, tk.END)
        entrada_descripcion.delete(0, tk.END)
        entrada_fecha_inicio.delete(0, tk.END)
        entrada_fecha_fin_estimada.delete(0, tk.END)
        entrada_fecha_fin_real.delete(0, tk.END)
        combo_estado_proyecto.set(ESTADOS_PROYECTO[0])
        combo_cliente.set("")

    def cargar_datos_en_formulario(evento):
        seleccion = tabla_proyectos.selection()
        if not seleccion:
            return
        valores = tabla_proyectos.item(seleccion[0])["values"]
        id_proyecto_seleccionado["valor"] = valores[0]
        entrada_nombre_proyecto.delete(0, tk.END)
        entrada_nombre_proyecto.insert(0, valores[1])
        combo_estado_proyecto.set(valores[3])
        entrada_fecha_inicio.delete(0, tk.END)
        entrada_fecha_inicio.insert(0, valores[4])
        entrada_fecha_fin_estimada.delete(0, tk.END)
        entrada_fecha_fin_estimada.insert(0, valores[5])
        entrada_fecha_fin_real.delete(0, tk.END)
        if valores[6]:
            entrada_fecha_fin_real.insert(0, valores[6])
        fecha_fin_proyecto_seleccionado["valor"] = str(valores[5])

        lista_proyectos_completa = consultar_todos_los_proyectos()
        proyecto_actual = next((p for p in lista_proyectos_completa
                                if p["id_proyecto"] == valores[0]), None)
        if proyecto_actual:
            entrada_descripcion.delete(0, tk.END)
            entrada_descripcion.insert(0, proyecto_actual["descripcion"])
            for i, cliente in enumerate(lista_clientes_cargados):
                if cliente["id_cliente"] == proyecto_actual["id_cliente"]:
                    combo_cliente.current(i)
                    break

    def filtrar_por_estado():
        estado_filtro = combo_filtro_estado.get()
        if estado_filtro == "Todos":
            cargar_proyectos_en_tabla()
        else:
            lista_filtrada = consultar_proyectos_por_estado(estado_filtro)
            cargar_proyectos_en_tabla(lista_filtrada)

    def guardar_nuevo_proyecto():
        exito, mensaje = registrar_nuevo_proyecto(
            entrada_nombre_proyecto.get().strip(),
            entrada_descripcion.get().strip(),
            entrada_fecha_inicio.get().strip(),
            entrada_fecha_fin_estimada.get().strip(),
            combo_estado_proyecto.get(),
            obtener_id_cliente_seleccionado()
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_proyectos)
            limpiar_formulario()
            cargar_proyectos_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_proyectos)

    def actualizar_proyecto_seleccionado():
        if not id_proyecto_seleccionado["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione un proyecto de la tabla.", parent=ventana_proyectos)
            return
        exito, mensaje = modificar_proyecto_existente(
            id_proyecto_seleccionado["valor"],
            entrada_nombre_proyecto.get().strip(),
            entrada_descripcion.get().strip(),
            entrada_fecha_inicio.get().strip(),
            entrada_fecha_fin_estimada.get().strip(),
            entrada_fecha_fin_real.get().strip() or None,
            combo_estado_proyecto.get(),
            obtener_id_cliente_seleccionado()
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_proyectos)
            limpiar_formulario()
            cargar_proyectos_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_proyectos)

    def eliminar_proyecto_seleccionado():
        if not id_proyecto_seleccionado["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione un proyecto de la tabla.", parent=ventana_proyectos)
            return
        confirmar = messagebox.askyesno("Confirmar eliminacion",
                                        "¿Esta seguro de que desea eliminar este proyecto?",
                                        parent=ventana_proyectos)
        if not confirmar:
            return
        exito, mensaje = eliminar_proyecto_existente(id_proyecto_seleccionado["valor"])
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_proyectos)
            limpiar_formulario()
            cargar_proyectos_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_proyectos)

    # --- Interfaz ---
    marco_formulario = tk.LabelFrame(ventana_proyectos, text="Datos del Proyecto", padx=10, pady=8)
    marco_formulario.pack(fill="x", padx=10, pady=5)

    tk.Label(marco_formulario, text="Nombre Proyecto:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
    entrada_nombre_proyecto = tk.Entry(marco_formulario, width=28)
    entrada_nombre_proyecto.grid(row=0, column=1, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Descripcion:").grid(row=0, column=2, sticky="e", padx=5, pady=3)
    entrada_descripcion = tk.Entry(marco_formulario, width=28)
    entrada_descripcion.grid(row=0, column=3, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Cliente:").grid(row=0, column=4, sticky="e", padx=5, pady=3)
    combo_cliente = ttk.Combobox(marco_formulario, values=obtener_nombres_clientes(), width=25, state="readonly")
    combo_cliente.grid(row=0, column=5, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Fecha Inicio (YYYY-MM-DD):").grid(row=1, column=0, sticky="e", padx=5, pady=3)
    entrada_fecha_inicio = tk.Entry(marco_formulario, width=14)
    entrada_fecha_inicio.grid(row=1, column=1, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Fecha Fin Estimada:").grid(row=1, column=2, sticky="e", padx=5, pady=3)
    entrada_fecha_fin_estimada = tk.Entry(marco_formulario, width=14)
    entrada_fecha_fin_estimada.grid(row=1, column=3, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Fecha Fin Real:").grid(row=2, column=0, sticky="e", padx=5, pady=3)
    entrada_fecha_fin_real = tk.Entry(marco_formulario, width=14)
    entrada_fecha_fin_real.grid(row=2, column=1, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Estado:").grid(row=2, column=2, sticky="e", padx=5, pady=3)
    combo_estado_proyecto = ttk.Combobox(marco_formulario, values=ESTADOS_PROYECTO, width=15, state="readonly")
    combo_estado_proyecto.grid(row=2, column=3, sticky="w", pady=3)
    combo_estado_proyecto.set(ESTADOS_PROYECTO[0])

    marco_botones = tk.Frame(ventana_proyectos)
    marco_botones.pack(pady=5)

    tk.Button(marco_botones, text="Nuevo", width=12, command=limpiar_formulario).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Guardar", width=12, command=guardar_nuevo_proyecto).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Actualizar", width=12, command=actualizar_proyecto_seleccionado).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Eliminar", width=12, command=eliminar_proyecto_seleccionado).pack(side="left", padx=4)

    marco_filtros = tk.Frame(ventana_proyectos)
    marco_filtros.pack(pady=3)
    tk.Label(marco_filtros, text="Filtrar por estado:").pack(side="left", padx=5)
    combo_filtro_estado = ttk.Combobox(marco_filtros,
                                       values=["Todos"] + ESTADOS_PROYECTO,
                                       width=15, state="readonly")
    combo_filtro_estado.set("Todos")
    combo_filtro_estado.pack(side="left", padx=5)
    tk.Button(marco_filtros, text="Filtrar", command=filtrar_por_estado).pack(side="left", padx=5)

    marco_tabla = tk.LabelFrame(ventana_proyectos, text="Lista de Proyectos", padx=5, pady=5)
    marco_tabla.pack(fill="both", expand=True, padx=10, pady=5)

    columnas_tabla = ("ID", "Nombre Proyecto", "Cliente", "Estado",
                      "Fecha Inicio", "Fecha Fin Est.", "Fecha Fin Real")
    tabla_proyectos = ttk.Treeview(marco_tabla, columns=columnas_tabla, show="headings", height=10)
    anchos = [40, 200, 160, 90, 100, 100, 100]
    for nombre_columna, ancho in zip(columnas_tabla, anchos):
        tabla_proyectos.heading(nombre_columna, text=nombre_columna)
        tabla_proyectos.column(nombre_columna, width=ancho)

    barra_desplazamiento = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla_proyectos.yview)
    tabla_proyectos.configure(yscrollcommand=barra_desplazamiento.set)
    tabla_proyectos.pack(side="left", fill="both", expand=True)
    barra_desplazamiento.pack(side="right", fill="y")

    tabla_proyectos.bind("<<TreeviewSelect>>", cargar_datos_en_formulario)
    cargar_proyectos_en_tabla()
