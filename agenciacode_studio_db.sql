-- ============================================================
--   AgenciaCode Studio — Script de Base de Datos
--   Proyecto 9 — Sistema de Gestión de Proyectos de Desarrollo
-- ============================================================

CREATE DATABASE IF NOT EXISTS agenciacode_studio
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE agenciacode_studio;

-- Tabla: colaborador
CREATE TABLE IF NOT EXISTS colaborador (
    id_colaborador        INT AUTO_INCREMENT PRIMARY KEY,
    nombre                VARCHAR(50)  NOT NULL,
    apellido              VARCHAR(50)  NOT NULL,
    rol_colaborador       VARCHAR(50)  NOT NULL COMMENT 'Desarrollador, Diseñador, Analista',
    especialidad          VARCHAR(100) NOT NULL,
    estado_disponibilidad VARCHAR(20)  NOT NULL DEFAULT 'Activo' COMMENT 'Activo, Inactivo'
);

-- Tabla: usuario (autenticación)
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario      INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario  VARCHAR(25)  NOT NULL UNIQUE,
    email           VARCHAR(100) NOT NULL UNIQUE,
    contrasena      VARCHAR(255) NOT NULL,
    rol_sistema     VARCHAR(20)  NOT NULL DEFAULT 'Estandar' COMMENT 'Admin, Estandar',
    id_colaborador  INT          NOT NULL UNIQUE,
    CONSTRAINT fk_usuario_colaborador
        FOREIGN KEY (id_colaborador) REFERENCES colaborador(id_colaborador)
);

-- Tabla: cliente
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente   INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(50)  NOT NULL,
    apellido     VARCHAR(50)  NOT NULL,
    empresa      VARCHAR(100),
    sector       VARCHAR(50)  NOT NULL,
    telefono     VARCHAR(20)  NOT NULL,
    email        VARCHAR(100) NOT NULL UNIQUE,
    estado       VARCHAR(10)  NOT NULL DEFAULT 'Activo' COMMENT 'Activo, Inactivo'
);

-- Tabla: proyecto
CREATE TABLE IF NOT EXISTS proyecto (
    id_proyecto         INT AUTO_INCREMENT PRIMARY KEY,
    nombre_proyecto     VARCHAR(100) NOT NULL,
    descripcion         VARCHAR(255) NOT NULL,
    fecha_inicio        DATE         NOT NULL,
    fecha_fin_estimada  DATE         NOT NULL,
    fecha_fin_real      DATE         DEFAULT NULL,
    estado              VARCHAR(20)  NOT NULL DEFAULT 'En Proceso' COMMENT 'En Proceso, Completado, Cancelado',
    id_cliente          INT          NOT NULL,
    CONSTRAINT fk_proyecto_cliente
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

-- Tabla: asignacion_proyecto (N:N entre colaborador y proyecto)
CREATE TABLE IF NOT EXISTS asignacion_proyecto (
    id_asignacion      INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto        INT         NOT NULL,
    id_colaborador     INT         NOT NULL,
    fecha_vinculacion  DATE        NOT NULL,
    rol_en_proyecto    VARCHAR(50) NOT NULL DEFAULT 'Desarrollador',
    estado_asignacion  VARCHAR(20) NOT NULL DEFAULT 'Activo' COMMENT 'Activo, Inactivo',
    CONSTRAINT fk_asignacion_proyecto
        FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto),
    CONSTRAINT fk_asignacion_colaborador
        FOREIGN KEY (id_colaborador) REFERENCES colaborador(id_colaborador),
    CONSTRAINT uc_colaborador_proyecto UNIQUE (id_proyecto, id_colaborador)
);

-- Tabla: tarea
CREATE TABLE IF NOT EXISTS tarea (
    id_tarea        INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tarea    VARCHAR(100) NOT NULL,
    descripcion     VARCHAR(255) NOT NULL,
    prioridad       VARCHAR(20)  NOT NULL DEFAULT 'Media' COMMENT 'Alta, Media, Baja',
    estado          VARCHAR(20)  NOT NULL DEFAULT 'Pendiente' COMMENT 'Pendiente, En Progreso, En Revision, Completada, Cancelada',
    fecha_inicio    DATE         NOT NULL,
    fecha_entrega   DATE         NOT NULL,
    id_proyecto     INT          NOT NULL,
    id_colaborador  INT          NOT NULL,
    CONSTRAINT fk_tarea_proyecto
        FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto),
    CONSTRAINT fk_tarea_colaborador
        FOREIGN KEY (id_colaborador) REFERENCES colaborador(id_colaborador)
);

-- Tabla: sub_tarea
CREATE TABLE IF NOT EXISTS sub_tarea (
    id_sub_tarea  INT AUTO_INCREMENT PRIMARY KEY,
    descripcion   VARCHAR(255) NOT NULL,
    estado        VARCHAR(20)  NOT NULL DEFAULT 'Pendiente' COMMENT 'Pendiente, Completada',
    id_tarea      INT          NOT NULL,
    CONSTRAINT fk_sub_tarea_tarea
        FOREIGN KEY (id_tarea) REFERENCES tarea(id_tarea)
);

-- ============================================================
-- DATOS DE PRUEBA
-- ============================================================

INSERT INTO colaborador (nombre, apellido, rol_colaborador, especialidad, estado_disponibilidad) VALUES
('Carlos',  'Ramirez', 'Desarrollador', 'Backend Python',    'Activo'),
('Laura',   'Torres',  'Diseñador',     'UI/UX y Frontend',  'Activo'),
('Miguel',  'Herrera', 'Analista',      'Base de Datos',     'Activo'),
('Sofia',   'Mendoza', 'Desarrollador', 'Frontend React',    'Activo'),
('Andres',  'Paredes', 'Desarrollador', 'DevOps y Redes',    'Inactivo');

INSERT INTO usuario (nombre_usuario, email, contrasena, rol_sistema, id_colaborador) VALUES
('admin',    'admin@agenciacode.co',   'admin123',  'Admin',    1),
('laura_t',  'laura@agenciacode.co',  'pass456',   'Estandar', 2),
('miguel_h', 'miguel@agenciacode.co', 'pass789',   'Estandar', 3),
('sofia_m',  'sofia@agenciacode.co',  'pass321',   'Estandar', 4);

INSERT INTO cliente (nombre, apellido, empresa, sector, telefono, email, estado) VALUES
('Juan',    'Perez',  'Tienda JuanP',    'Retail',     '3001234567', 'juan@empresa.co',   'Activo'),
('Maria',   'Lopez',  'Clinica Salud',   'Salud',      '3109876543', 'maria@clinica.co',  'Activo'),
('Roberto', 'Gomez',  'LogiTrans SAS',   'Logistica',  '3207894561', 'roberto@logis.co',  'Activo'),
('Elena',   'Castro', 'Instituto FORMS', 'Educacion',  '3016541230', 'elena@edu.co',      'Inactivo');

INSERT INTO proyecto (nombre_proyecto, descripcion, fecha_inicio, fecha_fin_estimada, estado, id_cliente) VALUES
('Portal E-commerce',       'Tienda en linea con carrito y pagos',         '2025-01-10', '2025-06-30', 'En Proceso',  1),
('Sistema de Citas',        'Agendamiento de citas para clinica',           '2025-02-01', '2025-07-15', 'En Proceso',  2),
('App de Rastreo GPS',      'Seguimiento de envios en tiempo real',         '2025-03-01', '2025-09-01', 'En Proceso',  3),
('Plataforma E-learning',   'Cursos en linea con videos y evaluaciones',    '2024-10-01', '2025-01-31', 'Completado',  4);

INSERT INTO asignacion_proyecto (id_proyecto, id_colaborador, fecha_vinculacion, rol_en_proyecto, estado_asignacion) VALUES
(1, 1, '2025-01-10', 'Lider',        'Activo'),
(1, 2, '2025-01-12', 'Desarrollador','Activo'),
(2, 3, '2025-02-01', 'Desarrollador','Activo'),
(3, 1, '2025-03-01', 'Desarrollador','Activo'),
(3, 4, '2025-03-03', 'Diseñador',    'Activo');

INSERT INTO tarea (nombre_tarea, descripcion, prioridad, estado, fecha_inicio, fecha_entrega, id_proyecto, id_colaborador) VALUES
('Diseño base de datos',  'Modelar y crear esquema MySQL',         'Alta',  'Completada',  '2025-01-10', '2025-01-25', 1, 1),
('Desarrollo API REST',   'Crear endpoints para productos',        'Alta',  'En Progreso', '2025-01-26', '2025-03-15', 1, 1),
('Maquetacion UI',        'Diseñar pantallas principales',         'Media', 'En Progreso', '2025-02-01', '2025-03-30', 1, 2),
('Modulo agendamiento',   'CRUD de citas con calendario',          'Alta',  'Pendiente',   '2025-02-10', '2025-04-20', 2, 3),
('Integracion GPS',       'Conectar API de mapas',                 'Media', 'Pendiente',   '2025-03-05', '2025-06-01', 3, 1);

INSERT INTO sub_tarea (descripcion, estado, id_tarea) VALUES
('Crear diagrama ER',                    'Completada',  1),
('Ejecutar script de tablas',            'Completada',  1),
('Poblar datos de prueba',               'Completada',  1),
('Crear endpoint GET /productos',        'Completada',  2),
('Crear endpoint POST /pedidos',         'Pendiente',   2),
('Implementar autenticacion JWT',        'Pendiente',   2);
