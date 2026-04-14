# AgenciaCode Studio
## Sistema de Gestión de Proyectos de Desarrollo

### Descripción
Sistema de escritorio para gestionar proyectos, clientes, colaboradores y tareas de una agencia de desarrollo de software. Permite registrar el avance de cada proyecto, asignar colaboradores, controlar estados y generar reportes de productividad.

### Módulos del Sistema
1. **Acceso al Sistema** — Login con validación de credenciales
2. **Gestión de Usuarios** — CRUD de usuarios del sistema (solo Admin)
3. **Gestión de Clientes** — Registro y control de clientes con estado activo/inactivo
4. **Gestión de Colaboradores** — Registro de colaboradores por rol y especialidad
5. **Gestión de Proyectos** — CRUD con filtros por estado y rango de fechas
6. **Gestión de Tareas** — CRUD con subtareas, prioridades y estados
7. **Asignaciones** — Relación N:N entre colaboradores y proyectos
8. **Consultas y Reportes** — JOIN completo, avance porcentual y filtros múltiples

### Reglas de Negocio Implementadas
- Un colaborador no puede tener más de 3 proyectos activos simultáneamente
- No se puede eliminar un cliente con proyectos activos (solo desactivar)
- No se puede marcar un proyecto como "Completado" con tareas pendientes
- No se puede eliminar un proyecto con tareas "En Progreso"
- Una tarea no puede marcarse "Completada" si tiene subtareas pendientes
- La fecha de entrega de una tarea no puede superar la fecha fin del proyecto

### Herramientas Usadas
- **Lenguaje:** Python 3.8+
- **Interfaz:** Tkinter (exclusivamente)
- **Base de datos:** MySQL
- **Conector:** mysql-connector-python
- **Arquitectura:** MVC con funciones (sin clases ni decoradores)

### Estructura del Proyecto
```
AgenciaCodeStudio/
├── config/
│   └── database_connection.py
├── controllers/
│   ├── user_controller.py
│   ├── client_controller.py
│   ├── project_controller.py
│   ├── task_controller.py
│   └── collaborator_controller.py
├── models/
│   ├── user_model.py
│   ├── client_model.py
│   ├── project_model.py
│   ├── task_model.py
│   ├── collaborator_model.py
│   └── assignment_model.py
├── views/
│   ├── login_view.py
│   ├── main_view.py
│   ├── client_view.py
│   ├── collaborator_view.py
│   ├── project_view.py
│   ├── task_view.py
│   ├── assignment_view.py
│   ├── user_view.py
│   └── report_view.py
├── agenciacode_studio_db.sql
├── main.py
└── README.md
```

### Instalación y Ejecución
1. Instalar dependencias:
   ```
   pip install mysql-connector-python
   ```
2. Crear la base de datos ejecutando el archivo `agenciacode_studio_db.sql` en MySQL
3. Configurar credenciales en `config/database_connection.py`
4. Ejecutar la aplicación:
   ```
   python main.py
   ```

### Credenciales de Prueba
| Usuario | Contraseña | Rol     |
|---------|------------|---------|
| admin   | admin123   | Admin   |
| laura_t | pass456    | Estandar|
| miguel_h| pass789    | Estandar|

### Autor
# Autor: Amy Gonzalez
