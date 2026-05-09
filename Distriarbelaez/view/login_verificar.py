import sqlite3

def verificar_login(usuario, password):
    conexion = sqlite3.connect('database/distriarbelaez.db')
    cursor = conexion.cursor()

    cursor.execute('''
    SELECT * FROM administrador WHERE usuario = ? AND password = ?
    ''', (usuario, password))

    resultado = cursor.fetchone()
    conexion.close()

    return resultado is not None
