import customtkinter as ctk
import time
import threading
from tkinter import messagebox
import basededatos as db

class UILogin:
    def __init__(self, app):
        self.app = app # Ventana principal

    def mostrar_pantalla_carga(self):
        self.app.limpiar_ventana()
        self.app.set_background("fondo_carga.jpg")
        
        # Marco blanco del centro
        marco_carga = ctk.CTkFrame(self.app, fg_color="#ffffff", corner_radius=20)
        marco_carga.place(relx=0.5, rely=0.5, anchor="center")
        
        etiqueta_carga = ctk.CTkLabel(marco_carga, text="Cargando Módulos...", font=("Segoe UI", 24, "bold"))
        etiqueta_carga.pack(pady=20, padx=40)
        
        self.barra_progreso = ctk.CTkProgressBar(marco_carga, width=400)
        self.barra_progreso.pack(pady=10, padx=20)
        self.barra_progreso.set(0)
        
        # Iniciar hilo de carga
        hilo = threading.Thread(target=self.simular_carga)
        hilo.start()

    def simular_carga(self):
        for numero in range(101):
            time.sleep(0.01) 
            self.barra_progreso.set(numero / 100)
            self.app.update_idletasks()
        self.app.after(500, self.mostrar_login)

    def mostrar_login(self):
        self.app.limpiar_ventana()
        self.app.set_background("fondo_login.jpg")
        
        # Marco para el login
        marco_ingreso = ctk.CTkFrame(self.app, corner_radius=20, width=400, height=450, fg_color="white")
        marco_ingreso.place(relx=0.5, rely=0.5, anchor="center")
        
        etiqueta_titulo = ctk.CTkLabel(marco_ingreso, text="Acceso al Sistema", font=("Segoe UI", 26, "bold"), text_color="#3b8ed0")
        etiqueta_titulo.pack(pady=(40, 10))
        
        self.caja_usuario = ctk.CTkEntry(marco_ingreso, placeholder_text="Usuario", width=250, height=40)
        self.caja_usuario.pack(pady=15)
        
        self.caja_clave = ctk.CTkEntry(marco_ingreso, placeholder_text="Contraseña", show="*", width=250, height=40)
        self.caja_clave.pack(pady=15)
        
        self.caja_usuario.bind("<Return>", self.validar_login_ui)
        self.caja_clave.bind("<Return>", self.validar_login_ui)
        
        # Boton Ingresar
        boton_ingresar = ctk.CTkButton(marco_ingreso, text="INGRESAR", width=250, height=45, command=self.validar_login_ui)
        boton_ingresar.pack(pady=30)

    def validar_login_ui(self, event=None):
        usuario_escrito = self.caja_usuario.get()
        clave_escrita = self.caja_clave.get()
        
        resultado = db.validar_login(usuario_escrito, clave_escrita)
        
        if resultado is not None:
            self.app.usuario_actual = usuario_escrito
            self.app.rol_actual = resultado[0]
            self.app.mostrar_menu_bienvenida()
        else:
            messagebox.showerror("Error", "Usuario o Contraseña incorrectos")
