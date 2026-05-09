import tkinter as tk
import customtkinter as ctk
from tkcalendar import DateEntry
import sqlite3
from tkinter import ttk, messagebox
import pandas as pd
import os
from theme.colores import color_cuerpo_principal, color_fondo_inventario

class reportes_main:
    def __init__(self, cuerpo_principal):
        self.directorio_reportes = os.path.join(os.getcwd(), "Reportes Exel")
        if not os.path.exists(self.directorio_reportes):
            os.makedirs(self.directorio_reportes)

        # Marco Título
        self.marco_titulo = ctk.CTkFrame(cuerpo_principal, fg_color=color_cuerpo_principal, height=40)
        self.marco_titulo.pack(side=tk.TOP, fill='both')

        # Marco Filtros
        self.marco_filtros = ctk.CTkFrame(cuerpo_principal, fg_color=color_cuerpo_principal, height=50)
        self.marco_filtros.pack(side=tk.TOP, fill='both', pady=5)

        # Marco Tabla
        self.marco_tabla = ctk.CTkFrame(cuerpo_principal, fg_color=color_cuerpo_principal, height=300)  # Tabla más corta
        self.marco_tabla.pack(side=tk.TOP, fill='both', pady=10, padx=10)  # Añadir margen

        # Marco Acciones
        self.marco_acciones = ctk.CTkFrame(cuerpo_principal, fg_color=color_cuerpo_principal, height=50)
        self.marco_acciones.pack(side=tk.TOP, fill='both', pady=5)

        # Título
        title = ctk.CTkLabel(
            self.marco_titulo,
            text="REPORTES",
            font=('Roboto', 20),
            fg_color="#485159",
            text_color="#FFFFFF",
            pady=20
        )
        title.pack(expand=True, fill=tk.BOTH)
        
        # Filtros de Fechas
        ctk.CTkLabel(self.marco_filtros, text="Desde:", font=('Roboto', 14), text_color="#666a88").pack(side=tk.LEFT, padx=5)
        self.fecha_inicio = DateEntry(
            self.marco_filtros, 
            date_pattern='yyyy-mm-dd', 
            font=('Roboto', 12), 
            locale='es_ES'
        )
        self.fecha_inicio.pack(side=tk.LEFT, padx=5)

        ctk.CTkLabel(self.marco_filtros, text="Hasta:", font=('Roboto', 14), text_color="#666a88").pack(side=tk.LEFT, padx=5)
        self.fecha_fin = DateEntry(
            self.marco_filtros, 
            date_pattern='yyyy-mm-dd', 
            font=('Roboto', 12), 
            locale='es_ES'
        )
        self.fecha_fin.pack(side=tk.LEFT, padx=5)

        # Crear un marco adicional para centrar los botones
        self.marco_botones = ctk.CTkFrame(self.marco_acciones, fg_color=color_cuerpo_principal)
        self.marco_botones.pack(side=tk.TOP, fill=tk.BOTH, pady=10)

        # Botones para generar reportes
        btn_mas_vendidos = ctk.CTkButton(
            self.marco_botones,
            text="Productos Más Vendidos",
            command=self.mostrar_productos_mas_vendidos,
            width=200,  
            height=50, 
            font=('Roboto', 16)  
        )
        btn_mas_vendidos.grid(row=0, column=0, padx=20, pady=10)

        btn_ventas = ctk.CTkButton(
            self.marco_botones,
            text="Reporte de Ventas",
            command=self.mostrar_reporte_ventas,
            width=200,  
            height=50, 
            font=('Roboto', 16) 
        )
        btn_ventas.grid(row=0, column=1, padx=20, pady=10)

        # Centrar los botones con grid
        self.marco_botones.grid_columnconfigure(0, weight=1)
        self.marco_botones.grid_columnconfigure(1, weight=1)

        # Estilo de la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#000", borderwidth=1, relief="flat", font=('Roboto', 14))
        style.configure('Treeview.Heading', background="#2E3B4E", foreground="#fff", borderwidth=1, relief="flat", font=('Roboto', 14, 'bold'))

        # Crear tabla
        self.tree = ttk.Treeview(self.marco_tabla, show='headings')
        self.tree['columns'] = ('Producto', 'Cantidad Vendida', 'Ingresos Totales')
        
        # Ajustar las columnas para hacerlas más estrechas
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Producto', anchor=tk.CENTER, width=200) 
        self.tree.column('Cantidad Vendida', anchor=tk.CENTER, width=120)  
        self.tree.column('Ingresos Totales', anchor=tk.CENTER, width=150) 
        
        # Configuración de encabezados
        self.tree.heading('#0', text='')
        self.tree.heading('Producto', text='Producto')
        self.tree.heading('Cantidad Vendida', text='Cantidad Vendida')
        self.tree.heading('Ingresos Totales', text='Ingresos Totales')

        self.tree.pack(expand=True, fill='both')

        self.tree.tag_configure('oddrow', background='#f6f9ff') 
        self.tree.tag_configure('evenrow', background='#e8f1ff')


    def configurar_tabla(self, columnas):
        # Configurar columnas
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=200)

    def mostrar_productos_mas_vendidos(self):
        # Obtener fechas seleccionadas
        fecha_inicio = self.fecha_inicio.get()
        fecha_fin = self.fecha_fin.get()

        if not fecha_inicio or not fecha_fin:
            messagebox.showerror("Error", "Por favor seleccione un rango de fechas.")
            return

        try:
            conn = sqlite3.connect('database/distriarbelaez.db')
            cursor = conn.cursor()

            cursor.execute(""" 
                SELECT nombre_articulo AS Producto, SUM(cantidad) AS Cantidad_Vendida, 
                       SUM(subtotal) AS Ingresos_Totales
                FROM ventas
                WHERE fecha BETWEEN ? AND ?
                GROUP BY nombre_articulo
                ORDER BY Cantidad_Vendida DESC
            """, (fecha_inicio, fecha_fin))
            data = cursor.fetchall()

            # Mostrar datos en la tabla
            self.configurar_tabla(["Producto", "Cantidad Vendida", "Ingresos Totales"])
            for idx, row in enumerate(data):
                if idx % 2 == 0:
                    self.tree.insert("", tk.END, values=row, tags=('evenrow',))
                else:
                    self.tree.insert("", tk.END, values=row, tags=('oddrow',))

            # Calcular los totales
            total_cantidad = sum([row[1] for row in data])
            total_ingresos = sum([row[2] for row in data])

            # Añadir fila de totales
            self.tree.insert("", tk.END, values=("TOTAL", total_cantidad, total_ingresos), tags=('evenrow',))

            # Preguntar si desea guardar el reporte
            if messagebox.askyesno("Confirmación", "¿Desea generar el reporte en un archivo Excel?"):
                df = pd.DataFrame(data, columns=["Producto", "Cantidad Vendida", "Ingresos Totales"])

                df.loc[len(df)] = ["TOTAL", total_cantidad, total_ingresos]
                nombre_archivo = f"Productos_Mas_Vendidos_{fecha_inicio}_a_{fecha_fin}.xlsx"
                archivo_guardar = os.path.join(self.directorio_reportes, nombre_archivo)
                df.to_excel(archivo_guardar, index=False)
                conn.close()

                messagebox.showinfo("Reporte Generado", f"El reporte ha sido guardado como '{archivo_guardar}'.")
            else:
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el reporte: {e}")

    def mostrar_reporte_ventas(self):
        # Obtener fechas seleccionadas
        fecha_inicio = self.fecha_inicio.get()
        fecha_fin = self.fecha_fin.get()

        if not fecha_inicio or not fecha_fin:
            messagebox.showerror("Error", "Por favor seleccione un rango de fechas.")
            return

        try:
            conn = sqlite3.connect('database/distriarbelaez.db')
            cursor = conn.cursor()

            cursor.execute("""
                SELECT factura, nombre_cliente, fecha, SUM(subtotal) AS total
                FROM ventas
                WHERE fecha BETWEEN ? AND ?
                GROUP BY factura
                ORDER BY fecha
            """, (fecha_inicio, fecha_fin))
            data = cursor.fetchall()

            self.configurar_tabla(["Factura", "Cliente", "Fecha", "Total"])
            for idx, row in enumerate(data):
                if idx % 2 == 0:
                    self.tree.insert("", tk.END, values=row, tags=('evenrow',))
                else:
                    self.tree.insert("", tk.END, values=row, tags=('oddrow',))

            # Calcular el total de ventas
            total_ventas = sum([row[3] for row in data])

            self.tree.insert("", tk.END, values=("TOTAL", "", "", total_ventas), tags=('evenrow',))

            # Preguntar si desea guardar el reporte
            if messagebox.askyesno("Confirmación", "¿Desea generar el reporte en un archivo Excel?"):
                df = pd.DataFrame(data, columns=["Factura", "Cliente", "Fecha", "Total"])

                df.loc[len(df)] = ["TOTAL", "", "", total_ventas]
                nombre_archivo = f"Reporte_Ventas_{fecha_inicio}_a_{fecha_fin}.xlsx"
                archivo_guardar = os.path.join(self.directorio_reportes, nombre_archivo)
                df.to_excel(archivo_guardar, index=False)
                conn.close()

                messagebox.showinfo("Reporte Generado", f"El reporte ha sido guardado como '{archivo_guardar}'.")
            else:
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el reporte de ventas: {e}")
