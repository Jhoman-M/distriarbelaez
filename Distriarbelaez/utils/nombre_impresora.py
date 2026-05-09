import sqlite3

def obtener_nombre_impresora():
        try:
            conexion = sqlite3.connect("database/distriarbelaez.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT valor FROM ajustes WHERE clave = 'nombre_impresora'")
            resultado = cursor.fetchone()
            conexion.close()
    
            if resultado:
                return resultado[0]
            else:
                return None
        except Exception as e:
            print(f"Error al obtener el nombre de la impresora: {e}")
            return None
