import sqlite3

# Conexión a la base de datos
connect = sqlite3.connect('database/distriarbelaez.db')
conn = connect.cursor()

# Crear tabla "administrador"
conn.execute('''
CREATE TABLE IF NOT EXISTS administrador (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Crear tabla "productos"
conn.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
    precio INTEGER NOT NULL CHECK(precio >= 0),
    categoria TEXT NOT NULL,
    codigo_jerarquico TEXT UNIQUE NOT NULL
)
''')

# Crear tabla "ventas"
conn.execute('''
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    factura INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    nombre_cliente TEXT NOT NULL,
    nombre_articulo TEXT NOT NULL,
    precio INTEGER NOT NULL CHECK(precio >= 0),
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    subtotal INTEGER NOT NULL CHECK(subtotal >= 0),
    FOREIGN KEY (nombre_articulo) REFERENCES productos(nombre) ON DELETE CASCADE
)
''')

# Crear tabla "clientes"
conn.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_cliente TEXT NOT NULL,
    direccion TEXT,
    telefono TEXT UNIQUE,
    correo TEXT
)
''')

# Crear tabla "ajustes"
conn.execute('''
CREATE TABLE IF NOT EXISTS ajustes (
    clave TEXT PRIMARY KEY,
    valor TEXT
)
''')

# Insertar datos iniciales en "administrador"
try:
    conn.execute('''
    INSERT INTO administrador (usuario, password) 
    VALUES (?, ?)
    ''', ('admin', '123'))
except sqlite3.IntegrityError:
    pass

# Insertar datos iniciales en "ajustes"
try:
    conn.execute('''
    INSERT INTO ajustes (clave, valor)
    VALUES (?, ?)
    ''', ('nombre_impresora', 'Impresora Predeterminada'))
except sqlite3.IntegrityError:
    pass

# Guardar cambios y cerrar conexión
connect.commit()
connect.close()

print("Base de datos creada y actualizada correctamente.")
