import customtkinter as ctk

class UIMenuPrincipal:
    def __init__(self, app):
        self.app = app

    def mostrar_menu_bienvenida(self):
        self.app.limpiar_ventana()
        self.app.set_background("fondo_app.jpg")
        
        # Marco de arriba
        marco_arriba = ctk.CTkFrame(self.app, height=50, corner_radius=0)
        marco_arriba.pack(fill="x")
        
        texto_usuario = f"👤 {self.app.usuario_actual} | {self.app.rol_actual}"
        etiqueta_usuario = ctk.CTkLabel(marco_arriba, text=texto_usuario, padx=20)
        etiqueta_usuario.pack(side="left")
        
        boton_salir = ctk.CTkButton(marco_arriba, text="Cerrar Sesión", fg_color="#c0392b", width=100, command=self.app.mostrar_login)
        boton_salir.pack(side="right", padx=10, pady=5)
        
        # Marco del centro
        marco_centro = ctk.CTkFrame(self.app, fg_color=("white", "gray20"), corner_radius=15)
        marco_centro.place(relx=0.5, rely=0.5, anchor="center")
        
        titulo_menu = ctk.CTkLabel(marco_centro, text="MENU PRINCIPAL", font=("Segoe UI", 22, "bold"))
        titulo_menu.pack(pady=30, padx=50)

        # Funciones para los botones
        def ir_nuevo():
            self.app.cargar_interfaz_principal(modo="nuevo")
            
        def ir_buscar():
            self.app.cargar_interfaz_principal(modo="buscar")
        
        boton_nuevo = ctk.CTkButton(marco_centro, text="📝 Nuevo Registro", width=300, height=45, command=ir_nuevo)
        boton_nuevo.pack(pady=10)
        
        boton_buscar = ctk.CTkButton(marco_centro, text="🔍 Buscar y Gestionar", width=300, height=45, command=ir_buscar)
        boton_buscar.pack(pady=10)
        
        boton_excel = ctk.CTkButton(marco_centro, text="📂 Exportar a Excel", width=300, height=45, fg_color="#27ae60", command=self.app.exportar_excel_ui)
        boton_excel.pack(pady=10)
        
        if self.app.rol_actual == "Administrador":
            boton_backup = ctk.CTkButton(marco_centro, text="💾 Crear Respaldo (Backup)", width=300, height=45, fg_color="#8e44ad", command=self.app.respaldar_bd_ui)
            boton_backup.pack(pady=10)


        total = self.app.obtener_total_registros()
        self.btn_contador = ctk.CTkButton(
           self.app, 
           text=f"📊 Total Registros: {total}",
           command=self.mostrar_detalles_registros,
           width=200,
           height=50,
           font=("Segoe UI", 14, "bold")
        )

        self.btn_contador.place(relx=0.1, rely=0.5, anchor="w")

    def mostrar_detalles_registros(self):
        import basededatos as db
        total, centros = db.obtener_estadisticas_detalladas()
    
        ventana_info = ctk.CTkToplevel(self.app)
        ventana_info.title("Desglose de Registros")
        ventana_info.geometry("300x200")
        ventana_info.attributes("-topmost", True)
    
        ctk.CTkLabel(ventana_info, text="📊 Resumen del Sistema", font=("Segoe UI", 16, "bold")).pack(pady=10)
    
        ctk.CTkLabel(ventana_info, text=f"• Total de registros: {total}", font=("Segoe UI", 13)).pack(anchor="w", padx=20)
        ctk.CTkLabel(ventana_info, text=f"• Centros con registros: {centros}", font=("Segoe UI", 13)).pack(anchor="w", padx=20)
    
        btn_cerrar = ctk.CTkButton(ventana_info, text="Entendido", command=ventana_info.destroy)
        btn_cerrar.pack(pady=20)