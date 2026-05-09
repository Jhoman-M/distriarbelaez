import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from theme.colores import color_fondo_inventario, color_fondo_buscar_inventario

class inventario_main():
    def __init__(self, cuerpo_principal):
        # Configuración inicial de los marcos
        self.marco_titulo = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario, height=40)
        self.marco_titulo.pack(side=tk.TOP, fill='both')

        self.marco_registro = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario, height=50)
        self.marco_registro.pack(side=tk.TOP, fill='both', pady=10)

        self.marco_acciones = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario, height=50)
        self.marco_acciones.pack(side=tk.TOP, fill='both')

        self.marco_productos = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario)
        self.marco_productos.pack(side=tk.TOP, fill='both', padx=30, pady=15, expand=True)

        # Título
        title = ctk.CTkLabel(self.marco_titulo, text="INVENTARIO", font=('Roboto', 20), 
                            fg_color="#485159", text_color=color_fondo_buscar_inventario, pady=20)
        title.pack(expand=True, fill=tk.BOTH)

        # Campos de registro
        etiqueta_nombre = tk.Label(self.marco_registro, text="Producto:", 
                                  font=('Roboto', 13), fg="#666a88", bg=color_fondo_inventario)
        etiqueta_nombre.pack(side="left", padx=5, pady=10)
        self.campo_nombre = ttk.Entry(self.marco_registro, font=('Roboto', 13),width=15)
        self.campo_nombre.pack(side="left", padx=5, pady=10)

        etiqueta_cantidad = tk.Label(self.marco_registro, text="Cantidad:", 
                                    font=('Roboto', 13), fg="#666a88", bg=color_fondo_inventario)
        etiqueta_cantidad.pack(side="left", padx=5, pady=10)
        self.campo_cantidad = ttk.Entry(self.marco_registro, font=('Roboto', 13),width=15)
        self.campo_cantidad.pack(side="left", padx=5, pady=10)

        etiqueta_precio = tk.Label(self.marco_registro, text="Precio:", 
                                  font=('Roboto', 13), fg="#666a88", bg=color_fondo_inventario)
        etiqueta_precio.pack(side="left", padx=5, pady=10)
        self.campo_precio = ttk.Entry(self.marco_registro, font=('Roboto', 13),width=15)
        self.campo_precio.pack(side="left", padx=5, pady=10)

        # Combobox para categorías
        self.categorias = ["Cerveza", "Vino", "Licor", "Gaseosa", "Agua", "Jugo", "Energizante"]
        etiqueta_categoria = tk.Label(self.marco_registro, text="Categoría:", 
                                     font=('Roboto', 13), fg="#666a88", bg=color_fondo_inventario)
        etiqueta_categoria.pack(side="left", padx=5, pady=10)

        self.combo_categoria = ttk.Combobox(self.marco_registro, font=('Roboto', 13), values=self.categorias,width=15)
        self.combo_categoria.pack(side="left", padx=5, pady=10)

        # Botones de acciones
        self.boton_registro = ctk.CTkButton(self.marco_acciones, text="Registrar", font=('Roboto', 13), 
                                           fg_color='#1c84cd', text_color="#fff", corner_radius=8, 
                                           hover_color="#2871a4", border_width=2, border_color="#2871a4", 
                                           command=self.registrar_producto)
        self.boton_registro.pack(side=tk.LEFT, padx=5)

        self.boton_eliminar = ctk.CTkButton(self.marco_acciones, text="Eliminar", font=('Roboto', 13), 
                                          fg_color='#bd0507', text_color="#fff", corner_radius=8, 
                                          hover_color="#a42123", border_width=2, border_color="#a42123", 
                                          command=self.eliminar_producto)
        self.boton_eliminar.pack(side=tk.LEFT, padx=5)

        self.boton_modificar = ctk.CTkButton(self.marco_acciones, text="Modificar", font=('Roboto', 13), 
                                           fg_color='#536270', text_color="#fff", corner_radius=8, 
                                           hover_color="#374048", border_width=2, border_color="#374048", 
                                           command=self.modificar_producto)
        self.boton_modificar.pack(side=tk.LEFT, padx=5)

        self.boton_limpiar_campos = ctk.CTkButton(self.marco_acciones, text="Limpiar Campos", font=('Roboto', 13), 
                                                 fg_color='#1e3cd1', text_color="#fff", corner_radius=8, 
                                                 hover_color="#21359c", border_width=2, border_color="#21359c", 
                                                 command=self.limpiar_campos)
        self.boton_limpiar_campos.pack(side=tk.LEFT, padx=5)



        self.boton_buscar = ctk.CTkButton(self.marco_acciones, text="Buscar", font=('Roboto', 13), 
                                         fg_color='#1e3cd1', text_color="#fff", corner_radius=8, 
                                         hover_color="#21359c", border_width=2, border_color="#21359c", 
                                         command=self.buscar_producto)
        self.boton_buscar.pack(side=tk.RIGHT, padx=10)

        self.campo_buscar = ttk.Entry(self.marco_acciones, font=('Roboto', 13),width=15)
        self.campo_buscar.pack(side="right", padx=5, pady=10)
        etiqueta_buscar = tk.Label(self.marco_acciones, text="Buscar Producto:", 
                                 font=('Roboto', 13), fg="#666a88", bg=color_fondo_inventario)
        etiqueta_buscar.pack(side="right", padx=5, pady=10)

        # Configuración del Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#000", 
                       borderwidth=1, relief="flat", font=('Roboto', 14))
        style.configure('Treeview.Heading', background="#2E3B4E", foreground="#fff", 
                       borderwidth=1, relief="flat", font=('Roboto', 14, 'bold'))

        self.tree = ttk.Treeview(self.marco_productos, show='headings')
        self.tree['columns'] = ('Id', 'codigo_jerarquico', 'Nombre', 'Cantidad', 'Precio', 'Categoría')
        
        # Configuración de columnas
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Id', width=0, stretch=tk.NO) 
        self.tree.column('codigo_jerarquico', anchor=tk.CENTER, width=100)
        self.tree.column('Nombre', anchor=tk.CENTER, width=200)
        self.tree.column('Cantidad', anchor=tk.CENTER, width=100)
        self.tree.column('Precio', anchor=tk.CENTER, width=100)
        self.tree.column('Categoría', anchor=tk.CENTER, width=150)

        self.tree.heading('#0', text='')
        self.tree.heading('Id', text='')  
        self.tree.heading('codigo_jerarquico', text='Código', command=lambda: self.ordenar_por_columna('codigo_jerarquico', False))
        self.tree.heading('Nombre', text='Nombre', command=lambda: self.ordenar_por_columna('Nombre', False))
        self.tree.heading('Cantidad', text='Cantidad', command=lambda: self.ordenar_por_columna('Cantidad', True))
        self.tree.heading('Precio', text='Precio', command=lambda: self.ordenar_por_columna('Precio', True))
        self.tree.heading('Categoría', text='Categoría', command=lambda: self.ordenar_por_columna('Categoría', False))

        self.tree.pack(expand=True, fill='both')
        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar_treeview)

        self.tree.tag_configure('oddrow', background='#f6f9ff')
        self.tree.tag_configure('evenrow', background='#e8f1ff')

        self.orden_actual = None
        self.columna_orden = None
        self.orden_descendente = False

        # Conectar a la base de datos
        self.conectar_db()
        self.actualizar_lista()

    def conectar_db(self):
        self.conn = sqlite3.connect('database/distriarbelaez.db')
        self.cursor = self.conn.cursor()

    def generar_codigo_jerarquico(self, categoria):
        """Genera un código único por categoría comenzando desde 001."""
        prefijo = categoria[:3].upper()
        self.cursor.execute("SELECT COUNT(*) FROM productos WHERE categoria=?", (categoria,))
        count = self.cursor.fetchone()[0] + 1  
        return f"{prefijo}-{count:03d}"

    def buscar_producto(self):
        termino_busqueda = self.campo_buscar.get().strip()
        if termino_busqueda:
            self.cursor.execute("""
                SELECT id, codigo_jerarquico, nombre, cantidad, precio, categoria 
                FROM productos 
                WHERE nombre LIKE ? OR categoria LIKE ?
            """, ('%' + termino_busqueda + '%', '%' + termino_busqueda + '%'))
            
            productos = self.cursor.fetchall()
            self.actualizar_lista(productos)
        else:
            self.actualizar_lista()

    def ordenar_por_columna(self, columna, es_numerica):
        """Ordena el Treeview por la columna seleccionada."""
        items = [(self.tree.set(item, columna), item) for item in self.tree.get_children('')]
        
        if self.columna_orden == columna:
            self.orden_descendente = not self.orden_descendente
        else:
            self.columna_orden = columna
            self.orden_descendente = False
        
        if es_numerica:
            items.sort(key=lambda x: float(x[0].replace('$', '').replace(',', '')), 
                      reverse=self.orden_descendente)
        else:
            items.sort(key=lambda x: x[0].lower(), reverse=self.orden_descendente)
        
        for index, (valor, item) in enumerate(items):
            self.tree.move(item, '', index)
        
        self.actualizar_heading(columna)

    def actualizar_heading(self, columna):
        for col in self.tree['columns']:
            text = self.tree.heading(col)['text']
            if col == columna:
                if self.orden_descendente:
                    self.tree.heading(col, text=text + ' ▼')
                else:
                    self.tree.heading(col, text=text + ' ▲')
            else:
                if ' ▼' in text or ' ▲' in text:
                    self.tree.heading(col, text=text.replace(' ▼', '').replace(' ▲', ''))

    def actualizar_lista(self, productos=None):
        """Actualiza el Treeview con los productos."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if productos is None:
            self.cursor.execute("SELECT id, codigo_jerarquico, nombre, cantidad, precio, categoria FROM productos")
            productos = self.cursor.fetchall()
        
        count = 0
        for producto in productos:
            precio = f"${producto[4]}"
            tags = ('evenrow',) if count % 2 == 0 else ('oddrow',)
            self.tree.insert('', tk.END, 
                           values=(producto[0], producto[1], producto[2], producto[3], precio, producto[5]),
                           tags=tags)
            count += 1

    def registrar_producto(self):
        nombre = self.campo_nombre.get()
        cantidad = self.campo_cantidad.get()
        precio = self.campo_precio.get()
        categoria = self.combo_categoria.get()
    
        if nombre and precio and cantidad and categoria:
            try:
                codigo_jerarquico = self.generar_codigo_jerarquico(categoria)
                self.cursor.execute("""
                    INSERT INTO productos (nombre, cantidad, precio, categoria, codigo_jerarquico) 
                    VALUES (?, ?, ?, ?, ?)
                """, (nombre, cantidad, precio, categoria, codigo_jerarquico))
                self.conn.commit()
                self.actualizar_lista()
                self.limpiar_campos()
                messagebox.showinfo("Registro exitoso", "Producto registrado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el producto: {e}")
        else:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")

    def al_seleccionar_treeview(self, event):
        selected = self.tree.selection()
        if selected:
            valores = self.tree.item(selected, 'values')
            producto_id = valores[0]  
            nombre = valores[2]      
            cantidad = valores[3]    
            precio = valores[4].replace("$", "") 
            categoria = valores[5]    

            self.campo_nombre.delete(0, 'end')
            self.campo_nombre.insert(0, nombre)
            self.campo_precio.delete(0, 'end')
            self.campo_precio.insert(0, precio)
            self.campo_cantidad.delete(0, 'end')
            self.campo_cantidad.insert(0, cantidad)
            self.combo_categoria.set(categoria)

            self.boton_registro.pack_forget()
            self.boton_eliminar.pack(side=tk.LEFT, padx=5)
            self.boton_modificar.pack(side=tk.LEFT, padx=5)

    def eliminar_producto(self):
        selected = self.tree.selection()
        if selected:
            producto_id = self.tree.item(selected, 'values')[0]
            try:
                self.cursor.execute("DELETE FROM productos WHERE id=?", (producto_id,))
                self.conn.commit()
                self.actualizar_lista()
                self.limpiar_campos()
                messagebox.showinfo("Eliminación exitosa", "Producto eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")
        else:
            messagebox.showwarning("Selecciona un producto", "Por favor, selecciona un producto para eliminar.")

    def modificar_producto(self):
        selected = self.tree.selection()
        if selected:
            producto_id = self.tree.item(selected, 'values')[0]
            nombre = self.campo_nombre.get()
            cantidad = self.campo_cantidad.get()
            precio = self.campo_precio.get()
            categoria = self.combo_categoria.get()

            if nombre and precio and cantidad and categoria:
                try:
                    self.cursor.execute("""
                        UPDATE productos 
                        SET nombre=?, cantidad=?, precio=?, categoria=? 
                        WHERE id=?
                    """, (nombre, cantidad, precio, categoria, producto_id))
                    self.conn.commit()
                    self.actualizar_lista()
                    self.limpiar_campos()
                    messagebox.showinfo("Modificación exitosa", "Producto modificado correctamente.")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo modificar el producto: {e}")
            else:
                messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
        else:
            messagebox.showwarning("Selecciona un producto", "Por favor, selecciona un producto para modificar.")

    def limpiar_campos(self):
        try:
            self.campo_nombre.delete(0, 'end')
            self.campo_cantidad.delete(0, 'end')
            self.campo_precio.delete(0, 'end')
            self.combo_categoria.set('')
            self.boton_registro.pack(side=tk.LEFT, padx=5)
            self.boton_eliminar.pack_forget()
            self.boton_modificar.pack_forget()
        except Exception as e:
            messagebox.showerror("Error", f"Error en la limpieza: {e}")