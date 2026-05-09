import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from theme.colores import color_fondo_inventario, color_fondo_buscar_inventario


class ajustes_main:
    def __init__(self, cuerpo_principal):
        self.cuerpo_principal = cuerpo_principal

        # Marco principal
        self.marco_principal = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario, corner_radius=10)
        self.marco_principal.pack(expand=True, fill='both')

        self.marco_titulo = ctk.CTkFrame(self.marco_principal, fg_color=color_fondo_inventario, height=40)
        self.marco_titulo.pack(side=tk.TOP, fill='x')

        title = ctk.CTkLabel(
            self.marco_titulo,
            text="AJUSTES",
            font=('Roboto', 20),
            fg_color="#485159",
            text_color=color_fondo_buscar_inventario,
            pady=20
        )
        title.pack(expand=True, fill=tk.BOTH)

        # Marco de configuración
        self.marco_registro = ctk.CTkFrame(self.marco_principal, fg_color=color_fondo_buscar_inventario, corner_radius=10)
        self.marco_registro.pack(side=tk.TOP, expand=True, fill='both', padx=10, pady=10)

        # Campos de configuración general
        self.textos_labels = [
            "Nombre de la impresora",
            "Nombre Propietario",
            "NIT",
            "Dirección",
            "Teléfono",
            "Usuario", 
            "Contraseña"  
        ]
        self.textos_claves = [
            "nombre_impresora",
            "nombre",
            "nit",
            "direccion",
            "telefono",
            "usuario",  
            "contrasena" 
        ]
        self.textos_entries = {}

        for idx, label_text in enumerate(self.textos_labels):
            label = ctk.CTkLabel(self.marco_registro, text=f"{label_text}:", text_color="#333333", font=('Roboto', 14))
            label.grid(row=idx, column=0, pady=10, padx=15, sticky="w")
            entry = ctk.CTkEntry(self.marco_registro, font=('Roboto', 14), width=300, corner_radius=10)
            entry.grid(row=idx, column=1, pady=10, padx=15)
            self.textos_entries[self.textos_claves[idx]] = entry

        # Ocultar la contraseña con asteriscos
        self.textos_entries["contrasena"].configure(show="*")

        # Cargar los valores actuales desde la base de datos
        self.cargar_datos()

        # Marco de acciones (botones)
        self.marco_acciones = ctk.CTkFrame(self.marco_principal, fg_color=color_fondo_inventario, height=50, corner_radius=10)
        self.marco_acciones.pack(side=tk.BOTTOM, fill='x', padx=10, pady=10)

        # Botón para guardar cambios
        self.boton_guardar = ctk.CTkButton(
            self.marco_acciones,
            text="Guardar cambios",
            command=self.mostrar_ventana_autenticacion,
            font=('Roboto', 14),
            fg_color="#1c84cd",
            hover_color="#2d73a4",
            corner_radius=8,
            border_width=2,
            border_color="#2d73a4"
        )
        self.boton_guardar.pack(side=tk.RIGHT, padx=15, pady=10)

    def cargar_datos(self):
        """Cargar los datos desde la base de datos."""
        try:
            conexion = sqlite3.connect("database/distriarbelaez.db")
            cursor = conexion.cursor()

            # Cargar datos de la tabla "ajustes"
            for clave in self.textos_claves:
                if clave in ["usuario", "contrasena"]:
                    continue 
                cursor.execute("SELECT valor FROM ajustes WHERE clave = ?", (clave,))
                resultado = cursor.fetchone()
                if resultado:
                    self.textos_entries[clave].insert(0, resultado[0])

            # Cargar datos de la tabla "administrador"
            cursor.execute("SELECT usuario, password FROM administrador WHERE id = 1")
            resultado = cursor.fetchone()
            if resultado:
                self.textos_entries["usuario"].insert(0, resultado[0])
                self.textos_entries["contrasena"].insert(0, resultado[1])

            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

    def mostrar_ventana_autenticacion(self):
        """Mostrar una ventana de autenticación personalizada."""
        self.ventana_autenticacion = ctk.CTkToplevel(self.cuerpo_principal)
        self.ventana_autenticacion.title("Autenticación")
        self.ventana_autenticacion.geometry("350x170+500+150")
        self.ventana_autenticacion.resizable(False, False)
        self.ventana_autenticacion.transient(self.cuerpo_principal)
        self.ventana_autenticacion.grab_set() 

        # Marco de la ventana de autenticación
        marco_autenticacion = ctk.CTkFrame(self.ventana_autenticacion, fg_color="#f0f0f0", corner_radius=10)
        marco_autenticacion.pack(expand=True, fill='both', padx=10, pady=10)

        # Campo de usuario
        label_usuario = ctk.CTkLabel(marco_autenticacion, text="Usuario:", text_color="#333333", font=('Roboto', 14))
        label_usuario.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.entry_usuario = ctk.CTkEntry(marco_autenticacion, font=('Roboto', 14), width=200, corner_radius=10)
        self.entry_usuario.grid(row=0, column=1, pady=10, padx=10)

        # Campo de contraseña
        label_contrasena = ctk.CTkLabel(marco_autenticacion, text="Contraseña:", text_color="#333333", font=('Roboto', 14))
        label_contrasena.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.entry_contrasena = ctk.CTkEntry(marco_autenticacion, font=('Roboto', 14), width=200, corner_radius=10, show="*")
        self.entry_contrasena.grid(row=1, column=1, pady=10, padx=10)

        # Botón de autenticación
        boton_autenticar = ctk.CTkButton(
            marco_autenticacion,
            text="Autenticar",
            command=self.verificar_autenticacion,
            font=('Roboto', 14),
            fg_color="#1c84cd",
            hover_color="#2d73a4",
            corner_radius=8,
            border_width=2,
            border_color="#2d73a4"
        )
        boton_autenticar.grid(row=2, column=0, columnspan=2, pady=20)

    def verificar_autenticacion(self):
        """Verificar las credenciales ingresadas."""
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if usuario and contrasena:
            if self.validar_credenciales(usuario, contrasena):
                self.ventana_autenticacion.destroy()  # Cerrar la ventana de autenticación
                self.guardar_datos()  # Guardar cambios si las credenciales son correctas
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        else:
            messagebox.showwarning("Advertencia", "Debe ingresar usuario y contraseña.")

    def validar_credenciales(self, usuario, contrasena):
        """Validar las credenciales del usuario."""
        try:
            conexion = sqlite3.connect("database/distriarbelaez.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT password FROM administrador WHERE usuario = ?", (usuario,))
            resultado = cursor.fetchone()
            conexion.close()

            if resultado and resultado[0] == contrasena:
                return True  # Credenciales correctas
            return False  # Credenciales incorrectas
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron validar las credenciales: {e}")
            return False

    def guardar_datos(self):
        """Guardar los valores actualizados en la base de datos."""
        try:
            conexion = sqlite3.connect("database/distriarbelaez.db")
            cursor = conexion.cursor()

            # Guardar datos en la tabla "ajustes"
            for clave, entry in self.textos_entries.items():
                if clave in ["usuario", "contrasena"]:
                    continue  # No guardar usuario y contraseña en ajustes
                nuevo_valor = entry.get().strip()
                if nuevo_valor:
                    cursor.execute("REPLACE INTO ajustes (clave, valor) VALUES (?, ?)", (clave, nuevo_valor))

            # Guardar datos en la tabla "administrador"
            nuevo_usuario = self.textos_entries["usuario"].get().strip()
            nueva_contrasena = self.textos_entries["contrasena"].get().strip()

            if nuevo_usuario and nueva_contrasena:
                cursor.execute("UPDATE administrador SET usuario = ?, password = ? WHERE id = 1", (nuevo_usuario, nueva_contrasena))

            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Los ajustes se han guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los ajustes: {e}")
            