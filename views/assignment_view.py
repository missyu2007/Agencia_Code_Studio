import tkinter as tk
from tkinter import ttk, messagebox
from controllers.collaborator_controller import (
    consultar_todas_las_asignaciones,
    consultar_asignaciones_por_proyecto,
    registrar_nueva_asignacion,
    modificar_asignacion_existente,
    eliminar_asignacion_existente,
    consultar_colaboradores_activos
)
from controllers.project_controller import consultar_todos_los_proyectos

ROLES_EN_PROYECTO = ["Lider", "Desarrollador", "Diseñador", "Tester", "Analista", "DevOps"]
ESTADOS_ASIGNACION = ["Activo", "Inactivo"]


def abrir_ventana_asignaciones(ventana_padre):
    ventana_asignaciones = tk.Toplevel(ventana_padre)
    ventana_asignaciones.title("Gestion de Asignaciones - Colaboradores por Proyecto")
    ventana_asignaciones.geometry("980x560")

    id_asignacion_seleccionada = {"valor": None}
    lista_proyectos_cargados = []
    lista_colaboradores_cargados = []

    def obtener_nombres_proyectos():
        nonlocal lista_proyectos_cargados
        lista_proyectos_cargados = consultar_todos_los_proyectos()
        return [f"{p['nombre_proyecto']} ({p['estado']})" for p in lista_proyectos_cargados]

    def obtener_nombres_colaboradores():
        nonlocal lista_colaboradores_cargados
        lista_colaboradores_cargados = consultar_colaboradores_activos()
        return [f"{c['nombre']} {c['apellido']} - {c['rol_colaborador']}"
                for c in lista_colaboradores_cargados]

    def obtener_id_proyecto():
        indice = combo_proyecto_asig.current()
        if indice < 0 or indice >= len(lista_proyectos_cargados):
            return None
        return lista_proyectos_cargados[indice]["id_proyecto"]

    def obtener_id_colaborador():
        indice = combo_colaborador_asig.current()
        if indice < 0 or indice >= len(lista_colaboradores_cargados):
            return None
        return lista_colaboradores_cargados[indice]["id_colaborador"]

    def cargar_asignaciones_en_tabla(lista_asignaciones=None):
        for fila in tabla_asignaciones.get_children():
            tabla_asignaciones.delete(fila)
        if lista_asignaciones is None:
            lista_asignaciones = consultar_todas_las_asignaciones()
        for asignacion in lista_asignaciones:
            tabla_asignaciones.insert("", "end", values=(
                asignacion["id_asignacion"],
                asignacion["nombre_proyecto"],
                asignacion["nombre_colaborador"],
                asignacion["rol_en_proyecto"],
                asignacion["fecha_vinculacion"],
                asignacion["estado_asignacion"]
            ))

    def limpiar_formulario():
        id_asignacion_seleccionada["valor"] = None
        combo_proyecto_asig.set("")
        combo_colaborador_asig.set("")
        entrada_fecha_vinculacion.delete(0, tk.END)
        combo_rol_en_proyecto.set(ROLES_EN_PROYECTO[0])
        combo_estado_asignacion.set(ESTADOS_ASIGNACION[0])

    def cargar_datos_en_formulario(evento):
        seleccion = tabla_asignaciones.selection()
        if not seleccion:
            return
        valores = tabla_asignaciones.item(seleccion[0])["values"]
        id_asignacion_seleccionada["valor"] = valores[0]
        combo_rol_en_proyecto.set(valores[3])
        entrada_fecha_vinculacion.delete(0, tk.END)
        entrada_fecha_vinculacion.insert(0, valores[4])
        combo_estado_asignacion.set(valores[5])

    def filtrar_por_proyecto():
        id_proyecto = obtener_id_proyecto()
        if not id_proyecto:
            cargar_asignaciones_en_tabla()
            return
        lista_filtrada = consultar_asignaciones_por_proyecto(id_proyecto)
        cargar_asignaciones_en_tabla(lista_filtrada)

    def guardar_nueva_asignacion():
        exito, mensaje = registrar_nueva_asignacion(
            obtener_id_proyecto(),
            obtener_id_colaborador(),
            entrada_fecha_vinculacion.get().strip(),
            combo_rol_en_proyecto.get(),
            combo_estado_asignacion.get()
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_asignaciones)
            limpiar_formulario()
            cargar_asignaciones_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_asignaciones)

    def actualizar_asignacion_seleccionada():
        if not id_asignacion_seleccionada["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione una asignacion.", parent=ventana_asignaciones)
            return
        exito, mensaje = modificar_asignacion_existente(
            id_asignacion_seleccionada["valor"],
            combo_rol_en_proyecto.get(),
            combo_estado_asignacion.get()
        )
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_asignaciones)
            limpiar_formulario()
            cargar_asignaciones_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_asignaciones)

    def eliminar_asignacion_seleccionada():
        if not id_asignacion_seleccionada["valor"]:
            messagebox.showwarning("Advertencia", "Seleccione una asignacion.", parent=ventana_asignaciones)
            return
        confirmar = messagebox.askyesno("Confirmar eliminacion",
                                        "¿Esta seguro de que desea eliminar esta asignacion?",
                                        parent=ventana_asignaciones)
        if not confirmar:
            return
        exito, mensaje = eliminar_asignacion_existente(id_asignacion_seleccionada["valor"])
        if exito:
            messagebox.showinfo("Exito", mensaje, parent=ventana_asignaciones)
            limpiar_formulario()
            cargar_asignaciones_en_tabla()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana_asignaciones)

    # --- Interfaz ---
    marco_formulario = tk.LabelFrame(ventana_asignaciones, text="Nueva Asignacion", padx=10, pady=8)
    marco_formulario.pack(fill="x", padx=10, pady=5)

    tk.Label(marco_formulario, text="Proyecto:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
    combo_proyecto_asig = ttk.Combobox(marco_formulario, values=obtener_nombres_proyectos(), width=28, state="readonly")
    combo_proyecto_asig.grid(row=0, column=1, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Colaborador:").grid(row=0, column=2, sticky="e", padx=5, pady=3)
    combo_colaborador_asig = ttk.Combobox(marco_formulario, values=obtener_nombres_colaboradores(), width=28, state="readonly")
    combo_colaborador_asig.grid(row=0, column=3, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Fecha Vinculacion (YYYY-MM-DD):").grid(row=1, column=0, sticky="e", padx=5, pady=3)
    entrada_fecha_vinculacion = tk.Entry(marco_formulario, width=14)
    entrada_fecha_vinculacion.grid(row=1, column=1, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Rol en Proyecto:").grid(row=1, column=2, sticky="e", padx=5, pady=3)
    combo_rol_en_proyecto = ttk.Combobox(marco_formulario, values=ROLES_EN_PROYECTO, width=16, state="readonly")
    combo_rol_en_proyecto.set(ROLES_EN_PROYECTO[0])
    combo_rol_en_proyecto.grid(row=1, column=3, sticky="w", pady=3)

    tk.Label(marco_formulario, text="Estado Asignacion:").grid(row=2, column=0, sticky="e", padx=5, pady=3)
    combo_estado_asignacion = ttk.Combobox(marco_formulario, values=ESTADOS_ASIGNACION, width=14, state="readonly")
    combo_estado_asignacion.set(ESTADOS_ASIGNACION[0])
    combo_estado_asignacion.grid(row=2, column=1, sticky="w", pady=3)

    marco_botones = tk.Frame(ventana_asignaciones)
    marco_botones.pack(pady=5)
    tk.Button(marco_botones, text="Nuevo", width=12, command=limpiar_formulario).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Guardar", width=12, command=guardar_nueva_asignacion).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Actualizar", width=12, command=actualizar_asignacion_seleccionada).pack(side="left", padx=4)
    tk.Button(marco_botones, text="Eliminar", width=12, command=eliminar_asignacion_seleccionada).pack(side="left", padx=4)

    marco_filtro = tk.Frame(ventana_asignaciones)
    marco_filtro.pack(pady=2)
    tk.Label(marco_filtro, text="Ver asignaciones del proyecto:").pack(side="left", padx=5)
    tk.Button(marco_filtro, text="Filtrar por Proyecto Seleccionado", command=filtrar_por_proyecto).pack(side="left", padx=5)
    tk.Button(marco_filtro, text="Mostrar Todas", command=lambda: cargar_asignaciones_en_tabla()).pack(side="left", padx=5)

    marco_tabla = tk.LabelFrame(ventana_asignaciones, text="Lista de Asignaciones", padx=5, pady=5)
    marco_tabla.pack(fill="both", expand=True, padx=10, pady=5)

    columnas_tabla = ("ID", "Proyecto", "Colaborador", "Rol en Proyecto", "Fecha Vinculacion", "Estado")
    tabla_asignaciones = ttk.Treeview(marco_tabla, columns=columnas_tabla, show="headings", height=12)
    anchos = [40, 240, 200, 130, 130, 90]
    for nombre_columna, ancho in zip(columnas_tabla, anchos):
        tabla_asignaciones.heading(nombre_columna, text=nombre_columna)
        tabla_asignaciones.column(nombre_columna, width=ancho)

    barra_desplazamiento = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla_asignaciones.yview)
    tabla_asignaciones.configure(yscrollcommand=barra_desplazamiento.set)
    tabla_asignaciones.pack(side="left", fill="both", expand=True)
    barra_desplazamiento.pack(side="right", fill="y")

    tabla_asignaciones.bind("<<TreeviewSelect>>", cargar_datos_en_formulario)
    cargar_asignaciones_en_tabla()
