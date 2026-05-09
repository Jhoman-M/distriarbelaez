import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from theme.colores import color_fondo_inventario, color_fondo_buscar_inventario

# Interfaz de clientes
class clientes_main():
    def __init__(self, cuerpo_principal):
        self.marco_titulo = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario, height=40)
        self.marco_titulo.pack(side=tk.TOP, fill='both')

        self.marco_registro = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario, height=50)
        self.marco_registro.pack(side=tk.TOP, fill='both', pady=10)

        self.marco_acciones = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario, height=50)
        self.marco_acciones.pack(side=tk.TOP, fill='both')

        self.marco_productos = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario)
        self.marco_productos.pack(side=tk.TOP, fill='both', padx=30, pady=15, expand=True)

        title = ctk.CTkLabel(self.marco_titulo, text="CLIENTES", font=('Roboto', 20), fg_color="#485159", text_color=color_fondo_buscar_inventario, pady=20)
        title.pack(expand=True, fill=tk.BOTH)

        etiqueta_id = tk.Label(self.marco_registro, text="Id:", font=('Roboto', 14), fg="#666a88", bg=color_fondo_inventario, width=5)
        etiqueta_id.pack(side="left", padx=5, pady=10)

        self.campo_id = ttk.Entry(self.marco_registro, font=('Roboto', 14), state="readonly", width=5)
        self.campo_id.pack(side="left", padx=5, pady=10)

        etiqueta_nombre = tk.Label(self.marco_registro, text="Cliente:", font=('Roboto', 14), fg="#666a88", bg=color_fondo_inventario)
        etiqueta_nombre.pack(side="left", padx=5, pady=10)
        self.campo_nombre = ttk.Entry(self.marco_registro, font=('Roboto', 14))
        self.campo_nombre.pack(side="left", padx=5, pady=10)
        
        etiqueta_direccion = tk.Label(self.marco_registro, text="Direccion:", font=('Roboto', 14), fg="#666a88", bg=color_fondo_inventario)
        etiqueta_direccion.pack(side="left", padx=5, pady=10)
        self.campo_direccion = ttk.Entry(self.marco_registro, font=('Roboto', 14))
        self.campo_direccion.pack(side="left", padx=5, pady=10)

        etiqueta_telefono = tk.Label(self.marco_registro, text="Telefono:", font=('Roboto', 14), fg="#666a88", bg=color_fondo_inventario)
        etiqueta_telefono.pack(side="left", padx=5, pady=10)
        self.campo_telefono = ttk.Entry(self.marco_registro, font=('Times', 14))
        self.campo_telefono.pack(side="left", padx=5, pady=10)

        self.boton_registro = ctk.CTkButton(self.marco_acciones,text="Registrar",font=('Roboto', 14),fg_color='#1c84cd',text_color="#fff",
        corner_radius=8,hover_color="#2871a4",border_width=2,border_color="#2871a4",command=self.registrar_producto)
        self.boton_registro.pack(side=tk.LEFT, padx=5)

        self.boton_eliminar = ctk.CTkButton(self.marco_acciones, text="Eliminar", font=('Roboto', 14), fg_color='#bd0507', text_color="#fff",
        corner_radius=8,hover_color="#a42123",border_width=2,border_color="#a42123", command=self.eliminar_producto)
        self.boton_eliminar.pack(side=tk.LEFT, padx=5)

        self.boton_modificar = ctk.CTkButton(self.marco_acciones, text="Modificar", font=('Roboto', 14), fg_color='#536270',text_color="#fff", 
        corner_radius=8,hover_color="#374048",border_width=2,border_color="#374048",command=self.modificar_producto)
        self.boton_modificar.pack(side=tk.LEFT, padx=5)

        self.boton_limpiar_campos = ctk.CTkButton(self.marco_acciones, text="Limpiar Campos", font=('Roboto', 14), fg_color='#1e3cd1',text_color="#fff",
        corner_radius=8,hover_color="#21359c",border_width=2,border_color="#21359c",command=self.limpiar_campos)
        self.boton_limpiar_campos.pack(side=tk.LEFT, padx=5)

        # Tabla de clientes
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#000",borderwidth=1,relief="flat", font=('Roboto', 14))
        style.configure('Treeview.Heading', background="#2E3B4E", foreground="#fff",borderwidth=1,relief="flat", font=('Roboto', 14,'bold'))



        self.tree = ttk.Treeview(self.marco_productos, show='headings')
        self.tree['columns'] = ('Id', 'Nombre', 'direccion', 'telefono')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Id', anchor=tk.CENTER, width=25)
        self.tree.column('Nombre', anchor=tk.CENTER, width=200)
        self.tree.column('direccion', anchor=tk.CENTER, width=100)
        self.tree.column('telefono', anchor=tk.CENTER, width=100)

        self.tree.heading('#0', text='')
        self.tree.heading('Id', text='Id')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('direccion', text='Direccion')
        self.tree.heading('telefono', text='Telefono')
        self.tree.pack(expand=True, fill='both')
        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar_treeview)

        self.tree.tag_configure('oddrow', background='#f6f9ff') 
        self.tree.tag_configure('evenrow', background='#e8f1ff') 

        # Conectar a base de datos
        self.conectar_db()
        self.actualizar_lista()
        
    def conectar_db(self):
        self.conn = sqlite3.connect('database/distriarbelaez.db')
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def registrar_producto(self):
        nombre_cliente = self.campo_nombre.get()
        direccion = self.campo_direccion.get()
        telefono = self.campo_telefono.get()

        if nombre_cliente:
            try:
                self.cursor.execute("INSERT INTO clientes (nombre_cliente, direccion, telefono) VALUES (?, ?, ?)",
                                    (nombre_cliente, direccion if direccion else '', telefono if telefono else ''))
                self.conn.commit()
                self.actualizar_lista()
                self.limpiar_campos()
                messagebox.showinfo("Registro exitoso", "Cliente registrado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")
        else:
            messagebox.showwarning("Campo obligatorio", "Por favor, ingresa el nombre del cliente.")
    
    def actualizar_lista(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT * FROM clientes")
        clientes = self.cursor.fetchall()
        count = 0
        for cliente in clientes:
            if count % 2 == 0:
                self.tree.insert('', tk.END, values=(cliente[0], cliente[1], cliente[2], cliente[3]), tags=('evenrow',))
            else:
                self.tree.insert('', tk.END, values=(cliente[0], cliente[1], cliente[2], cliente[3]), tags=('oddrow',))
            count += 1

    def eliminar_producto(self):
        selected = self.tree.selection()
        if selected:
            cliente_id = self.tree.item(selected)['values'][0]
            try:
                self.cursor.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
                self.conn.commit()
                self.actualizar_lista()
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")
        else:
            messagebox.showwarning("Selecciona un cliente", "Por favor, selecciona un cliente para eliminar.")

    def modificar_producto(self):
        selected = self.tree.selection()
        if selected:
            cliente_id = self.tree.item(selected)['values'][0]
            nombre_cliente = self.campo_nombre.get()
            direccion = self.campo_direccion.get()
            telefono = self.campo_telefono.get()

            try:
                self.cursor.execute("UPDATE clientes SET nombre_cliente=?, direccion=?, telefono=? WHERE id=?", (nombre_cliente, direccion, telefono, cliente_id))
                self.conn.commit()
                self.actualizar_lista()
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo modificar el cliente: {e}")
        else:
            messagebox.showwarning("Selecciona un cliente", "Por favor, selecciona un cliente para modificar.")

    def limpiar_campos(self):
        self.campo_id.config(state=tk.NORMAL)
        self.campo_id.delete(0, tk.END)
        self.campo_nombre.delete(0, tk.END)
        self.campo_direccion.delete(0, tk.END)
        self.campo_telefono.delete(0, tk.END)
        self.campo_id.config(state="readonly")

    def al_seleccionar_treeview(self, event):
        selected = self.tree.selection()
        if selected:
            cliente = self.tree.item(selected)['values']
            self.campo_id.config(state=tk.NORMAL)
            self.campo_id.delete(0, tk.END)
            self.campo_id.insert(0, cliente[0])
            self.campo_id.config(state="readonly")
            self.campo_nombre.delete(0, tk.END)
            self.campo_nombre.insert(0, cliente[1])
            self.campo_direccion.delete(0, tk.END)
            self.campo_direccion.insert(0, cliente[2])
            self.campo_telefono.delete(0, tk.END)
            self.campo_telefono.insert(0, cliente[3])
