import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import utils.centrar_ventana as util_ventana_centrar
from modules.inventario import inventario_main
from modules.facturacion import Facturacion_main
from modules.clientes import clientes_main
from modules.reportes import reportes_main
from modules.ajustes import ajustes_main
from theme.colores import color_barra_superior,color_cuerpo_principal,color_menu_lateral,color_botones_lateral_cursor

#ventana principal

class ventana_principal(ctk.CTk):
    def __init__(self):
        super().__init__() 
        self.panel()
        self.botones_barra_lateral()
        self.logo_barra_superior()
        self.boton_salir_barra_lateral()
        self.inicio_boton()
        self.configurar_ventana()

    #configuracion de ventana principal
    def configurar_ventana(self):
        self.ventana=ctk.set_appearance_mode("dark")
        self.title("Distriarbelaez")
        self.iconbitmap("icono.ico")
        w, h = 1200, 700
        util_ventana_centrar.centrar(self, w, h)  
        
    #frames de ventana principal
    def panel(self):
        self.barra_superior = ctk.CTkFrame(self, corner_radius=0, fg_color=color_barra_superior ,height=50)
        self.barra_superior.pack(side="top",fill="x", expand=False)
        self.barra_superior.pack_propagate(False)

        self.barra_lateral = ctk.CTkFrame(self, corner_radius=0, fg_color=color_menu_lateral)
        self.barra_lateral.pack(side="left",fill="y", expand=False)

        self.cuerpo_principal = ctk.CTkFrame(self,fg_color=color_cuerpo_principal,width=150,corner_radius=0)
        self.cuerpo_principal.pack(side=tk.RIGHT,fill='both' ,expand=True)
        
    
    
    #imagen barra superior
    def logo_barra_superior(self):
        imagen = Image.open("imagenes/logo_distri.png")
        imagen = imagen.resize((100, 100), Image.LANCZOS)
        imagen_ctk = ctk.CTkImage(imagen, size=(40, 40))

        self.imagen_label = ctk.CTkButton(self.barra_superior,font=('Roboto', 12), image=imagen_ctk, text="Distriarbelaez",fg_color=color_barra_superior,hover_color=color_botones_lateral_cursor,command=(self.inicio_boton))
        self.imagen_label.image = imagen_ctk 
        self.imagen_label.pack(side="left", padx=5, pady=5)
    
    #botones de funciones
    
    def botones_barra_lateral(self):
        #icono inventario
        imagen_inventario = Image.open("imagenes/icono_inventario.png")
        imagen_inventario = imagen_inventario.resize((50, 50), Image.LANCZOS)
        imagen_ctk_inventario = ctk.CTkImage(imagen_inventario, size=(35, 35))
        
        #icono facturacion
        imagen_facturacion = Image.open("imagenes/icono_facturacion.png")
        imagen_facturacion  = imagen_facturacion .resize((50, 50), Image.LANCZOS)
        imagen_ctk_facturacion = ctk.CTkImage(imagen_facturacion, size=(35, 35))
        
        #icono reportes
        imagen_reportes = Image.open("imagenes/icono_reportes.png")
        imagen_reportes = imagen_reportes.resize((50, 50), Image.LANCZOS)
        imagen_ctk_reportes = ctk.CTkImage(imagen_reportes, size=(35, 35))
        
        #icono contactos
        imagen_contactos = Image.open("imagenes/icono_contactos.png")
        imagen_contactos= imagen_contactos.resize((50, 50), Image.LANCZOS)
        imagen_ctk_contactos = ctk.CTkImage(imagen_contactos, size=(35, 35))

        imagen_ajustes = Image.open("imagenes/icono_ajustes.png")
        imagen_ajustes= imagen_ajustes.resize((50, 50), Image.LANCZOS)
        imagen_ctk_ajustes = ctk.CTkImage(imagen_ajustes, size=(35, 35))
        
        #botones
        self.boton1 = ctk.CTkButton(self.barra_lateral, image=imagen_ctk_inventario, text="Inventario",font=("Roboto",14), command=self.abrir_panel_inventario
        ,fg_color="transparent",hover_color=color_barra_superior, corner_radius=32,border_color=color_barra_superior, border_width=2)
        self.boton1.pack(pady=10, padx=10, fill="x")

        self.boton2 = ctk.CTkButton(self.barra_lateral, image=imagen_ctk_facturacion, text="Facturacion",font=("Roboto",14), command=self.abrir_panel_facturacion
        ,fg_color="transparent",hover_color=color_barra_superior, corner_radius=32,border_color=color_barra_superior, border_width=2)
        self.boton2.pack(pady=10, padx=10, fill="x")

        self.boton3 = ctk.CTkButton(self.barra_lateral, image=imagen_ctk_reportes, text="Reportes",font=("Roboto",14), command=self.abrir_panel_reportes
        ,fg_color="transparent",hover_color=color_barra_superior, corner_radius=32,border_color=color_barra_superior, border_width=2)
        self.boton3.pack(pady=10, padx=10, fill="x")
        
        self.boton4 = ctk.CTkButton(self.barra_lateral, image=imagen_ctk_contactos, text="Clientes",font=("Roboto",14),command=self.abrir_panel_clientes
        ,fg_color="transparent",hover_color=color_barra_superior, corner_radius=32,border_color=color_barra_superior, border_width=2)
        self.boton4.pack(pady=10, padx=10, fill="x")

        self.boton4 = ctk.CTkButton(self.barra_lateral, image=imagen_ctk_ajustes, text="Ajustes",font=("Roboto",14),command=self.abrir_panel_ajustes
        ,fg_color="transparent",hover_color=color_barra_superior, corner_radius=32,border_color=color_barra_superior, border_width=2)
        self.boton4.pack(pady=10, padx=10, fill="x")


        #ir a funciones
    def abrir_panel_inventario(self):
        self.limpiar_cuerpo(self.cuerpo_principal)
        inventario_main(self.cuerpo_principal)

    def abrir_panel_facturacion(self):
        self.limpiar_cuerpo(self.cuerpo_principal)
        Facturacion_main(self.cuerpo_principal)
        
    def abrir_panel_clientes(self):
        self.limpiar_cuerpo(self.cuerpo_principal)
        clientes_main(self.cuerpo_principal)  

    def abrir_panel_reportes(self):
        self.limpiar_cuerpo(self.cuerpo_principal)
        reportes_main(self.cuerpo_principal)   

    def abrir_panel_ajustes(self):
        self.limpiar_cuerpo(self.cuerpo_principal)
        ajustes_main(self.cuerpo_principal)  

    # Limpiar cuerpo
    def limpiar_cuerpo(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()
        
    #boton barra lateral salir
    def boton_salir_barra_lateral(self):
        imagen = Image.open("imagenes/icono_cerrar_sesion.png")
        imagen = imagen.resize((50, 50), Image.LANCZOS)
        imagen_ctk = ctk.CTkImage(imagen, size=(40, 40))

        self.imagen_label = ctk.CTkButton(self.barra_lateral,text="Salir",font=("Roboto", 14), image=imagen_ctk,fg_color=color_barra_superior,hover_color=color_botones_lateral_cursor,command=self.abrir_inicio_sesion)
        self.imagen_label.image = imagen_ctk 
        self.imagen_label.pack(side="bottom", padx=0, pady=5) 
        
    #inicio de ventana principal
    def inicio_boton(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()
        
        # Mensaje de bienvenida
        bienvenida = ctk.CTkLabel(self.cuerpo_principal, text="Bienvenido a Distriarbelaez", font=("Roboto", 24), text_color="#666a88")
        bienvenida.pack(pady=20, padx=20)

        # Cargar y mostrar el logo en grande
        imagen_logo = Image.open("imagenes/logo_distri.png")
        imagen_logo = imagen_logo.resize((450,450), Image.LANCZOS)  # Ajusta el tamaño del logo
        imagen_ctk_logo = ctk.CTkImage(imagen_logo, size=(450, 450))

        logo_label = ctk.CTkLabel(self.cuerpo_principal, image=imagen_ctk_logo, text="")
        logo_label.image = imagen_ctk_logo  
        logo_label.pack(pady=20, padx=20)   

        
    #volver a inicio de sesion
    def abrir_inicio_sesion(self):
        from view.login_ventana import ventana_inicio_sesion
        self.destroy() 
        inicio_sesion = ventana_inicio_sesion()
        inicio_sesion.mainloop()

            
if __name__ == "__main__":

    ventana=ventana_principal()
    ventana.mainloop()