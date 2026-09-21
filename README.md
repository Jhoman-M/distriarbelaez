Distriarbelaez v1.2

Sistema de gestión comercial en Python (Tkinter/CustomTkinter) y SQLite. Administra inventario, facturación, clientes y reportes.

Descripción

Aplicación de escritorio para el control de inventario, ventas con tickets en PDF e impresión térmica, gestión de clientes y reportes exportables a Excel.

Nota: La impresión directa requiere Windows e impresora térmica compatible con win32print.

Módulos

Módulo                   Descripción
Autenticación            Acceso con usuario y contraseña
Inventario               CRUD de productos y búsqueda en tiempo real
Facturación              Ventas, control de stock, tickets y PDF
Clientes                 Registro y administración de clientes
Reportes                 Ventas y productos más vendidos (exportable a Excel)
Ajustes                  Datos del negocio, impresora y credenciales

Requisitos

Python 3.10+, Windows (para impresión térmica) y las librerías: customtkinter, Pillow, tkcalendar, pandas, openpyxl, reportlab, fpdf, pywin32.

Instalación

Bash
git clone https://github.com/tu-usuario/distriarbelaez.git
cd distriarbelaez
pip install customtkinter Pillow tkcalendar pandas openpyxl reportlab fpdf pywin32
python database/crear_base.py
python main.py

Base de Datos

SQLite local (database/distriarbelaez.db) con las tablas: administrador, productos, ventas, clientes y ajustes.

Uso

Inicio de sesión: Ingresa credenciales en la pantalla de login.
Inventario: Registra, busca, modifica o elimina productos.
Facturación: Selecciona productos, define cantidades, procesa cobro, calcula cambio y genera comprobante.
Clientes: Administra datos de contacto.
Reportes: Filtra por fechas (más vendidos o total ventas) y exporta a Excel.
Ajustes: Modifica la configuración del negocio, impresora y acceso.

Credenciales por Defecto

Usuario: admin
Contraseña: 123

Autores

Jhoman Alejandro Martínez Arbelaez
