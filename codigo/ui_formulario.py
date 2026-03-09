import customtkinter as ctk

class UIFormularioPrincipal:
    def __init__(self, app):
        self.app = app

    def cargar_interfaz_principal(self, modo="nuevo"):
        self.app.modo_actual = modo 
        self.app.limpiar_ventana()
        self.app.set_background("fondo_win.jpg")
        
        marco_superior = ctk.CTkFrame(self.app, fg_color="transparent")
        marco_superior.pack(fill="x", padx=20, pady=5)
        
        boton_volver = ctk.CTkButton(marco_superior, text="⬅ Volver", fg_color="#7f8c8d", width=80, command=self.app.mostrar_menu_bienvenida)
        boton_volver.pack(side="left")
        
        if modo == "nuevo":
            texto_modo = "📝 MODO: NUEVO REGISTRO"
            color_modo = "#27ae60"
        else:
            texto_modo = "🔍 MODO: EDICIÓN Y GESTIÓN"
            color_modo = "#2980b9"
        
        self.app.lbl_modo = ctk.CTkLabel(marco_superior, text=texto_modo, font=("Segoe UI", 16, "bold"), text_color=color_modo)
        self.app.lbl_modo.pack(side="left", padx=20)
        
        boton_ayuda = ctk.CTkButton(marco_superior, text="❓ AYUDA", fg_color="#f39c12", text_color="white", width=100, font=("bold", 12), command=self.app.mostrar_ayuda)
        boton_ayuda.pack(side="right", padx=10)
        
        if modo == "buscar":
            marco_busqueda = ctk.CTkFrame(self.app, fg_color="white", corner_radius=10)
            marco_busqueda.pack(fill="x", padx=20, pady=5)
            
            etiqueta_busqueda = ctk.CTkLabel(marco_busqueda, text="Búsqueda:", font=("bold", 12))
            etiqueta_busqueda.pack(side="left", padx=(15, 5))
            
            self.app.entry_buscar = ctk.CTkEntry(marco_busqueda, placeholder_text="Escriba nombre o cédula...", height=35)
            self.app.entry_buscar.pack(side="left", padx=5, pady=10, expand=True, fill="x")
            self.app.entry_buscar.bind("<KeyRelease>", self.app.actualizar_busqueda_dinamica)
            
            def buscar_ahora():
                texto_buscado = self.app.entry_buscar.get()
                self.app.cargar_registro_desde_busqueda(texto_buscado)
                
            boton_lupa = ctk.CTkButton(marco_busqueda, text="🔍 BUSCAR", width=100, height=35, command=buscar_ahora)
            boton_lupa.pack(side="left", padx=10)
            
            if self.app.rol_actual == "Administrador":
                boton_borrar = ctk.CTkButton(marco_busqueda, text="ELIMINAR", width=100, height=35, fg_color="#e74c3c", command=self.app.eliminar_registro_ui)
                boton_borrar.pack(side="right", padx=15)
        else:
            self.app.entry_buscar = None

        self.app.lista_resultados = ctk.CTkScrollableFrame(self.app, height=150, width=500, fg_color="#f8f9f9", corner_radius=5, border_width=1)
        self.app.scroll = ctk.CTkScrollableFrame(self.app, fg_color="transparent")
        self.app.scroll.pack(expand=True, fill="both", padx=10, pady=5)
        self.app.inputs = {}
        self.app.combos = {}
        
        marco_columnas = ctk.CTkFrame(self.app.scroll, fg_color="transparent")
        marco_columnas.pack(fill="x", expand=True)

        # SECCIÓN IZQUIERDA
        marco_izquierdo = ctk.CTkFrame(marco_columnas, corner_radius=15, fg_color="white")
        marco_izquierdo.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        
        titulo_personales = ctk.CTkLabel(marco_izquierdo, text="DATOS PERSONALES", font=("bold", 14), text_color="#2980b9")
        titulo_personales.pack(pady=10)
        
        self.app.crear_input(marco_izquierdo, "Nombre Completo", "nombre", placeholder="Ej: Leonardo Moreno", val_type="letras")
        
        fila_dni = ctk.CTkFrame(marco_izquierdo, fg_color="transparent")
        fila_dni.pack(fill="x", padx=15)
        
        self.app.crear_input(fila_dni, "Cédula", "cedula", pack_side="left", placeholder="Solo números", val_type="numeros")
        self.app.crear_input(fila_dni, "Fecha Nacimiento", "fnac", pack_side="right", placeholder="DD/MM/AAAA", val_type="fecha")
        self.app.crear_input(marco_izquierdo, "Correo Electrónico", "correo", placeholder="correo@ejemplo.com")
        self.app.crear_input(marco_izquierdo, "Teléfono", "telf", placeholder="04120000000", val_type="numeros")
        self.app.crear_input(marco_izquierdo, "Dirección", "dir", placeholder="Calle, Sector, Ciudad")
        
        etiqueta_obs = ctk.CTkLabel(marco_izquierdo, text="Observaciones", font=("Segoe UI", 11, "bold"))
        etiqueta_obs.pack(anchor="w", padx=20, pady=(5,0))
        
        self.app.txt_obs = ctk.CTkTextbox(marco_izquierdo, height=100, border_width=1, border_color="#abb2b9")
        self.app.txt_obs.pack(fill="x", padx=20, pady=(0, 20))

        # SECCIÓN DERECHA
        marco_derecho = ctk.CTkFrame(marco_columnas, corner_radius=15, fg_color="white")
        marco_derecho.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.crear_seccion_institucional(marco_derecho)

        self.app.cargar_datos_combos_inicial()

        marco_botones = ctk.CTkFrame(self.app, fg_color="transparent")
        marco_botones.pack(fill="x", padx=20, pady=10)
        
        if self.app.modo_actual == "nuevo":
            color_boton = "#27ae60"
            texto_boton = "💾 GUARDAR"
            color_hover = "#1e8449"
        else:
            color_boton = "#2980b9"
            texto_boton = "💾 ACTUALIZAR CAMBIOS"
            color_hover = "#1a5276"

        self.btn_guardar = ctk.CTkButton(marco_botones, text=texto_boton, fg_color=color_boton, 
                                         hover_color=color_hover,
                                         height=45, command=self.app.guardar_ui)
        self.btn_guardar.pack(side="left", expand=True, fill="x", padx=5)
        
        boton_word = ctk.CTkButton(marco_botones, text="📄 GENERAR DESIGNACIÓN", fg_color="#e67e22", height=45, command=self.app.generar_word_ui)
        boton_word.pack(side="left", expand=True, fill="x", padx=5)
        
        boton_limpiar = ctk.CTkButton(marco_botones, text="🧹 LIMPIAR TODO", fg_color="#95a5a6", height=45, command=self.app.limpiar_formulario)
        boton_limpiar.pack(side="left", expand=True, fill="x", padx=5)

    def crear_seccion_institucional(self, f_der):
        etiqueta_titulo = ctk.CTkLabel(f_der, text="DATOS INSTITUCIONALES", font=("bold", 14), text_color="#2980b9")
        etiqueta_titulo.pack(pady=10)
        
        self.app.crear_combo(f_der, "Universidad", "uni", command=self.app.cargar_especialidades_por_uni)
        
        self.app.crear_input(f_der, "Especialidad", "esp", placeholder="Escriba o seleccione universidad")
        
        self.app.crear_combo(f_der, "Centro de Salud", "cen", command=self.app.actualizar_responsable_en_pantalla)
        
        self.app.lbl_responsable = ctk.CTkLabel(f_der, text="Responsable: (Seleccione un centro)", font=("Segoe UI", 10, "italic"), text_color="#3498db")
        self.app.lbl_responsable.pack(anchor="w", padx=25, pady=(0, 10))

        self.app.crear_input(f_der, "Guardias Asignadas", "guardias", placeholder="Ej: Lunes y Miércoles")
        
        self.app.crear_combo(f_der, "Cargo", "car")
        self.app.crear_combo(f_der, "Modalidad", "mod")
        
        fila_fechas = ctk.CTkFrame(f_der, fg_color="transparent")
        fila_fechas.pack(fill="x", padx=15, pady=5)
        
        self.app.crear_input(fila_fechas, "Fecha Inicio", "ini", pack_side="left", placeholder="DD/MM/AAAA", val_type="fecha")
        self.app.crear_input(fila_fechas, "Fecha Fin", "fin", pack_side="right", placeholder="DD/MM/AAAA", val_type="fecha")