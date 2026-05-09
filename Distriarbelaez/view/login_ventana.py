import customtkinter as ctk
import tkinter as tk
import utils.centrar_ventana as util_ventana_centrar
from view.login_verificar import verificar_login
from PIL import Image, ImageTk

#crear clase
class ventana_inicio_sesion(ctk.CTk):
    def __init__(self):
        super().__init__() 
        self.configurar_ventana()
        self.panel_login()
        self.bind("<Return>", self.iniciar_sesion)
        
    # Configuración de ventana principal
    def configurar_ventana(self):
        self.title("Distriarbelaez")
        self.iconbitmap("imagenes/logo_distri.ico")
        ctk.set_appearance_mode("dark")
        w, h = 1100, 700
        util_ventana_centrar.centrar(self, w, h)


    # Panel de login
    def panel_login(self):

        self.panel_inicio_sesion = ctk.CTkFrame(self, corner_radius=0, width=400)
        self.panel_inicio_sesion.place(relx=0.5, rely=0.5, anchor="center", relheight=1) 
        
        self.login_label = ctk.CTkLabel(self.panel_inicio_sesion, text="Distriarbelaez\nIniciar sesión",
            font=ctk.CTkFont('Roboto',size=25, weight="bold"))
        self.login_label.grid(padx=30, pady=(150, 15))
        
        self.input_usuario = ctk.CTkEntry(self.panel_inicio_sesion, width=200, placeholder_text="Usuario")
        self.input_usuario.grid(row=1, column=0, padx=30, pady=(15, 15))
        
        self.input_contraseña = ctk.CTkEntry(self.panel_inicio_sesion, width=200, placeholder_text="Contraseña",show="*")
        self.input_contraseña.grid(row=2, column=0, padx=30, pady=(0, 15))
        
        self.login_boton = ctk.CTkButton(self.panel_inicio_sesion, text="Iniciar sesión", width=200, command=self.iniciar_sesion)
        self.login_boton.grid(row=3, column=0, padx=30, pady=(15, 15))

    def iniciar_sesion(self, event=None):
        usuario = self.input_usuario.get()
        contraseña = self.input_contraseña.get()

        if verificar_login(usuario, contraseña):
            from view.inicio import ventana_principal
            self.destroy() 
            inicio = ventana_principal()
            inicio.mainloop()
        else:
            self.mensaje_temporal("Usuario o contraseña incorrectos")

    def mensaje_temporal(self, mensaje, duracion=1000):
        mensaje_tem = ctk.CTkLabel(self, text=mensaje, font=ctk.CTkFont(size=13, weight="bold"), fg_color="red")
        mensaje_tem.place(relx=0.5, rely=0.2, anchor="center")
        self.after(duracion, mensaje_tem.destroy)

if __name__ == "__main__":
    app = ventana_inicio_sesion()
    app.mainloop()
