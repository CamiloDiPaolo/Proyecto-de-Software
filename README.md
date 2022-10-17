# Grupo 21

# Pablo Gabriel Terrone 17554/1

# Facundo Odone 18648/1

# Joaquin Fontana 18569/3

# Camilo Di Paolo 18904/8

#-----------------------------------------
# Credenciales de usuario administrador:
# Username: admin
# Password: admin

#-----------------------------------------
# Comandos para recrear DB:

##CREATE TABLE configuracion (
###    id SERIAL PRIMARY KEY,
###    elementos_por_pag INT,
###    tabla_pagos BOOLEAN,
###    contacto BOOLEAN,
###    encabezado_pago VARCHAR(255),
###    valor_cuota_base REAL,
###    recargo_deuda REAL,
###    moneda VARCHAR(255)
###);

##CREATE TABLE usuario(
###    id SERIAL PRIMARY KEY,
###    email VARCHAR(255),
###    username VARCHAR(255),
###    contraseña VARCHAR(255),
###    activo boolean,
###    ultima_actualizacion DATE,
###    creacion DATE,
###    nombre VARCHAR(255),
###    apellido VARCHAR(255)
###);

##CREATE TABLE usuario_tiene_rol(
###    id SERIAL PRIMARY KEY,
###    usuario_id INT,
###    rol_id INT
###);

##CREATE TABLE rol(
###    id SERIAL PRIMARY KEY,
###    nombre VARCHAR(255)
###);

##CREATE TABLE rol_tiene_permiso(
###    id SERIAL PRIMARY KEY,
###    rol_id INT,
###    permiso_id INT
###);

##CREATE TABLE permiso(
###    id SERIAL PRIMARY KEY,
###   nombre VARCHAR(255)
###);

##CREATE TABLE socio(
###    id SERIAL PRIMARY KEY,
###    email VARCHAR(255),
###    nombre VARCHAR(255),
###    apellido VARCHAR(255),
###   tipo_documento VARCHAR(255),
###    nro_documento VARCHAR(255),
###    genero VARCHAR(255),
###    nro_socio INT UNIQUE,
###    direccion VARCHAR(255),
###    estado BOOLEAN,
###    telefono VARCHAR(255),
###    fecha_alta DATE
##);

##CREATE TABLE socio_subscrito_disciplina(
###    id_disciplina INT,
###    id_socio INT
###);

##CREATE TABLE disciplina(
###    id SERIAL PRIMARY KEY,
###    nombre VARCHAR(255),
###    categoria_id INT,
###    instructores VARCHAR(255),
###    horarios VARCHAR(255),
###    costo REAL,
###    habilitada BOOLEAN
###);

##CREATE TABLE categoria(
###    id SERIAL PRIMARY KEY,
###    nombre VARCHAR(255)
###);

##CREATE TABLE pago(
###    id SERIAL PRIMARY KEY,
###    id_socio INT,
###    pago REAL,
###    fecha DATE
###);
