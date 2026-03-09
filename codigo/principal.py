import os
import time
import sqlite3
import threading
import customtkinter as ctk
import tkinter as tk

from tkinter import messagebox
from PIL import Image

import basededatos as db
import documentos as docs

from ui_login import UILogin
from ui_menu import UIMenuPrincipal
from ui_formulario import UIFormularioPrincipal

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AppFinalPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Registro Médico")
        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        try:
            self.state("fullscreen") 
        except:
            self.geometry("1200x800") 

        self.usuario_actual = ""
        self.rol_actual = ""
        self.imagenes = {}
        self.modo_actual = "nuevo"
        
        self.vcmd_letra = (self.register(self.validar_letras), '%P')
        self.vcmd_num = (self.register(self.validar_numeros), '%P')
        self.vcmd_fecha = (self.register(self.validar_fecha), '%P')
        
        self.inputs = {}
        self.inputs["fnac"] = ctk.CTkEntry(self)
        self.inputs["fnac"].pack()
        
        self.inputs["ini"] = ctk.CTkEntry(self)
        self.inputs["ini"].pack()
        
        self.inputs["fin"] = ctk.CTkEntry(self)
        self.inputs["fin"].pack()

        self.inputs["fnac"].bind("<FocusOut>", lambda e: self.validar_fechas_tiempo_real(e, "Fecha de Nacimiento"))
        self.inputs["ini"].bind("<FocusOut>", lambda e: self.validar_fechas_tiempo_real(e, "Fecha de Inicio"))
        self.inputs["fin"].bind("<FocusOut>", lambda e: self.validar_fechas_tiempo_real(e, "Fecha de Finalización"))
        
        self.protocol("WM_DELETE_WINDOW", self.confirmar_salida)
        
        self.login_ui = UILogin(self)
        self.menu_ui = UIMenuPrincipal(self)
        self.form_ui = UIFormularioPrincipal(self)
        
        db.crear_db()
        db.inicializar_datos_semilla() 
        self.mostrar_pantalla_carga()


    def cerrar_aplicacion(self):
        """Detiene todas las tareas y cierra la ventana de forma segura."""
        try:
            self.root.quit()
            self.root.destroy()
        except Exception:
            pass

    def convertir_a_mayusculas(self, event):
        widget = event.widget
        posicion_cursor = widget.index("insert")
    
        texto_original = widget.get()
    
        nuevo_texto = texto_original.upper()
    
        if texto_original != nuevo_texto:
            widget.delete(0, "end")
            widget.insert(0, nuevo_texto)
        
            widget.icursor(posicion_cursor)

    def validar_letras(self, texto_nuevo):
        if texto_nuevo == "" or texto_nuevo == "Ej: Leonardo David Moreno Bruce": 
            return True
            
        for letra in texto_nuevo:
            if not (letra.isalpha() or letra.isspace()):
                return False
        return True

    def validar_numeros(self, texto_nuevo):
        if texto_nuevo == "" or texto_nuevo == "Solo números" or texto_nuevo == "04120000000": return True
        return texto_nuevo.isdigit()

    def validar_fecha(self, texto_nuevo):
        if texto_nuevo == "" or texto_nuevo == "DD/MM/AAAA": 
            return True
            
        for caracter in texto_nuevo:
            if not (caracter.isdigit() or caracter == "/" or caracter == "-"):
                return False
        return True
    
    def auto_formatear_fecha(self, event, widget_entry):
        if event.keysym in ("BackSpace", "Delete", "Left", "Right"): return
        texto = widget_entry.get()
        numeros = "".join(filter(str.isdigit, texto))
        if len(numeros) > 8: numeros = numeros[:8]
        res = ""
        for i, n in enumerate(numeros):
            if i in (2, 4): res += "/"
            res += n
        if widget_entry.get() != res:
            widget_entry.delete(0, 'end')
            widget_entry.insert(0, res)
   
    def set_background(self, nombre_imagen):
        import os
        ruta_imagen = os.path.join("imagenes", nombre_imagen)
        try:
            if nombre_imagen not in self.imagenes:
                img_pil = Image.open(ruta_imagen)
                w, h = self.winfo_screenwidth(), self.winfo_screenheight()
                img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(w, h))
                self.imagenes[nombre_imagen] = img_ctk
            
            bg_label = ctk.CTkLabel(self, text="", image=self.imagenes[nombre_imagen])
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except Exception:
            self.configure(fg_color="#f0f0f0")

    def limpiar_ventana(self):
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_pantalla_carga(self):
        self.login_ui.mostrar_pantalla_carga()

    def mostrar_login(self):
        self.login_ui.mostrar_login()

    def mostrar_menu_bienvenida(self):
        self.menu_ui.mostrar_menu_bienvenida()

    def cargar_interfaz_principal(self, modo="nuevo"):
        self.form_ui.cargar_interfaz_principal(modo)

    def crear_input(self, master, label, key, pack_side=None, placeholder="", val_type=None):
        if pack_side:
            f = ctk.CTkFrame(master, fg_color="transparent"); f.pack(side=pack_side, expand=True, fill="x", padx=2)
            master = f
        ctk.CTkLabel(master, text=label, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20)
        
        entry = ctk.CTkEntry(master, height=30, placeholder_text=placeholder)

        entry.bind("<KeyRelease>", self.convertir_a_mayusculas)
        
        if val_type == "letras": entry.configure(validate="key", validatecommand=self.vcmd_letra)
        elif val_type == "numeros": entry.configure(validate="key", validatecommand=self.vcmd_num)
        elif val_type == "fecha": 
            entry.configure(validate="key", validatecommand=self.vcmd_fecha)
            entry.bind("<KeyRelease>", lambda e, w=entry: self.auto_formatear_fecha(e, w))
            
        if key == "cedula":
            entry.bind("<FocusOut>", self.verificar_cedula_existente)
    
        if key in ["fnac", "ini", "fin"]:
            entry.bind("<FocusOut>", lambda e, k=key: self.validar_fechas_tiempo_real(e, k))
            
        if key == "correo":
           entry.bind("<KeyRelease>", lambda e: self.validar_formato_correo_visual(entry), add="+")
           vcmd_espacios = (self.register(self.bloquear_espacios), '%P')
           entry.configure(validate="key", validatecommand=vcmd_espacios)
           entry.bind("<KeyRelease>", lambda e: self.procesar_texto_correo(e, entry))
        else:
           entry.bind("<KeyRelease>", self.convertir_a_mayusculas)
    
        self.inputs[key] = entry
        entry.pack(fill="x", padx=20, pady=(0, 10))          

    def crear_combo(self, master, label, key, command=None):
        ctk.CTkLabel(master, text=label, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20)
        self.combos[key] = ctk.CTkComboBox(master, height=30, state="readonly", command=command)
        self.combos[key].pack(fill="x", padx=20, pady=(0, 10))

    def cargar_datos_combos_inicial(self):
        self.combos["uni"].configure(values=db.obtener_opciones("universidades"))
        self.combos["cen"].configure(values=db.obtener_opciones("centros"))
        self.combos["car"].configure(values=db.obtener_opciones("cargos"))
        self.combos["mod"].configure(values=db.obtener_opciones("modalidades"))

    def cargar_especialidades_por_uni(self, uni):
        """Ahora rellena un CTkEntry en lugar de un CTkComboBox"""
        res = db.obtener_opciones("oferta_academica", "especialidad", "universidad", uni)
        self.inputs["esp"].delete(0, 'end')
        if res: 
            self.inputs["esp"].insert(0, res[0])

    def cargar_guardias_por_centro(self, centro):
        """Ahora rellena un CTkEntry en lugar de un CTkComboBox"""
        res = db.obtener_opciones("guardias_centro", "guardia", "centro", centro)
        self.inputs["guardias"].delete(0, 'end')
        if res: 
            self.inputs["guardias"].insert(0, res[0])
            
    def actualizar_responsable_en_pantalla(self, centro_seleccionado):
        self.cargar_guardias_por_centro(centro_seleccionado)
        nombre = db.obtener_responsable_centro(centro_seleccionado)
        
        if nombre:
            self.lbl_responsable.configure(text=f"✅ Responsable: {nombre}", text_color="#27ae60")
        else:
            self.lbl_responsable.configure(text="⚠️ Centro sin responsable asignado", text_color="#e74c3c")

    def actualizar_busqueda_dinamica(self, event=None):
        if not hasattr(self, 'entry_buscar') or self.entry_buscar is None: return
        texto = self.entry_buscar.get().strip()
        for widget in self.lista_resultados.winfo_children(): widget.destroy()
        if texto == "":
            self.lista_resultados.place_forget()
            return
            
        res = db.buscar_registros_dinamico(texto)
        
        if res:
            self.lista_resultados.place(x=self.entry_buscar.winfo_rootx() - self.winfo_rootx(), 
                                        y=(self.entry_buscar.winfo_rooty() - self.winfo_rooty()) + 40)
            self.lista_resultados.lift()
            for ced, nom in res:
                btn = ctk.CTkButton(self.lista_resultados, text=f"{ced} - {nom}", fg_color="transparent", 
                                    text_color="black", anchor="w", hover_color="#d5dbdb", 
                                    command=lambda c=ced: self.cargar_registro_desde_busqueda(c))
                btn.pack(fill="x", pady=1)
        else:
            self.lista_resultados.place_forget()

    def cargar_registro_desde_busqueda(self, parametro):
        self.lista_resultados.place_forget()
        if not parametro: return
        
        u = db.obtener_registro(parametro)
        if u:
            self.limpiar_formulario()
            self.entry_buscar.delete(0, 'end'); self.entry_buscar.insert(0, u[0])
            campos = ["cedula","nombre","telf","correo","fnac","dir"]
            for i, k in enumerate(campos): self.inputs[k].insert(0, u[i])
            self.inputs["ini"].insert(0, u[12]); self.inputs["fin"].insert(0, u[13])
            if len(u) > 14 and u[14]: self.txt_obs.insert("1.0", u[14])
            
            self.combos["uni"].set(u[7]); self.cargar_especialidades_por_uni(u[7])
            self.combos["esp"].set(u[8]); self.combos["cen"].set(u[11])
            self.cargar_guardias_por_centro(u[11]); self.combos["guardias"].set(u[6])
            self.combos["car"].set(u[9]); self.combos["mod"].set(u[10])
        else:
            messagebox.showinfo("Búsqueda", "No se encontraron resultados.")
    
    def procesar_texto_correo(self, event, entry):
        texto = entry.get()
        if texto != texto.lower():
           pos = entry.index("insert")
           entry.delete(0, "end")
           entry.insert(0, texto.lower())
           entry.icursor(pos)
    
        if "@" in texto and "." in texto:
           entry.configure(border_color="#27ae60")
        else:
           entry.configure(border_color="#e74c3c")

    def validar_fechas_tiempo_real(self, event, tipo_campo):
        """Valida cuando el usuario sale de la casilla de fecha."""
        texto = event.widget.get().strip()
    
        if not texto or texto in ["DD/MM/AAAA", "Inicio", "Fin"]:
           return

        try:
            time.strptime(texto, "%d/%m/%Y")
        
            f_ini = self.inputs["ini"].get().strip()
            f_fin = self.inputs["fin"].get().strip()
        
            if f_ini and f_fin and "/" in f_ini and "/" in f_fin:
                obj_ini = time.strptime(f_ini, "%d/%m/%Y")
                obj_fin = time.strptime(f_fin, "%d/%m/%Y")
            
                if obj_ini > obj_fin:
                    messagebox.showwarning("Rango de Fechas", 
                                     "Atención: La fecha de inicio no puede ser posterior a la de fin.")
                    if tipo_campo == "fin":
                        self.inputs["fin"].delete(0, 'end')

        except ValueError:
            messagebox.showerror("Fecha Inválida", 
                             f"El formato en el campo de fecha es incorrecto.\nUse: DD/MM/AAAA")
            self.after(100, lambda: event.widget.focus_set())

    def validar_formato_correo_visual(self, entry):
        correo = entry.get()
        if "@" in correo and "." in correo:
            entry.configure(border_color="#27ae60")
        else:
            entry.configure(border_color="#e74c3c")    

    def obtener_total_registros(self):
        return db.contar_todos_los_registros()

    def actualizar_contador_ui(self):
        nuevo_total = self.obtener_total_registros()
        if hasattr(self, 'btn_contador'):
            self.btn_contador.configure(text=f"📊 Total Registros: {nuevo_total}")

    def obtener_estadisticas_detalladas():
        conn = sqlite3.connect(db.DB_PATH)
        cursor = conn.cursor()
    
        cursor.execute("SELECT COUNT(*) FROM registros")
        total = cursor.fetchone()[0]
    
        cursor.execute("SELECT COUNT(DISTINCT cen) FROM registros")
        centros_ocupados = cursor.fetchone()[0]
    
        conn.close()
        return total, centros_ocupados        


    def verificar_cedula_existente(self, event=None):
        cedula = self.inputs["cedula"].get().strip()
        if not cedula: return
        
        nombre_existente = db.verificar_cedula(cedula)
        if nombre_existente:
            self.after(100, lambda: messagebox.showwarning(
                "Cédula Duplicada", f"La cédula {cedula} ya está registrada a nombre de {nombre_existente}."
            ))

    def bloquear_espacios(self, texto_nuevo):
        if " " in texto_nuevo:
            return False
        
        if texto_nuevo.count("@") > 1:
            return False
        
        return True
        
    def guardar_ui(self):
        d = {}
        for clave, valor in self.inputs.items():
            d[clave] = valor.get().strip()
            
        c = {}
        for clave, valor in self.combos.items():
            c[clave] = valor.get()
            
        obs = self.txt_obs.get("1.0", "end-1c").strip()
        
        for clave, valor in d.items():
            if valor == "":
                messagebox.showwarning("Atención", "No puede dejar ningún campo en blanco. Llénelos todos por favor.")
                return
                
        for clave, valor in c.items():
            if valor == "":
                messagebox.showwarning("Atención", "Debe seleccionar una opción en todas las listas.")
                return

        fechas = [d["fnac"], d["ini"], d["fin"]]
        for f in fechas:
            try:
                time.strptime(f, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Fecha incorrecta", "La fecha ingresada tiene fallas. Por favor corríjala usando el formato: DD/MM/AAAA")
                return
            
        obj_nac = time.strptime(d["fnac"], "%d/%m/%Y")
        if obj_nac > time.localtime():
            messagebox.showwarning("Atención", "La fecha de nacimiento no puede ser una fecha futura.")
            return

        obj_ini = time.strptime(d["ini"], "%d/%m/%Y")
        obj_fin = time.strptime(d["fin"], "%d/%m/%Y")

        if obj_ini > obj_fin:
            messagebox.showwarning("Error de Rango", "La fecha de inicio no puede ser posterior a la fecha de finalización.")
            return
            
        if "@" not in d["correo"] or "." not in d["correo"]:
            self.inputs["correo"].configure(border_color="#e74c3c", border_width=2)
            messagebox.showerror("Correo Inválido", "El formato del correo es incorrecto.")
            return
        else:
            self.inputs["correo"].configure(border_color="#abb2b9", border_width=1)
            
        if len(d["telf"]) < 10:
            messagebox.showerror("Teléfono Inválido", "El número de teléfono parece estar incompleto.")
            return
            
        try:
            nombre_existente = db.verificar_cedula(d["cedula"])
            
            if self.modo_actual == "nuevo":
                if nombre_existente:
                    messagebox.showerror("Error", f"La cédula {d['cedula']} ya está registrada.\nPara editarlo, use Búsqueda.")
                    return
                db.guardar_nuevo_usuario(d, c, obs)
                messagebox.showinfo("Éxito", "¡Registro creado exitosamente!")
                self.actualizar_contador_ui()

            else:
                if nombre_existente:
                    db.actualizar_registro(d, c, obs)
                    messagebox.showinfo("Actualizado", "Los cambios han sido guardados correctamente.")
                else:
                    if messagebox.askyesno("Nuevo Registro", "Esta cédula no existe. ¿Desea crear un nuevo registro?"):
                        db.guardar_nuevo_usuario(d, c, obs)
                        messagebox.showinfo("Éxito", "¡Registro creado exitosamente!")

        except Exception as e: 
            messagebox.showerror("Error de BD", f"Error: {str(e)}")

    def generar_word_ui(self):
        try:
            ced = self.inputs["cedula"].get().strip()
            centro_actual = self.combos["cen"].get()
            
            if not ced: 
                messagebox.showwarning("Atención", "Debe ingresar una cédula para generar el documento.")
                return

            datos_pantalla = {}
            for clave, valor in self.inputs.items():
                datos_pantalla[clave] = valor.get().strip()
                
            combos_pantalla = {}
            for clave, valor in self.combos.items():
                combos_pantalla[clave] = valor.get()
                
            obs_pantalla = self.txt_obs.get("1.0", "end-1c").strip()

            u = db.obtener_registro(ced)
            datos_guardados = False
            if u:
                match = (str(u[0]) == datos_pantalla["cedula"] and str(u[1]) == datos_pantalla["nombre"] and
                         str(u[11]) == combos_pantalla["cen"] and str(u[14] if u[14] else "") == obs_pantalla)
                if match: datos_guardados = True

            if not datos_guardados:
                if not messagebox.askyesno("Datos no Guardados", "¿Desea generar el Word con los datos de la pantalla de todos modos?"):
                    return

            responsable = db.obtener_responsable_centro(centro_actual)
            docs.generar_documento_word(datos_pantalla, combos_pantalla, obs_pantalla, responsable)
            
        except Exception as e: 
            messagebox.showerror("Error", f"No se pudo generar el Word: {e}")

    def limpiar_formulario(self):
        for key in self.inputs:
            self.inputs[key].delete(0, 'end')
            self.inputs[key].configure(border_color="#abb2b9", border_width=1)   
        for key in self.combos:
            self.combos[key].set("")
    
        if hasattr(self, 'txt_obs'):
            self.txt_obs.delete("1.0", "end")
        if hasattr(self, 'entry_buscar') and self.entry_buscar is not None:
            self.entry_buscar.delete(0, 'end')
        if hasattr(self, 'lista_resultados'):
            self.lista_resultados.place_forget()
    
        self.modo_actual = "nuevo"
        self.inputs["cedula"].configure(state="normal")
        
    def mostrar_ayuda(self):
        msj_actual = db.obtener_mensaje_ayuda()
        ventana_ayuda = ctk.CTkToplevel(self)
        ventana_ayuda.title("Centro de Ayuda")
        ventana_ayuda.geometry("550x400")
        ventana_ayuda.transient(self)
        ventana_ayuda.grab_set()
        ctk.CTkLabel(ventana_ayuda, text="Centro de ayuda:", font=("Segoe UI", 14, "bold")).pack(pady=(20, 10))
        caja_texto = ctk.CTkTextbox(ventana_ayuda, width=500, height=250, border_width=1, border_color="#abb2b9")
        caja_texto.pack(pady=10, padx=20)
        caja_texto.insert("1.0", msj_actual)

    def respaldar_bd_ui(self):
        import time
        from tkinter import filedialog
        
        fecha_str = time.strftime("%d_%m_%Y_%H%M")
        nombre_default = f"Respaldo_BD_{fecha_str}.db"
        
        ruta = filedialog.asksaveasfilename(
            defaultextension=".db",
            initialfile=nombre_default,
            title="Guardar Respaldo de Base de Datos",
            filetypes=[("Archivos de Base de Datos", "*.db"), ("Todos los archivos", "*.*")]
        )
        
        if ruta:
            exito = db.hacer_respaldo_bd(ruta)
            if exito:
                messagebox.showinfo("Respaldo Exitoso", f"La base de datos completa se ha guardado correctamente como una copia de seguridad en:\n{ruta}")
            else:
                messagebox.showerror("Error", "No se encontró el archivo original de la base de datos para copiar.")

    def eliminar_registro_ui(self):
        ced = self.inputs["cedula"].get()
        if ced and messagebox.askyesno("Confirmar", "¿Eliminar registro?"):
            db.eliminar_registro(ced)
            self.limpiar_formulario()

    def exportar_excel_ui(self):
        try:
            docs.exportar_excel_db()
        except Exception as e: 
            messagebox.showerror("Excel Error", str(e))

    def confirmar_salida(self): self.destroy()

if __name__ == "__main__":
    app = AppFinalPro()
    app.mainloop()
