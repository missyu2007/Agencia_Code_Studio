import tkinter as tk
from tkinter import ttk, messagebox
from controllers.task_controller import (
    consultar_todas_las_tareas,
    consultar_tareas_por_proyecto,
    consultar_tareas_por_colaborador,
    consultar_tareas_por_estado,
    registrar_nueva_tarea,
    modificar_tarea_existente,
    eliminar_tarea_existente,
    consultar_subtareas_por_tarea,
    registrar_nueva_sub_tarea,
    modificar_sub_tarea_existente,
    eliminar_sub_tarea_existente
)
from controllers.project_controller import consultar_todos_los_proyectos
from controllers.collaborator_controller import consultar_colaboradores_activos

ESTADOS_TAREA    = ["Pendiente", "En Progreso", "En Revision", "Completada", "Cancelada"]
PRIORIDADES      = ["Alta", "Media", "Baja"]
ESTADOS_SUBTAREA = ["Pendiente", "Completada"]


def abrir_ventana_tareas(ventana_padre):
    ventana_tareas = tk.Toplevel(ventana_padre)
    ventana_tareas.title("Gestion de Tareas")
    ventana_tareas.geometry("1060x660")

    id_tarea_seleccionada    = {"valor": None}
    lista_proyectos_cargados     = []
    lista_colaboradores_cargados = []

    # ── Carga de datos para los Combobox ──────────────────────────
    def obtener_nombres_proyectos():
        nonlocal lista_proyectos_cargados
        lista_proyectos_cargados = consultar_todos_los_proyectos()
        return [f"{p['nombre_proyecto']} ({p['estado']})" for p in lista_proyectos_cargados]

    def obtener_nombres_colaboradores():
        nonlocal lista_colaboradores_cargados
        lista_colaboradores_cargados = consultar_colaboradores_activos()
        return [f"{c['nombre']} {c['apellido']} - {c['rol_colaborador']}"
                for c in lista_colaboradores_cargados]

    def obtener_proyecto_seleccionado():
        """Devuelve (id_proyecto, fecha_fin_estimada_str) del proyecto activo en el combo."""
        indice = combo_proyecto.current()
        if indice < 0 or indice >= len(lista_proyectos_cargados):
            return None, None
        proyecto = lista_proyectos_cargados[indice]
        return proyecto["id_proyecto"], str(proyecto["fecha_fin_estimada"])

    def obtener_id_colaborador_seleccionado():
        indice = combo_colaborador.current()
        if indice < 0 or indice >= len(lista_colaboradores_cargados):
            return None
        return lista_colaboradores_cargados[indice]["id_colaborador"]

    # ── Actualiza etiqueta de fecha limite al cambiar proyecto ────
    def al_cambiar_proyecto(evento=None):
        _, fecha_fin = obtener_proyecto_seleccionado()
        if fecha_fin and fecha_fin != "None":
            etiqueta_limite_fecha.config(
                text=f"Fecha max. permitida para entrega: {fecha_fin}",
                fg="#B8860B"
            )
        else:
            etiqueta_limite_fecha.config(text="", fg="gray")

    # ── Tabla de tareas ───────────────────────────────────────────
    def cargar_tareas_en_tabla(lista_tareas=None):
        for fila in tabla_tareas.get_children():
            tabla_tareas.delete(fila)
        if lista_tareas is None:
            lista_tareas = consultar_todas_las_tareas()
        for tarea in lista_tareas:
            tabla_tareas.insert("", "end", values=(
                tarea["id_tarea"],
                tarea["nombre_tarea"],
                tarea["nombre_proyecto"],
                tarea["nombre_colaborador"],
                tarea["prioridad"],
                tarea["estado"],
                tarea["fecha_inicio"],
                tarea["fecha_entrega"]
            ))

    # ── Formulario ────────────────────────────────────────────────
    def limpiar_formulario_tarea():
        id_tarea_seleccionada["valor"] = None
        entrada_nombre_tarea.delete(0, tk.END)
        entrada_descripcion_tarea.delete(0, tk.END)
        combo_prioridad.set(PRIORIDADES[1])
        combo_estado_tarea.set(ESTADOS_TAREA[0])
        entrada_fecha_inicio_tarea.delete(0, tk.END)
        entrada_fecha_entrega_tarea.delete(0, tk.END)
        combo_proyecto.set("")
        combo_colaborador.set("")
        etiqueta_limite_fecha.config(text="", fg="gray")
        limpiar_tabla_subtareas()

    def cargar_datos_tarea_en_formulario(evento):
        seleccion = tabla_tareas.selection()
        if not seleccion:
            return
        valores = tabla_tareas.item(seleccion[0])["values"]
        id_tarea_seleccionada["valor"] = valores[0]

        entrada_nombre_tarea.delete(0, tk.END)
        entrada_nombre_tarea.insert(0, valores[1])
        combo_prioridad.set(valores[4])
        combo_estado_tarea.set(valores[5])
        entrada_fecha_inicio_tarea.delete(0, tk.END)
        entrada_fecha_inicio_tarea.insert(0, valores[6])
        entrada_fecha_entrega_tarea.delete(0, tk.END)
        entrada_fecha_entrega_tarea.insert(0, valores[7])

        lista_tareas_completa = consultar_todas_las_tareas()
        tarea_actual = next((t for t in lista_tareas_completa
                             if t["id_tarea"] == valores[0]), None)
        if tarea_actual:
            entrada_descripcion_tarea.delete(0, tk.END)
            entrada_descripcion_tarea.insert(0, tarea_actual["descripcion"])
            for i, proyecto in enumerate(lista_proyectos_cargados):
                if proyecto["id_proyecto"] == tarea_actual["id_proyecto"]:
                    combo_proyecto.current(i)
                    al_cambiar_proyecto()
                    break
            for i, colaborador in enumerate(lista_colaboradores_cargados):
                if colaborador["id_colaborador"] == tarea_actual["id_colaborador"]:
                    combo_colaborador.current(i)
                    break

        cargar_subtareas_en_tabla(valores[0])

    def filtrar_tareas():
        filtro = combo_filtro_tarea.get()
        if filtro == "Todos":
            cargar_tareas_en_tabla()
        else:
            cargar_tareas_en_tabla(consultar_tareas_por_estado(filtro))

    # ── CRUD Tareas ───────────────────────────────────────────────
    def guardar_nueva_tarea():
        id_proyecto, fecha_fin_proyecto = obtener_proyecto_seleccionado()
        exito, mensaje = registrar_nueva_tarea(
            entrada_nombre_tarea.get().strip(),
            entrada_descripcion_tarea.get().strip(),
            combo_prioridad.get(),
            combo_estado_tarea.get(),
            entrada_fecha_inicio_tarea.get().strip(),
            entrada_fecha_entrega_tarea.get().strip(),
            id_proyecto,
            obtener_id_colaborador_seleccionado(),
            fecha_fin_proyecto
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_tareas)
            limpiar_formulario_tarea()
            cargar_tareas_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_tareas)

    def actualizar_tarea_seleccionada():
        if not id_tarea_seleccionada["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione una tarea de la tabla.",
                                   parent=ventana_tareas)
            return
        id_proyecto, fecha_fin_proyecto = obtener_proyecto_seleccionado()
        exito, mensaje = modificar_tarea_existente(
            id_tarea_seleccionada["valor"],
            entrada_nombre_tarea.get().strip(),
            entrada_descripcion_tarea.get().strip(),
            combo_prioridad.get(),
            combo_estado_tarea.get(),
            entrada_fecha_inicio_tarea.get().strip(),
            entrada_fecha_entrega_tarea.get().strip(),
            id_proyecto,
            obtener_id_colaborador_seleccionado(),
            fecha_fin_proyecto
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_tareas)
            limpiar_formulario_tarea()
            cargar_tareas_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_tareas)

    def eliminar_tarea_seleccionada():
        if not id_tarea_seleccionada["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione una tarea de la tabla.",
                                   parent=ventana_tareas)
            return
        confirmar = messagebox.askyesno(
            "Confirmar eliminacion",
            "¿Esta seguro? Tambien se eliminaran sus subtareas.",
            parent=ventana_tareas
        )
        if not confirmar:
            return
        exito, mensaje = eliminar_tarea_existente(id_tarea_seleccionada["valor"])
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_tareas)
            limpiar_formulario_tarea()
            cargar_tareas_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_tareas)

    # ── Subtareas ────────────────────────────────────────────────
    id_subtarea_seleccionada = {"valor": None}

    def limpiar_tabla_subtareas():
        for fila in tabla_subtareas.get_children():
            tabla_subtareas.delete(fila)
        entrada_descripcion_subtarea.delete(0, tk.END)
        combo_estado_subtarea.set(ESTADOS_SUBTAREA[0])
        id_subtarea_seleccionada["valor"] = None

    def cargar_subtareas_en_tabla(id_tarea):
        for fila in tabla_subtareas.get_children():
            tabla_subtareas.delete(fila)
        lista_subtareas = consultar_subtareas_por_tarea(id_tarea)
        for subtarea in lista_subtareas:
            tabla_subtareas.insert("", "end", values=(
                subtarea["id_sub_tarea"],
                subtarea["descripcion"],
                subtarea["estado"]
            ))

    def seleccionar_subtarea(evento):
        seleccion = tabla_subtareas.selection()
        if not seleccion:
            return
        valores = tabla_subtareas.item(seleccion[0])["values"]
        id_subtarea_seleccionada["valor"] = valores[0]
        entrada_descripcion_subtarea.delete(0, tk.END)
        entrada_descripcion_subtarea.insert(0, valores[1])
        combo_estado_subtarea.set(valores[2])

    def guardar_nueva_subtarea():
        if not id_tarea_seleccionada["valor"]:
            messagebox.showwarning("Advertencia", "Primero seleccione una tarea de la tabla.",
                                   parent=ventana_tareas)
            return
        exito, mensaje = registrar_nueva_sub_tarea(
            entrada_descripcion_subtarea.get().strip(),
            combo_estado_subtarea.get(),
            id_tarea_seleccionada["valor"]
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_tareas)
            entrada_descripcion_subtarea.delete(0, tk.END)
            cargar_subtareas_en_tabla(id_tarea_seleccionada["valor"])
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_tareas)

    def actualizar_subtarea_seleccionada():
        if not id_subtarea_seleccionada["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione una subtarea del panel derecho.",
                                   parent=ventana_tareas)
            return
        exito, mensaje = modificar_sub_tarea_existente(
            id_subtarea_seleccionada["valor"],
            entrada_descripcion_subtarea.get().strip(),
            combo_estado_subtarea.get()
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_tareas)
            cargar_subtareas_en_tabla(id_tarea_seleccionada["valor"])
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_tareas)

    def eliminar_subtarea_seleccionada():
        if not id_subtarea_seleccionada["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione una subtarea del panel derecho.",
                                   parent=ventana_tareas)
            return
        confirmar = messagebox.askyesno("Confirmar", "¿Eliminar esta subtarea?",
                                        parent=ventana_tareas)
        if not confirmar:
            return
        exito, mensaje = eliminar_sub_tarea_existente(id_subtarea_seleccionada["valor"])
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_tareas)
            cargar_subtareas_en_tabla(id_tarea_seleccionada["valor"])
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_tareas)

    # ════════════════════════════════════════════════════════════
    #  CONSTRUCCION DE LA INTERFAZ
    # ════════════════════════════════════════════════════════════

    # ── Formulario de la tarea ───────────────────────────────────
    marco_formulario = tk.LabelFrame(ventana_tareas, text="Datos de la Tarea", padx=8, pady=6)
    marco_formulario.pack(fill="x", padx=10, pady=5)

    # Fila 0: nombre, descripcion, prioridad
    tk.Label(marco_formulario, text="Nombre Tarea:").grid(
        row=0, column=0, sticky="e", padx=4, pady=3)
    entrada_nombre_tarea = tk.Entry(marco_formulario, width=25)
    entrada_nombre_tarea.grid(row=0, column=1, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Descripcion:").grid(
        row=0, column=2, sticky="e", padx=4, pady=3)
    entrada_descripcion_tarea = tk.Entry(marco_formulario, width=25)
    entrada_descripcion_tarea.grid(row=0, column=3, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Prioridad:").grid(
        row=0, column=4, sticky="e", padx=4, pady=3)
    combo_prioridad = ttk.Combobox(marco_formulario, values=PRIORIDADES, width=10, state="readonly")
    combo_prioridad.set(PRIORIDADES[1])
    combo_prioridad.grid(row=0, column=5, sticky="w", pady=3)

    # Fila 1: estado, fechas
    tk.Label(marco_formulario, text="Estado:").grid(
        row=1, column=0, sticky="e", padx=4, pady=3)
    combo_estado_tarea = ttk.Combobox(marco_formulario, values=ESTADOS_TAREA, width=14, state="readonly")
    combo_estado_tarea.set(ESTADOS_TAREA[0])
    combo_estado_tarea.grid(row=1, column=1, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Fecha Inicio (YYYY-MM-DD):").grid(
        row=1, column=2, sticky="e", padx=4, pady=3)
    entrada_fecha_inicio_tarea = tk.Entry(marco_formulario, width=13)
    entrada_fecha_inicio_tarea.grid(row=1, column=3, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Fecha Entrega (YYYY-MM-DD):").grid(
        row=1, column=4, sticky="e", padx=4, pady=3)
    entrada_fecha_entrega_tarea = tk.Entry(marco_formulario, width=13)
    entrada_fecha_entrega_tarea.grid(row=1, column=5, sticky="w", pady=3)

    # Fila 2: proyecto, colaborador
    tk.Label(marco_formulario, text="Proyecto:").grid(
        row=2, column=0, sticky="e", padx=4, pady=3)
    combo_proyecto = ttk.Combobox(
        marco_formulario, values=obtener_nombres_proyectos(), width=30, state="readonly")
    combo_proyecto.grid(row=2, column=1, columnspan=2, sticky="w", pady=3)
    combo_proyecto.bind("<<ComboboxSelected>>", al_cambiar_proyecto)

    tk.Label(marco_formulario, text="Colaborador:").grid(
        row=2, column=3, sticky="e", padx=4, pady=3)
    combo_colaborador = ttk.Combobox(
        marco_formulario, values=obtener_nombres_colaboradores(), width=30, state="readonly")
    combo_colaborador.grid(row=2, column=4, columnspan=2, sticky="w", pady=3)

    # Fila 3: etiqueta informativa de fecha limite
    etiqueta_limite_fecha = tk.Label(
        marco_formulario,
        text="",
        font=("Arial", 9, "bold"),
        fg="#B8860B",
        anchor="w"
    )
    etiqueta_limite_fecha.grid(row=3, column=0, columnspan=6, sticky="w", padx=6, pady=(0, 2))

    # ── Botones CRUD ─────────────────────────────────────────────
    marco_botones_tarea = tk.Frame(ventana_tareas)
    marco_botones_tarea.pack(pady=4)
    tk.Button(marco_botones_tarea, text="Nuevo",     width=12,
              command=limpiar_formulario_tarea).pack(side="left", padx=3)
    tk.Button(marco_botones_tarea, text="Guardar",   width=12,
              command=guardar_nueva_tarea).pack(side="left", padx=3)
    tk.Button(marco_botones_tarea, text="Actualizar",width=12,
              command=actualizar_tarea_seleccionada).pack(side="left", padx=3)
    tk.Button(marco_botones_tarea, text="Eliminar",  width=12,
              command=eliminar_tarea_seleccionada).pack(side="left", padx=3)

    # ── Filtro de estado ─────────────────────────────────────────
    marco_filtro = tk.Frame(ventana_tareas)
    marco_filtro.pack(pady=2)
    tk.Label(marco_filtro, text="Filtrar por estado:").pack(side="left", padx=5)
    combo_filtro_tarea = ttk.Combobox(
        marco_filtro, values=["Todos"] + ESTADOS_TAREA, width=15, state="readonly")
    combo_filtro_tarea.set("Todos")
    combo_filtro_tarea.pack(side="left", padx=5)
    tk.Button(marco_filtro, text="Filtrar", command=filtrar_tareas).pack(side="left", padx=5)

    # ── Panel inferior: tabla tareas + panel subtareas ────────────
    marco_inferior = tk.Frame(ventana_tareas)
    marco_inferior.pack(fill="both", expand=True, padx=10, pady=5)

    # Tabla de tareas
    marco_tabla_tareas = tk.LabelFrame(marco_inferior, text="Lista de Tareas", padx=5, pady=5)
    marco_tabla_tareas.pack(side="left", fill="both", expand=True)

    columnas_tarea = ("ID", "Nombre Tarea", "Proyecto", "Colaborador",
                      "Prioridad", "Estado", "F. Inicio", "F. Entrega")
    tabla_tareas = ttk.Treeview(
        marco_tabla_tareas, columns=columnas_tarea, show="headings", height=9)
    anchos_tarea = [35, 155, 145, 135, 65, 90, 85, 85]
    for nombre_columna, ancho in zip(columnas_tarea, anchos_tarea):
        tabla_tareas.heading(nombre_columna, text=nombre_columna)
        tabla_tareas.column(nombre_columna, width=ancho)
    barra_tareas = ttk.Scrollbar(marco_tabla_tareas, orient="vertical",
                                  command=tabla_tareas.yview)
    tabla_tareas.configure(yscrollcommand=barra_tareas.set)
    tabla_tareas.pack(side="left", fill="both", expand=True)
    barra_tareas.pack(side="right", fill="y")
    tabla_tareas.bind("<<TreeviewSelect>>", cargar_datos_tarea_en_formulario)

    # Panel de subtareas
    marco_subtareas = tk.LabelFrame(
        marco_inferior, text="Subtareas de la Tarea Seleccionada", padx=5, pady=5)
    marco_subtareas.pack(side="right", fill="both", padx=(5, 0))

    tk.Label(marco_subtareas, text="Descripcion:").grid(
        row=0, column=0, sticky="e", padx=4, pady=3)
    entrada_descripcion_subtarea = tk.Entry(marco_subtareas, width=22)
    entrada_descripcion_subtarea.grid(row=0, column=1, sticky="w", pady=3)

    tk.Label(marco_subtareas, text="Estado:").grid(
        row=1, column=0, sticky="e", padx=4, pady=3)
    combo_estado_subtarea = ttk.Combobox(
        marco_subtareas, values=ESTADOS_SUBTAREA, width=12, state="readonly")
    combo_estado_subtarea.set(ESTADOS_SUBTAREA[0])
    combo_estado_subtarea.grid(row=1, column=1, sticky="w", pady=3)

    marco_botones_subtarea = tk.Frame(marco_subtareas)
    marco_botones_subtarea.grid(row=2, column=0, columnspan=2, pady=4)
    tk.Button(marco_botones_subtarea, text="Agregar",   width=9,
              command=guardar_nueva_subtarea).pack(side="left", padx=2)
    tk.Button(marco_botones_subtarea, text="Actualizar",width=9,
              command=actualizar_subtarea_seleccionada).pack(side="left", padx=2)
    tk.Button(marco_botones_subtarea, text="Eliminar",  width=9,
              command=eliminar_subtarea_seleccionada).pack(side="left", padx=2)

    columnas_subtarea = ("ID", "Descripcion", "Estado")
    tabla_subtareas = ttk.Treeview(
        marco_subtareas, columns=columnas_subtarea, show="headings", height=9)
    tabla_subtareas.heading("ID", text="ID")
    tabla_subtareas.column("ID", width=30)
    tabla_subtareas.heading("Descripcion", text="Descripcion")
    tabla_subtareas.column("Descripcion", width=185)
    tabla_subtareas.heading("Estado", text="Estado")
    tabla_subtareas.column("Estado", width=80)
    tabla_subtareas.grid(row=3, column=0, columnspan=2, sticky="nsew")
    tabla_subtareas.bind("<<TreeviewSelect>>", seleccionar_subtarea)

    # Carga inicial
    cargar_tareas_en_tabla()
