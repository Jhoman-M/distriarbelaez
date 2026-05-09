import tkinter as tk
import customtkinter as ctk
import sqlite3
from tkinter import Toplevel, Text, Scrollbar
from datetime import datetime
import win32print
import win32ui
import win32con
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from tkinter import ttk, messagebox
from theme.colores import color_fondo_inventario, color_fondo_buscar_inventario
import sys
from fpdf import FPDF
import os
from utils.nombre_impresora import obtener_nombre_impresora


class Facturacion_main():
    def __init__(self, cuerpo_principal):
        # Marco del título
        self.marco_titulo = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario, height=40)
        self.marco_titulo.pack(side=tk.TOP, fill='both')

        title = ctk.CTkLabel(self.marco_titulo, text="FACTURACIÓN", font=('Roboto', 20), fg_color="#485159", text_color=color_fondo_buscar_inventario, pady=20)
        title.pack(expand=True, fill=tk.BOTH)

        # Marco del registro
        self.marco_registro = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario, height=130)
        self.marco_registro.place(x=0, y=90, relwidth=1)

        etiqueta_producto = tk.Label(self.marco_registro, text="Nombre producto: ", font=('Roboto', 14), fg="#666a88", bg=color_fondo_inventario)
        etiqueta_producto.pack(side='left')

        self.campo_producto = ttk.Combobox(self.marco_registro, font=('Roboto', 14), width=20)
        self.campo_producto.pack(side='left')

        self.cargar_productos()
        self.campo_producto.bind('<KeyRelease>', self.autocompletar_producto)

        etiqueta_cantidad = tk.Label(self.marco_registro, text="Cantidad: ", font=('Roboto', 14), fg="#666a88", bg=color_fondo_inventario)
        etiqueta_cantidad.pack(side='left')
        self.campo_cantidad = ttk.Entry(self.marco_registro, font=('Roboto', 14), width=10)
        self.campo_cantidad.pack(side='left')

        # Botones
        self.marco_Botones = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario, height=130)
        self.marco_Botones.place(x=0, y=140, relwidth=1)

        self.boton_agregar = ctk.CTkButton(self.marco_Botones, text="Agregar Producto", font=('Roboto', 14), fg_color='#1c84cd', text_color="#fff",
        corner_radius=8,hover_color="#2d73a4",border_width=2,border_color="#2d73a4", command=self.registrar)
        self.boton_agregar.pack(side=tk.LEFT, padx=15)

        self.boton_pagar = ctk.CTkButton(self.marco_Botones, text="Pagar", font=('Roboto', 14), fg_color='#3ed152', text_color="#fff",
        corner_radius=8,hover_color="#33a943",border_width=2,border_color="#33a943",command=self.ventana_pago)
        self.boton_pagar.pack(side=tk.LEFT, padx=15)

        self.boton_factura = ctk.CTkButton(self.marco_Botones, text="Ver facturas", font=('Roboto', 14), fg_color='#aa0404', text_color="#fff",
        corner_radius=8,hover_color="#951d1d",border_width=2,border_color="#951d1d",command=self.abrir_ventana_factura)
        self.boton_factura.pack(side=tk.LEFT, padx=15)
        
        self.boton_eliminar = ctk.CTkButton(self.marco_Botones, text="Eliminar", font=('Roboto', 14), fg_color='#bd0507', text_color="#fff",
        corner_radius=8,hover_color="#991517",border_width=2,border_color="#991517",command=self.eliminar_producto)
        self.boton_eliminar.pack_forget()

        # Total a pagar
        self.marco_label = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario, height=130)
        self.marco_label.place(x=0, y=190, relwidth=1)

        self.label_suma_total = tk.Label(self.marco_label, text="Total a pagar: COP 0", font=('Roboto', 16), fg="#666a88", bg=color_fondo_inventario)
        self.label_suma_total.pack(anchor='center')

        # Marco de productos
        self.marco_productos = ctk.CTkFrame(cuerpo_principal, fg_color=color_fondo_inventario, height=130)
        self.marco_productos.place(relx=0.05, y=240, relwidth=0.9)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#000", borderwidth=1, relief="flat", font=('Roboto', 14))
        style.configure('Treeview.Heading', background="#2E3B4E", foreground="#fff", borderwidth=1, relief="flat", font=('Roboto', 14, 'bold'))

        self.tree = ttk.Treeview(self.marco_productos, show='headings')
        self.tree['columns'] = ('Producto', 'Cantidad', 'Precio', 'Subtotal')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Producto', anchor=tk.CENTER, width=200)
        self.tree.column('Cantidad', anchor=tk.CENTER, width=100)
        self.tree.column('Precio', anchor=tk.CENTER, width=100)
        self.tree.column('Subtotal', anchor=tk.CENTER, width=100)

        self.tree.heading('#0', text='')
        self.tree.heading('Producto', text='Producto')
        self.tree.heading('Cantidad', text='Cantidad')
        self.tree.heading('Precio', text='Precio')
        self.tree.heading('Subtotal', text='Subtotal')

        self.tree.pack(expand=True, fill='both')
        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar_treeview)

        self.tree.tag_configure('oddrow', background='#f6f9ff') 
        self.tree.tag_configure('evenrow', background='#e8f1ff')

    db_name = "database/distriarbelaez.db"

    def cargar_productos(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT nombre FROM productos")
        productos = c.fetchall()
        self.productos = [producto[0] for producto in productos] 
        self.campo_producto["values"] = self.productos 
        conn.close()

    def autocompletar_producto(self, event):
        texto = self.campo_producto.get().lower()
        if texto == '':
            self.campo_producto["values"] = self.productos
        else:
            productos_filtrados = [prod for prod in self.productos if texto in prod.lower()]
            self.campo_producto["values"] = productos_filtrados
            self.campo_producto.event_generate('<Down>') 

    def registrar(self):
        producto = self.campo_producto.get()
        cantidad = self.campo_cantidad.get()
    
        if not producto or not cantidad:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un producto y una cantidad.")
            return
    
        try:
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número.")
            return
    
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT precio FROM productos WHERE nombre = ?", (producto,))
        precio = c.fetchone()
    
        if precio:
            precio = precio[0]
            subtotal = cantidad * precio

            precio_formateado = f"${precio:.0f}"
            subtotal_formateado = f"${subtotal:.0f}"

            index = len(self.tree.get_children())
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
    
            self.tree.insert("", "end", values=(producto, cantidad, precio_formateado, subtotal_formateado), tags=(tag,))
            self.actualizar_total()

            self.campo_producto.set('')
            self.campo_cantidad.delete(0, 'end')
        else:
            messagebox.showerror("Error", "El producto no existe en la base de datos.")
    
        conn.close()
    def actualizar_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = self.tree.item(child, "values")[3]
            subtotal = float(subtotal.replace('$', '').replace(',', ''))
            total += subtotal
        self.label_suma_total.config(text=f"Total a pagar: ${total:.0f}")

    def verificar_stock(self,nombre_producto,cantidad):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT cantidad FROM productos WHERE nombre =?",(nombre_producto,))    
            stock = c.fetchone()
            if stock and stock[0] >= cantidad:
                return True
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al verificar el stock: {e}")
            return False
        finally:
            conn.close()



    def al_seleccionar_treeview(self, event):
         selected = self.tree.selection()
         if selected:
             producto = self.tree.item(selected)['values'][0]
             cantidad = self.tree.item(selected)['values'][1]
             precio = self.tree.item(selected)['values'][2]
             self.campo_producto.set(producto)
             self.campo_cantidad.delete(0, 'end')
             self.campo_cantidad.insert(0, cantidad)
             self.boton_eliminar.pack(side=tk.LEFT, padx=5)

    def eliminar_producto(self):
         selected = self.tree.selection()
         if selected:
             for item in selected:
                 self.tree.delete(item)
             self.actualizar_total()


    def ventana_pago(self):
        # Crear la ventana de pago
        ventana_pago = ctk.CTkToplevel()
        ventana_pago.title("Pago")
        ventana_pago.geometry("400x400+500+150")        
        ventana_pago.iconbitmap("icono.ico")
        ventana_pago.lift()
        ventana_pago.attributes('-topmost', True)
        ventana_pago.resizable(False,False)

        etiqueta_nombre_cliente = ctk.CTkLabel(ventana_pago, text="Nombre del cliente:", font=('Roboto', 14))
        etiqueta_nombre_cliente.pack(pady=10)

        self.campo_nombre_cliente = ttk.Combobox(ventana_pago, font=('Roboto', 14), width=15,style='Custom.TCombobox')
        self.campo_nombre_cliente.pack(pady=10)
        style = ttk.Style()
        style.configure('Custom.TCombobox',
                fieldbackground='#343638', 
                background='#ffffff',      
                foreground='#ffffff', 
                selectbackground='#343638',
                
                )

        self.cargar_clientes()

        self.campo_nombre_cliente.bind('<KeyRelease>', self.autocompletar_cliente)

        total = self.label_suma_total.cget("text").split(": ")[1]
        etiqueta_total = ctk.CTkLabel(ventana_pago, text=f"Total a pagar: {total}", font=('Roboto', 14))
        etiqueta_total.pack(pady=30)

        etiqueta_pago_cliente = ctk.CTkLabel(ventana_pago, text="Cantidad con la que paga:", font=('Roboto', 14))
        etiqueta_pago_cliente.pack(pady=10)

        self.campo_pago_cliente = ctk.CTkEntry(ventana_pago, font=('Roboto', 14), width=200)
        self.campo_pago_cliente.pack()

        boton_calcular_vuelto = ctk.CTkButton(ventana_pago, text="Calcular vuelto", font=('Roboto', 14), fg_color='#0a5890', text_color="#fff",
        corner_radius=8,hover_color="#1e557e",border_width=2,border_color="#1e557e", command=self.calcular_vuelto)
        boton_calcular_vuelto.pack(pady=10)

        boton_pagar = ctk.CTkButton(ventana_pago, text="Confirmar venta", font=('Roboto', 14), fg_color='#3ed152', text_color="#fff",
        corner_radius=8,hover_color="#33a943",border_width=2,border_color="#33a943",command=lambda: self.pagar(ventana_pago))
        boton_pagar.pack()

        self.etiqueta_vuelto = ctk.CTkLabel(ventana_pago, text="", font=('Roboto', 14))
        self.etiqueta_vuelto.place(x=140, y=150)

        boton_previsualizar = ctk.CTkButton(ventana_pago, text="Previsualizar Factura", font=('Roboto', 14), fg_color='#f5a623',text_color="#fff",
        corner_radius=8,hover_color="#c18116",border_width=2,border_color="#c18116", command=self.previsualizar_factura)
        boton_previsualizar.pack(pady=10)


    def cargar_clientes(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT nombre_cliente FROM clientes")
        clientes = c.fetchall()
        self.clientes = [cliente[0] for cliente in clientes]
        self.campo_nombre_cliente["values"] = self.clientes
        conn.close()

    def autocompletar_cliente(self, event):
        texto = self.campo_nombre_cliente.get().lower()
        if texto == '':
            self.campo_nombre_cliente["values"] = self.clientes
        else:
            clientes_filtrados = [cliente for cliente in self.clientes if texto in cliente.lower()]
            self.campo_nombre_cliente["values"] = clientes_filtrados
            self.campo_nombre_cliente.event_generate('<Down>')

    def calcular_vuelto(self):
        try:
            cantidad_pagada = float(self.campo_pago_cliente.get())

            total_texto = self.label_suma_total.cget("text")
            total = float(total_texto.split(": $")[1].replace(',', ''))

            cambio = cantidad_pagada - total

            if cambio < 0:
                messagebox.showerror("Error", "La cantidad es insuficiente.")
                return

            self.etiqueta_vuelto.configure(text=f"Vuelto: COP {cambio:.0f}")
        except ValueError:
                messagebox.showerror("Error", "Ingrese una cantidad válida.")



    def pagar(self, ventana_pago):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            self.numero_factura_actual = self.obtener_numero_factura_actual()
    
            cantidad_pagada = self.campo_pago_cliente.get()
            
            if cantidad_pagada and not cantidad_pagada.isdigit():
                messagebox.showerror("Error", "Ingrese una cantidad válida para el pago.")
                return
    
            # Si no se ingresa un cliente, se usa "CONSUMIDOR FINAL"
            nombre_cliente = self.campo_nombre_cliente.get().strip()
            if not nombre_cliente:
                nombre_cliente = "CONSUMIDOR FINAL"
    
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            total = 0
            productos = []
    
            for child in self.tree.get_children():
                item = self.tree.item(child, "values")
                nombre_producto = item[0]
                cantidad_vendida = int(item[1])
                precio = float(item[2].replace('$', '').replace(',', ''))
                subtotal = float(item[3].replace('$', '').replace(',', ''))
    
                # Verificar que haya stock suficiente
                if not self.verificar_stock(nombre_producto, cantidad_vendida):
                    messagebox.showerror("Error", f"Stock insuficiente para el producto {nombre_producto}.")
                    return
    
                c.execute("""
                    INSERT INTO ventas (factura, fecha, nombre_cliente, nombre_articulo, precio, cantidad, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (self.numero_factura_actual, fecha_actual, nombre_cliente, nombre_producto, precio, cantidad_vendida, subtotal))
    
                # Actualizar el stock de los productos
                c.execute("""
                    UPDATE productos
                    SET cantidad = cantidad - ?
                    WHERE nombre = ?
                """, (cantidad_vendida, nombre_producto))
    
                total += subtotal
                productos.append([cantidad_vendida, nombre_producto, f"${precio:.0f}", f"${subtotal:.0f}"])
    
            conn.commit()
    
            # Imprimir la factura
            self.imprimir_factura()
    
            for child in self.tree.get_children():
                self.tree.delete(child)
    
            self.label_suma_total.config(text="Total a pagar: COP 0")
    
            ventana_pago.destroy()
    
        except sqlite3.Error as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error al registrar la venta: {e}")
    
        finally:
            conn.close()
    


    def obtener_numero_factura_actual(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT MAX(factura) FROM ventas")
            max_factura = c.fetchone()[0]
            if max_factura:
                return max_factura + 1
            else:
                return 1
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el número de factura: {e}")
            return 1
        finally:
            conn.close()


    def imprimir_factura(self):
#            hprinter = win32print.OpenPrinter("POS-80C")
#            hdc = win32ui.CreateDC()
#            hdc.CreatePrinterDC("POS-80C")
#            hdc.StartDoc("Factura")
#            hdc.StartPage()
        try:
            conexion = sqlite3.connect("database/distriarbelaez.db")
            cursor = conexion.cursor()

            cursor.execute("SELECT valor FROM ajustes WHERE clave = 'nombre_impresora'")
            resultado = cursor.fetchone()
            nombre_impresora = resultado[0] if resultado else None

            if not nombre_impresora:
                print("Error: No se encontró un nombre de impresora configurado.")
                return
            hprinter = win32print.OpenPrinter(nombre_impresora)
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(nombre_impresora)
    
            hdc.StartDoc("Factura")
            hdc.StartPage()    

            fuente_distri = win32ui.CreateFont({
                "name": "Arial",
                "height": 33,  
                "weight": 700,
            })
            fuente_normal = win32ui.CreateFont({
                "name": "Arial",
                "height": 26,  
                "weight": 400,
            })
            fuente_negrita = win32ui.CreateFont({
                "name": "Arial",
                "height": 26,
                "weight": 700,
            })
            hdc.SelectObject(fuente_distri)
    
            y = 0 
            
            ancho_pagina = 600
            titulos = [
                "DISTRIARBELAEZ"
            ]
            for titu in titulos:
                ancho_texto = hdc.GetTextExtent(titu)[0] 
                x = (ancho_pagina - ancho_texto) // 2
                hdc.TextOut(x, y, titu) 
                y += 40 

            hdc.SelectObject(fuente_negrita)
            

            textos = []
            claves = ["nombre","nit", "direccion", "telefono"]
            for clave in claves:
                cursor.execute("SELECT valor FROM configuracion WHERE clave = ?", (clave,))
                resultado = cursor.fetchone()
                textos.append(resultado[0] if resultado else "No disponible")


            #textos = [
            #    "ANDRES CAMILO OROZCO ARBELAEZ",
            #    "NIT: 1.038.412.541-0",
            #    "CARRERA 33 #25A45",
            #    "Telefono: 3044973141"
            #]

            for texto in textos:
                ancho_texto = hdc.GetTextExtent(texto)[0] 
                x = (ancho_pagina - ancho_texto) // 2
                hdc.TextOut(x, y, texto) 
                y += 40 


            hdc.TextOut(80, y, f"Fecha exp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            y += 30

            hdc.SelectObject(fuente_negrita)

            hdc.TextOut(80, y, f"Cliente: {self.campo_nombre_cliente.get()}")
            y += 50

            hdc.SelectObject(fuente_normal)
            cursor.execute("""
                SELECT direccion FROM clientes WHERE nombre_cliente = ?
            """, (self.campo_nombre_cliente.get(),))
            direccion_cliente = cursor.fetchone()
            direccion_texto = f"Dirección: {direccion_cliente[0]}" if direccion_cliente else "Dirección:"
            hdc.TextOut(80, y, direccion_texto)
            y += 50

            hdc.TextOut(60, y, "CNT")
            hdc.TextOut(130, y, "Producto")
            hdc.TextOut(360, y, "Precio")
            hdc.TextOut(460, y, "Subtotal")
            y += 40

            hdc.SelectObject(fuente_normal)


            for child in self.tree.get_children():
                item = self.tree.item(child, "values")
                hdc.TextOut(60, y, item[1]) 
                hdc.TextOut(130, y, item[0])  
                hdc.TextOut(360, y, item[2]) 
                hdc.TextOut(460, y, item[3])  
                y += 30


            hdc.SelectObject(fuente_normal)
            hdc.SelectObject(fuente_negrita)

            hdc.TextOut(60, y, f"Total a pagar: {self.label_suma_total.cget('text').split(': ')[1]}")
            y += 40 
            
            hdc.SelectObject(fuente_normal)

            #resolucion antes del test
            #textosReso = [
            #    "Resolucion No. 123456",
            #    "Del 2024-02-20 hasta 2025-02-20",
            #]

            fecha_emision = datetime.now()
            fecha_final = fecha_emision.replace(year=fecha_emision.year + 1)
            textosReso = [
                "Resolucion No. 123456",
                f"Del {fecha_emision.strftime('%Y-%m-%d')} hasta {fecha_final.strftime('%Y-%m-%d')}",
            ]


            for textores in textosReso:
                ancho_texto = hdc.GetTextExtent(textores)[0] 
                x = (ancho_pagina - ancho_texto) // 2
                hdc.TextOut(x, y, textores) 
                y += 40

            hdc.SelectObject(fuente_negrita)

            hdc.TextOut(160, y, "NO RESPONSABLE DE IVA")
            hdc.EndPage()
            hdc.EndDoc()

        except Exception as e:
            print(f"Error al imprimir la factura: {e}")
        finally:
            if 'hprinter' in locals():
                win32print.ClosePrinter(hprinter)

    def previsualizar_factura(self):
        # Crear ventana de previsualización
        ventana_previsualizacion = ctk.CTkToplevel()
        ventana_previsualizacion.title("Previsualización de la Factura")
        ventana_previsualizacion.geometry("300x400")
        ventana_previsualizacion.attributes('-topmost', True)
        ventana_previsualizacion.resizable(False, False)

        frame = ctk.CTkFrame(ventana_previsualizacion)
        frame.pack(expand=True, fill='both')

        text_area = Text(frame, wrap="word", font=("Arial", 10))
        text_area.pack(side="left", expand=True, fill='both')

        scroll = Scrollbar(frame, command=text_area.yview)
        scroll.pack(side="right", fill="y")
        text_area.config(yscrollcommand=scroll.set)

        try:
            conexion = sqlite3.connect("database/distriarbelaez.db")
            cursor = conexion.cursor()

            claves = ["nombre", "nit", "direccion", "telefono"]
            datos = {}
            for clave in claves:
                cursor.execute("SELECT valor FROM ajustes WHERE clave = ?", (clave,))
                resultado = cursor.fetchone()
                datos[clave] = resultado[0] if resultado else "No disponible"

            # Formatear la factura
            factura = ""
            factura += "{:^40}\n".format("DISTRIARBELAEZ")
            factura += "{:^40}\n".format(datos["nombre"])
            factura += "{:^40}\n".format(datos["nit"])
            factura += "{:^40}\n".format(datos["direccion"])
            factura += "{:^40}\n".format(datos["telefono"])
            factura += f"Fecha exp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            factura += f"Cliente: {self.campo_nombre_cliente.get()}\n\n"

            # Encabezado de productos
            factura += "{:<10}{:<15}{:<15}{:<10}\n".format("Producto", "Cantidad", "Precio", "Subtotal")
            factura += "----------------------------------------------------------------------\n"

            # Detalles de productos
            for child in self.tree.get_children():
                item = self.tree.item(child, "values")
                factura += "{:<20}{:<10}{:<20}{:<10}\n".format(item[0], item[1], item[2], item[3])

            factura += "----------------------------------------------------------------------\n"
            factura += "{:>30}\n".format(f"Total a pagar: {self.label_suma_total.cget('text').split(': ')[1]}")
            factura += "{:>30}\n".format("NO RESPONSABLE DE IVA\n")

            text_area.insert("1.0", factura)

        except Exception as e:
            factura = "Error al cargar la factura:\n" + str(e)
            text_area.insert("1.0", factura)

        finally:
            if 'conexion' in locals():
                conexion.close()

        text_area.config(state="disabled")





    def cargar_facturas(self, tree):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute("""
                SELECT 
                    factura,
                    fecha,
                    nombre_cliente,
                    SUM(subtotal) AS total_venta
                FROM ventas
                GROUP BY factura, fecha, nombre_cliente
                ORDER BY fecha DESC
            """)
            facturas = c.fetchall()

            for item in tree.get_children():
                tree.delete(item)

            for i, factura in enumerate(facturas):
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                tree.insert("", "end", values=factura, tags=tags)

            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar las facturas: {e}")

    def abrir_ventana_factura(self):
        ventana_factura = ctk.CTkToplevel()
        ventana_factura.title("Facturas Registradas")
        ventana_factura.geometry("900x600")
        ventana_factura.iconbitmap("icono.ico")
        ventana_factura.lift()
        ventana_factura.attributes('-topmost', True)
        ventana_factura.resizable(True, True)
    
        # Marco de búsqueda
        frame_busqueda = tk.Frame(ventana_factura, bg="#74828a")
        frame_busqueda.pack(fill=tk.X, side=tk.TOP, pady=10)
    
        texto_buscar = ctk.CTkLabel(frame_busqueda, text="Buscar por fecha:", text_color="#ffffff")
        texto_buscar.grid(row=0, column=0, padx=10, pady=10)
    
        entrada_buscar = ctk.CTkEntry(frame_busqueda, width=200)
        entrada_buscar.grid(row=0, column=1, padx=10, pady=10)
    
        boton_buscar = ctk.CTkButton(
            frame_busqueda,
            text="Buscar",
            width=150,
            command=lambda: self.buscar_factura(tree_facturas, entrada_buscar.get())
        )
        boton_buscar.grid(row=0, column=2, padx=10, pady=10)
    
        boton_ver_pdf = ctk.CTkButton(
            frame_busqueda,
            text="Ver en PDF",
            width=150,
            command=lambda: self.ver_factura_pdf(tree_facturas)
        )
        boton_ver_pdf.grid(row=0, column=3, padx=10, pady=10)
    
        # Botón para imprimir la factura seleccionada
        boton_imprimir = ctk.CTkButton(
            frame_busqueda,
            text="Imprimir",
            width=150,
            command=lambda: self.imprimir_factura_seleccionada(tree_facturas)
        )
        boton_imprimir.grid(row=0, column=4, padx=10, pady=10)
    
        # Marco del Treeview
        treFrame = tk.Frame(ventana_factura)
        treFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
        tree_scroll_Y = ttk.Scrollbar(treFrame, orient='vertical')
        tree_scroll_Y.pack(side=tk.RIGHT, fill=tk.Y)
    
        tree_scroll_X = ttk.Scrollbar(treFrame, orient='horizontal')
        tree_scroll_X.pack(side=tk.BOTTOM, fill=tk.X)
    
        tree_facturas = ttk.Treeview(
            treFrame,
            show='headings',
            yscrollcommand=tree_scroll_Y.set,
            xscrollcommand=tree_scroll_X.set
        )
        tree_facturas['columns'] = ('Factura', 'Fecha', 'Cliente', 'Total')
    
        tree_facturas.column('#0', width=0, stretch=tk.NO)
        tree_facturas.column('Factura', anchor=tk.CENTER, width=100, stretch=tk.YES)
        tree_facturas.column('Fecha', anchor=tk.CENTER, width=150, stretch=tk.YES)
        tree_facturas.column('Cliente', anchor=tk.CENTER, width=250, stretch=tk.YES)
        tree_facturas.column('Total', anchor=tk.CENTER, width=150, stretch=tk.YES)
    
        tree_facturas.heading('#0', text='')
        tree_facturas.heading('Factura', text='Factura')
        tree_facturas.heading('Fecha', text='Fecha')
        tree_facturas.heading('Cliente', text='Cliente')
        tree_facturas.heading('Total', text='Total (COP)')
    
        tree_facturas.pack(expand=True, fill='both')
    
        tree_facturas.tag_configure('oddrow', background='#f2f2f2')
        tree_facturas.tag_configure('evenrow', background='#c6c6c6')
    
        tree_facturas.configure(yscrollcommand=tree_scroll_Y.set)
        tree_scroll_Y.config(command=tree_facturas.yview)
    
        tree_facturas.configure(xscrollcommand=tree_scroll_X.set)
        tree_scroll_X.config(command=tree_facturas.xview)
    
        self.cargar_facturas(tree_facturas)


    def ver_factura_pdf(self, tree):
        try:
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror("Error", "Seleccione una factura para ver.")
                return
    
            # Obtener el número de factura
            factura_id = tree.item(selected_item, "values")[0]
    
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("""
                SELECT nombre_articulo, precio, cantidad, subtotal
                FROM ventas
                WHERE factura = ?
            """, (factura_id,))
            productos = c.fetchall()
    
            c.execute("""
                SELECT fecha, nombre_cliente, SUM(subtotal)
                FROM ventas
                WHERE factura = ?
                GROUP BY factura, fecha, nombre_cliente
            """, (factura_id,))
            factura_info = c.fetchone()
            conn.close()
    
            if not factura_info:
                messagebox.showerror("Error", "No se encontró información para la factura seleccionada.")
                return
    
            # Definir carpeta predeterminada para guardar los PDFs
            carpeta_facturas = "Facturas_PDF"
            if not os.path.exists(carpeta_facturas):
                os.makedirs(carpeta_facturas)
    
            archivo_pdf = os.path.join(carpeta_facturas, f"Factura_{factura_id}.pdf")
    
            # Crear el objeto PDF
            pdf = FPDF()
            pdf.add_page()
    
            # Establecer la fuente
            pdf.set_font("Arial", 'B', 12)
    
            # Título de la factura
            pdf.cell(200, 10, 'DISTRIARBELAEZ', ln=True, align='C')
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(200, 10, 'ANDRES CAMILO OROZCO ARBELAEZ', ln=True, align='C')
            pdf.cell(200, 10, 'NIT: 1.038.412.541-0', ln=True, align='C')
            pdf.cell(200, 10, 'CARRERA 33 #25A45', ln=True, align='C')
            pdf.cell(200, 10, 'Telefono: 3044973141', ln=True, align='C')
    
            # Espacio para la fecha y cliente
            pdf.ln(10)
            pdf.set_font("Arial", '', 10)
            pdf.cell(200, 10, f"Fecha: {factura_info[0]}", ln=True)
            pdf.cell(200, 10, f"Cliente: {factura_info[1]}", ln=True)
            pdf.ln(10)
    
            # Detalles de los productos
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(40, 10, "Producto", align='C')
            pdf.cell(30, 10, "Cantidad", align='C')
            pdf.cell(40, 10, "Precio", align='C')
            pdf.cell(40, 10, "Subtotal", align='C')
            pdf.ln()
    
            # Mostrar los productos
            pdf.set_font("Arial", '', 10)
            for producto in productos:
                pdf.cell(40, 10, producto[0], align='C')
                pdf.cell(30, 10, str(producto[2]), align='C')
                pdf.cell(40, 10, f"{producto[1]:,.0f}", align='C')
                pdf.cell(40, 10, f"{producto[3]:,.0f}", align='C')
                pdf.ln()
    
            pdf.ln(5)
            pdf.cell(200, 10, f"Total a pagar: COP {factura_info[2]:,.0f}", ln=True, align='C')
            pdf.ln(5)
            pdf.cell(200, 10, "NO RESPONSABLE DE IVA", ln=True, align='C')
    
    
            fecha_factura_obj = datetime.strptime(factura_info[0], "%Y-%m-%d")
            fecha_inicio = fecha_factura_obj.strftime("%Y-%m-%d")
            fecha_fin = (fecha_factura_obj.replace(year=fecha_factura_obj.year + 1)).strftime("%Y-%m-%d")
            resolucion_texto = f"Resolución No. 123456\nDel {fecha_inicio} hasta {fecha_fin}"
    
            pdf.ln(10)
            pdf.multi_cell(0, 10, resolucion_texto, align='C')
    
            # Guardar el archivo PDF
            pdf.output(archivo_pdf)
    
            if os.name == 'nt':  
                os.startfile(archivo_pdf)
    
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el PDF: {e}")

    def imprimir_factura_seleccionada(self, tree):
        try:
            # Verificar selección
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror("Error", "Seleccione una factura para imprimir.")
                return

            factura_id = tree.item(selected_item, "values")[0]

            # Conexión a la base de datos
            conexion = sqlite3.connect("database/distriarbelaez.db")
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT nombre_articulo, precio, cantidad, subtotal
                FROM ventas
                WHERE factura = ?
            """, (factura_id,))
            productos = cursor.fetchall()

            cursor.execute("""
                SELECT fecha, nombre_cliente, SUM(subtotal)
                FROM ventas
                WHERE factura = ?
                GROUP BY factura, fecha, nombre_cliente
            """, (factura_id,))
            factura_info = cursor.fetchone()

            conexion.close()

            if not factura_info:
                messagebox.showerror("Error", "No se encontró información para la factura seleccionada.")
                return

            # Llamar a la función de impresión
            self.imprimir_factura_factura(factura_info, productos)

        except sqlite3.Error as db_error:
            messagebox.showerror("Error de Base de Datos", f"{db_error}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al imprimir la factura: {e}")

    def imprimir_factura_factura(self, factura_info, productos):

        try:
            # Obtener el nombre de la impresora desde la base de datos
            conexion = sqlite3.connect("database/distriarbelaez.db")
            cursor = conexion.cursor()

            cursor.execute("SELECT valor FROM ajustes WHERE clave = 'nombre_impresora'")
            resultado = cursor.fetchone()
            nombre_impresora = resultado[0] if resultado else None

            if not nombre_impresora:
                print("Error: No se encontró un nombre de impresora configurado.")
                return
            hprinter = win32print.OpenPrinter(nombre_impresora)
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(nombre_impresora)
    
            hdc.StartDoc("Factura")
            hdc.StartPage()    

            fuente_distri = win32ui.CreateFont({
                "name": "Arial",
                "height": 33,  
                "weight": 700,
            })
            fuente_normal = win32ui.CreateFont({
                "name": "Arial",
                "height": 26,  
                "weight": 400,
            })
            fuente_negrita = win32ui.CreateFont({
                "name": "Arial",
                "height": 26,
                "weight": 700,
            })
            hdc.SelectObject(fuente_distri)
    
            y = 0 
            
            ancho_pagina = 600
            titulos = [
                "DISTRIARBELAEZ"
            ]
            for titu in titulos:
                ancho_texto = hdc.GetTextExtent(titu)[0] 
                x = (ancho_pagina - ancho_texto) // 2
                hdc.TextOut(x, y, titu) 
                y += 40 

            hdc.SelectObject(fuente_negrita)
            

            textos = []
            claves = ["nombre","nit", "direccion", "telefono"]
            for clave in claves:
                cursor.execute("SELECT valor FROM ajustes WHERE clave = ?", (clave,))
                resultado = cursor.fetchone()
                textos.append(resultado[0] if resultado else "No disponible")



            for texto in textos:
                ancho_texto = hdc.GetTextExtent(texto)[0] 
                x = (ancho_pagina - ancho_texto) // 2
                hdc.TextOut(x, y, texto) 
                y += 40 


            hdc.TextOut(80, y, f"Fecha exp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            y += 30

            hdc.SelectObject(fuente_negrita)

            hdc.TextOut(80, y, f"Cliente: {self.campo_nombre_cliente.get()}")
            y += 50

            hdc.SelectObject(fuente_normal)
            cursor.execute("""
                SELECT direccion FROM clientes WHERE nombre_cliente = ?
            """, (self.campo_nombre_cliente.get(),))
            direccion_cliente = cursor.fetchone()
            direccion_texto = f"Dirección: {direccion_cliente[0]}" if direccion_cliente else "Dirección:"
            hdc.TextOut(80, y, direccion_texto)
            y += 50

            hdc.TextOut(60, y, "CNT")
            hdc.TextOut(130, y, "Producto")
            hdc.TextOut(360, y, "Precio")
            hdc.TextOut(460, y, "Subtotal")
            y += 40

            hdc.SelectObject(fuente_normal)


            for child in self.tree.get_children():
                item = self.tree.item(child, "values")
                hdc.TextOut(60, y, item[1]) 
                hdc.TextOut(130, y, item[0])  
                hdc.TextOut(360, y, item[2]) 
                hdc.TextOut(460, y, item[3])  
                y += 30


            hdc.SelectObject(fuente_normal)
            hdc.SelectObject(fuente_negrita)


            hdc.TextOut(60, y, "SUBTOTAL")
            hdc.TextOut(230, y, "DCTO")
            hdc.TextOut(360, y, "IVA")
            hdc.TextOut(460, y, "TOTAL")
            y += 40
            descuento = 0
            iva = 0

            hdc.TextOut(60, y, self.label_suma_total.cget('text').split(': ')[1]) 
            hdc.TextOut(230, y, f"${descuento}")    
            hdc.TextOut(360, y, f"${iva}")
            hdc.TextOut(460, y, self.label_suma_total.cget('text').split(': ')[1])  
            y += 30

            
            hdc.SelectObject(fuente_normal)



            fecha_emision = datetime.now()
            fecha_final = fecha_emision.replace(year=fecha_emision.year + 1)
            textosReso = [
                "Resolucion No. 123456",
                f"Del {fecha_emision.strftime('%Y-%m-%d')} hasta {fecha_final.strftime('%Y-%m-%d')}",
            ]


            for textores in textosReso:
                ancho_texto = hdc.GetTextExtent(textores)[0] 
                x = (ancho_pagina - ancho_texto) // 2
                hdc.TextOut(x, y, textores) 
                y += 40

            hdc.SelectObject(fuente_negrita)

            hdc.TextOut(160, y, "NO RESPONSABLE DE IVA")
            hdc.EndPage()
            hdc.EndDoc()

        except Exception as e:
            print(f"Error al imprimir la factura: {e}")
        finally:
            if 'hprinter' in locals():
                win32print.ClosePrinter(hprinter)

    def buscar_factura(self, tree, criterio_busqueda):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
    
            query = """
            SELECT factura, fecha, nombre_cliente, SUM(subtotal)
            FROM ventas 
            WHERE fecha LIKE ?
            GROUP BY factura
            """
            c.execute(query, ('%' + criterio_busqueda + '%',))
    
            resultados = c.fetchall()
    
            # Limpiar las filas existentes en el Treeview
            tree.delete(*tree.get_children())
    
            # Insertar los resultados con colores alternados
            for i, factura in enumerate(resultados):
                # Aplicar etiquetas alternadas para las filas
                tags = ('oddrow',) if i % 2 == 0 else ('evenrow',)
                tree.insert("", "end", values=factura, tags=tags)
    
            conn.close()
    
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al buscar la factura: {e}")
    
