import tkinter as tk
from tkinter import ttk, messagebox
from controllers.task_controller import consultar_reporte_avance_proyectos
from controllers.project_controller import (
    consultar_todos_los_proyectos,
    consultar_proyectos_por_cliente,
    consultar_proyectos_por_estado,
    consultar_proyectos_por_rango_de_fechas,
    consultar_avance_porcentual_de_proyecto
)
from controllers.collaborator_controller import (
    consultar_todas_las_asignaciones,
    consultar_asignaciones_por_proyecto,
    consultar_todos_los_colaboradores
)
from controllers.client_controller import consultar_clientes_activos
from controllers.task_controller import (
    consultar_todas_las_tareas,
    consultar_tareas_por_proyecto,
    consultar_tareas_por_colaborador,
    consultar_tareas_por_estado
)

ESTADOS_PROYECTO = ["En Proceso", "Completado", "Cancelado"]
ESTADOS_TAREA = ["Pendiente", "En Progreso", "En Revision", "Completada", "Cancelada"]


def abrir_ventana_reportes(ventana_padre):
    ventana_reportes = tk.Toplevel(ventana_padre)
    ventana_reportes.title("Consultas y Reportes")
    ventana_reportes.geometry("1100x650")

    lista_proyectos_cargados = []
    lista_colaboradores_cargados = []
    lista_clientes_cargados = []

    def obtener_nombres_proyectos():
        nonlocal lista_proyectos_cargados
        lista_proyectos_cargados = consultar_todos_los_proyectos()
        return ["Todos"] + [p["nombre_proyecto"] for p in lista_proyectos_cargados]

    def obtener_nombres_colaboradores():
        nonlocal lista_colaboradores_cargados
        lista_colaboradores_cargados = consultar_todos_los_colaboradores()
        return ["Todos"] + [f"{c['nombre']} {c['apellido']}" for c in lista_colaboradores_cargados]

    def obtener_nombres_clientes():
        nonlocal lista_clientes_cargados
        lista_clientes_cargados = consultar_clientes_activos()
        return ["Todos"] + [f"{c['nombre']} {c['apellido']}" for c in lista_clientes_cargados]

    def limpiar_tabla_resultado():
        for fila in tabla_resultado.get_children():
            tabla_resultado.delete(fila)
        for columna in tabla_resultado["columns"]:
            tabla_resultado.heading(columna, text="")
        tabla_resultado["columns"] = []

    def configurar_columnas_tabla(nombres_columnas, anchos=None):
        tabla_resultado["columns"] = nombres_columnas
        tabla_resultado["show"] = "headings"
        for i, nombre_columna in enumerate(nombres_columnas):
            tabla_resultado.heading(nombre_columna, text=nombre_columna)
            ancho = anchos[i] if anchos and i < len(anchos) else 130
            tabla_resultado.column(nombre_columna, width=ancho)

    # --- Reporte 1: Vista completa proyecto-cliente-tarea-colaborador ---
    def ejecutar_reporte_vista_completa():
        limpiar_tabla_resultado()
        lista_tareas = consultar_todas_las_tareas()
        columnas = ("ID Tarea", "Tarea", "Proyecto", "Cliente", "Colaborador", "Prioridad", "Estado", "F. Entrega")
        anchos = [65, 160, 160, 140, 150, 70, 90, 90]
        configurar_columnas_tabla(columnas, anchos)
        for tarea in lista_tareas:
            proyectos = consultar_todos_los_proyectos()
            proyecto_actual = next((p for p in proyectos if p["id_proyecto"] == tarea["id_proyecto"]), None)
            nombre_cliente = proyecto_actual["nombre_cliente"] if proyecto_actual else ""
            tabla_resultado.insert("", "end", values=(
                tarea["id_tarea"],
                tarea["nombre_tarea"],
                tarea["nombre_proyecto"],
                nombre_cliente,
                tarea["nombre_colaborador"],
                tarea["prioridad"],
                tarea["estado"],
                tarea["fecha_entrega"]
            ))
        etiqueta_resultado.config(text=f"Vista completa: {len(lista_tareas)} registros encontrados.")

    # --- Reporte 2: Avance porcentual por proyecto ---
    def ejecutar_reporte_avance_proyectos():
        limpiar_tabla_resultado()
        lista_avance = consultar_reporte_avance_proyectos()
        columnas = ("ID", "Proyecto", "Estado Proyecto", "Total Tareas",
                    "Completadas", "Pendientes", "En Progreso", "% Avance")
        anchos = [40, 220, 100, 90, 90, 90, 90, 80]
        configurar_columnas_tabla(columnas, anchos)
        for fila in lista_avance:
            tabla_resultado.insert("", "end", values=(
                fila["id_proyecto"],
                fila["nombre_proyecto"],
                fila["estado_proyecto"],
                fila["total_tareas"],
                fila["tareas_completadas"],
                fila["tareas_pendientes"],
                fila["tareas_en_progreso"],
                f"{fila['porcentaje_avance']}%"
            ))
        etiqueta_resultado.config(text=f"Reporte de avance: {len(lista_avance)} proyectos.")

    # --- Reporte 3: Filtrar tareas por proyecto ---
    def ejecutar_filtro_tareas_por_proyecto():
        limpiar_tabla_resultado()
        indice = combo_filtro_proyecto.current()
        if indice <= 0 or indice > len(lista_proyectos_cargados):
            lista_tareas = consultar_todas_las_tareas()
        else:
            id_proyecto = lista_proyectos_cargados[indice - 1]["id_proyecto"]
            lista_tareas = consultar_tareas_por_proyecto(id_proyecto)
        columnas = ("ID", "Tarea", "Descripcion", "Prioridad", "Estado", "F. Inicio", "F. Entrega", "Colaborador")
        anchos = [40, 160, 180, 70, 90, 90, 90, 150]
        configurar_columnas_tabla(columnas, anchos)
        for tarea in lista_tareas:
            tabla_resultado.insert("", "end", values=(
                tarea["id_tarea"],
                tarea["nombre_tarea"],
                tarea["descripcion"],
                tarea["prioridad"],
                tarea["estado"],
                tarea["fecha_inicio"],
                tarea["fecha_entrega"],
                tarea["nombre_colaborador"]
            ))
        etiqueta_resultado.config(text=f"Tareas encontradas: {len(lista_tareas)}")

    # --- Reporte 4: Filtrar tareas por colaborador ---
    def ejecutar_filtro_tareas_por_colaborador():
        limpiar_tabla_resultado()
        indice = combo_filtro_colaborador.current()
        if indice <= 0 or indice > len(lista_colaboradores_cargados):
            lista_tareas = consultar_todas_las_tareas()
        else:
            id_colaborador = lista_colaboradores_cargados[indice - 1]["id_colaborador"]
            lista_tareas = consultar_tareas_por_colaborador(id_colaborador)
        columnas = ("ID", "Tarea", "Proyecto", "Prioridad", "Estado", "F. Inicio", "F. Entrega")
        anchos = [40, 180, 200, 70, 90, 90, 90]
        configurar_columnas_tabla(columnas, anchos)
        for tarea in lista_tareas:
            tabla_resultado.insert("", "end", values=(
                tarea["id_tarea"],
                tarea["nombre_tarea"],
                tarea["nombre_proyecto"],
                tarea["prioridad"],
                tarea["estado"],
                tarea["fecha_inicio"],
                tarea["fecha_entrega"]
            ))
        etiqueta_resultado.config(text=f"Tareas del colaborador: {len(lista_tareas)}")

    # --- Reporte 5: Filtrar tareas por estado ---
    def ejecutar_filtro_tareas_por_estado():
        limpiar_tabla_resultado()
        estado_seleccionado = combo_filtro_estado_tarea.get()
        if estado_seleccionado == "Todos":
            lista_tareas = consultar_todas_las_tareas()
        else:
            lista_tareas = consultar_tareas_por_estado(estado_seleccionado)
        columnas = ("ID", "Tarea", "Proyecto", "Colaborador", "Prioridad", "Estado", "F. Entrega")
        anchos = [40, 170, 170, 150, 70, 90, 90]
        configurar_columnas_tabla(columnas, anchos)
        for tarea in lista_tareas:
            tabla_resultado.insert("", "end", values=(
                tarea["id_tarea"],
                tarea["nombre_tarea"],
                tarea["nombre_proyecto"],
                tarea["nombre_colaborador"],
                tarea["prioridad"],
                tarea["estado"],
                tarea["fecha_entrega"]
            ))
        etiqueta_resultado.config(text=f"Tareas con estado '{estado_seleccionado}': {len(lista_tareas)}")

    # --- Reporte 6: Proyectos por rango de fechas ---
    def ejecutar_filtro_proyectos_por_fechas():
        fecha_inicio = entrada_fecha_inicio_filtro.get().strip()
        fecha_fin = entrada_fecha_fin_filtro.get().strip()
        if not fecha_inicio or not fecha_fin:
            messagebox.showwarning("Advertencia", "Ingrese ambas fechas para filtrar.", parent=ventana_reportes)
            return
        limpiar_tabla_resultado()
        lista_proyectos = consultar_proyectos_por_rango_de_fechas(fecha_inicio, fecha_fin)
        columnas = ("ID", "Proyecto", "Cliente", "Estado", "F. Inicio", "F. Fin Estimada")
        anchos = [40, 220, 160, 100, 100, 120]
        configurar_columnas_tabla(columnas, anchos)
        for proyecto in lista_proyectos:
            tabla_resultado.insert("", "end", values=(
                proyecto["id_proyecto"],
                proyecto["nombre_proyecto"],
                proyecto["nombre_cliente"],
                proyecto["estado"],
                proyecto["fecha_inicio"],
                proyecto["fecha_fin_estimada"]
            ))
        etiqueta_resultado.config(text=f"Proyectos en rango de fechas: {len(lista_proyectos)}")

    # --- Construccion de la interfaz ---
    marco_filtros = tk.LabelFrame(ventana_reportes, text="Filtros y Reportes", padx=8, pady=6)
    marco_filtros.pack(fill="x", padx=10, pady=5)

    # Fila 1 - Reportes generales
    fila_reportes_generales = tk.Frame(marco_filtros)
    fila_reportes_generales.grid(row=0, column=0, columnspan=6, sticky="w", pady=4)
    tk.Label(fila_reportes_generales, text="Reportes generales:").pack(side="left", padx=5)
    tk.Button(fila_reportes_generales, text="Vista Completa (JOIN)", width=22,
              command=ejecutar_reporte_vista_completa).pack(side="left", padx=4)
    tk.Button(fila_reportes_generales, text="Avance por Proyecto (%)", width=22,
              command=ejecutar_reporte_avance_proyectos).pack(side="left", padx=4)

    # Fila 2 - Filtro por proyecto
    fila_filtro_proyecto = tk.Frame(marco_filtros)
    fila_filtro_proyecto.grid(row=1, column=0, columnspan=6, sticky="w", pady=4)
    tk.Label(fila_filtro_proyecto, text="Tareas del proyecto:").pack(side="left", padx=5)
    combo_filtro_proyecto = ttk.Combobox(fila_filtro_proyecto, values=obtener_nombres_proyectos(),
                                          width=28, state="readonly")
    combo_filtro_proyecto.set("Todos")
    combo_filtro_proyecto.pack(side="left", padx=5)
    tk.Button(fila_filtro_proyecto, text="Filtrar", command=ejecutar_filtro_tareas_por_proyecto).pack(side="left", padx=4)

    # Fila 3 - Filtro por colaborador
    fila_filtro_colaborador = tk.Frame(marco_filtros)
    fila_filtro_colaborador.grid(row=2, column=0, columnspan=6, sticky="w", pady=4)
    tk.Label(fila_filtro_colaborador, text="Tareas del colaborador:").pack(side="left", padx=5)
    combo_filtro_colaborador = ttk.Combobox(fila_filtro_colaborador, values=obtener_nombres_colaboradores(),
                                             width=28, state="readonly")
    combo_filtro_colaborador.set("Todos")
    combo_filtro_colaborador.pack(side="left", padx=5)
    tk.Button(fila_filtro_colaborador, text="Filtrar", command=ejecutar_filtro_tareas_por_colaborador).pack(side="left", padx=4)

    # Fila 4 - Filtro por estado de tarea
    fila_filtro_estado = tk.Frame(marco_filtros)
    fila_filtro_estado.grid(row=3, column=0, columnspan=6, sticky="w", pady=4)
    tk.Label(fila_filtro_estado, text="Tareas por estado:").pack(side="left", padx=5)
    combo_filtro_estado_tarea = ttk.Combobox(fila_filtro_estado,
                                              values=["Todos"] + ESTADOS_TAREA,
                                              width=18, state="readonly")
    combo_filtro_estado_tarea.set("Todos")
    combo_filtro_estado_tarea.pack(side="left", padx=5)
    tk.Button(fila_filtro_estado, text="Filtrar", command=ejecutar_filtro_tareas_por_estado).pack(side="left", padx=4)

    # Fila 5 - Filtro por rango de fechas
    fila_filtro_fechas = tk.Frame(marco_filtros)
    fila_filtro_fechas.grid(row=4, column=0, columnspan=6, sticky="w", pady=4)
    tk.Label(fila_filtro_fechas, text="Proyectos iniciados entre:").pack(side="left", padx=5)
    entrada_fecha_inicio_filtro = tk.Entry(fila_filtro_fechas, width=12)
    entrada_fecha_inicio_filtro.pack(side="left", padx=3)
    tk.Label(fila_filtro_fechas, text="y").pack(side="left")
    entrada_fecha_fin_filtro = tk.Entry(fila_filtro_fechas, width=12)
    entrada_fecha_fin_filtro.pack(side="left", padx=3)
    tk.Label(fila_filtro_fechas, text="(YYYY-MM-DD)").pack(side="left", padx=3)
    tk.Button(fila_filtro_fechas, text="Filtrar", command=ejecutar_filtro_proyectos_por_fechas).pack(side="left", padx=4)

    etiqueta_resultado = tk.Label(ventana_reportes, text="Seleccione un reporte o filtro para comenzar.")
    etiqueta_resultado.pack(pady=3)

    marco_tabla = tk.LabelFrame(ventana_reportes, text="Resultados", padx=5, pady=5)
    marco_tabla.pack(fill="both", expand=True, padx=10, pady=5)

    tabla_resultado = ttk.Treeview(marco_tabla, show="headings", height=14)
    barra_h = ttk.Scrollbar(marco_tabla, orient="horizontal", command=tabla_resultado.xview)
    barra_v = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla_resultado.yview)
    tabla_resultado.configure(xscrollcommand=barra_h.set, yscrollcommand=barra_v.set)
    tabla_resultado.pack(side="left", fill="both", expand=True)
    barra_v.pack(side="right", fill="y")
    barra_h.pack(side="bottom", fill="x")
