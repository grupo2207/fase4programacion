import abc
import logging
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk  # Requiere: pip install Pillow

# ==========================================
# 1. LOGGING Y EXCEPCIONES
# ==========================================
logging.basicConfig(
    filename='fj_errores.log', level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8'
)

class FJErrorBase(Exception): pass
class ErrorValidacion(FJErrorBase): pass

# ==========================================
# 2. MODELO DE NEGOCIO (Backend con OOP)
# ==========================================
class Cliente:
    def __init__(self, nombre, telefono, correo, tipo_doc, num_doc):
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.tipo_doc = tipo_doc
        self.num_doc = num_doc

class SistemaFJ:
    def __init__(self):
        self._clientes = []
        self._servicios_catalogo = {
            "Reserva de salon principal por dia": 550000,
            "Reserva de salon Pasoancho por dia": 350000,
            "Alquiler de portatil gamma media": 25000,
            "Alquiler de portatil gamma alta": 35000,
            "Asesoria especializada": 85000
        }
        self._precargar_datos()

    def _precargar_datos(self):
        self.registrar_cliente("Alejandro Escobar Higuera", "3195802896", "alejandro.non2207@gmail.com", "CC", "94539614")
        self.registrar_cliente("Andres Martinez Martinez", "3195801358", "amartinezm@gmail.com", "CC", "11130258963")

    def registrar_cliente(self, nombre, telefono, correo, tipo_doc, num_doc):
        if any(c.num_doc == num_doc for c in self._clientes):
            raise ErrorValidacion(f"El documento {num_doc} ya está registrado.")
        nuevo = Cliente(nombre, telefono, correo, tipo_doc, num_doc)
        self._clientes.append(nuevo)

    def buscar_cliente(self, num_doc):
        for c in self._clientes:
            if c.num_doc == str(num_doc).strip(): return c
        return None

# ==========================================
# 3. INTERFAZ GRÁFICA (Dashboard Principal)
# ==========================================
class AppDashboardFJ:
    def __init__(self, root, sistema):
        self.root = root
        self.sistema = sistema
        self.root.title("FJ Technology - Sistema Integral")
        self.root.geometry("1200x750")
        self.root.configure(bg="#0B1426")
        
        # Colores de la imagen
        self.c_bg_main = "#0B1426"
        self.c_bg_panel = "#112240"
        self.c_bg_sidebar = "#080F1E"
        self.c_accent_blue = "#0267C1"
        self.c_accent_green = "#00A896"
        self.c_text = "#CCD6F6"
        
        self._construir_interfaz()

    def _construir_interfaz(self):
        # 1. SIDEBAR
        sidebar = tk.Frame(self.root, bg=self.c_bg_sidebar, width=220)
        sidebar.pack(side="left", fill="y")

        # Cargar Logo
        try:
            img_raw = Image.open("logo_fj.png")
            img_res = img_raw.resize((160, 90), Image.LANCZOS)
            self.img_logo = ImageTk.PhotoImage(img_res)
            tk.Label(sidebar, image=self.img_logo, bg=self.c_bg_sidebar).pack(pady=20)
        except:
            tk.Label(sidebar, text="FJ TECHNOLOGY", fg=self.c_accent_blue, bg=self.c_bg_sidebar, font=("Arial", 14, "bold")).pack(pady=40)

        for btn_txt in ["Inicio", "Clientes", "Servicios", "Reservas", "Reportes"]:
            bg_c = self.c_bg_panel if btn_txt == "Inicio" else self.c_bg_sidebar
            tk.Button(sidebar, text=f"  {btn_txt}", bg=bg_c, fg="white", font=("Arial", 11), 
                      bd=0, anchor="w", padx=20, pady=12).pack(fill="x")

        # 2. AREA CENTRAL
        self.main_content = tk.Frame(self.root, bg=self.c_bg_main)
        self.main_content.pack(side="right", fill="both", expand=True, padx=20)

        # Header
        header = tk.Frame(self.main_content, bg=self.c_bg_main)
        header.pack(fill="x", pady=20)
        tk.Label(header, text="SISTEMA INTEGRAL DE", font=("Arial", 10), bg=self.c_bg_main, fg=self.c_accent_blue).pack()
        tk.Label(header, text="Gestión de Clientes, Servicios y Reservas", font=("Arial", 20, "bold"), bg=self.c_bg_main, fg="white").pack()

        # CONTENEDOR DE DOS COLUMNAS (Perspectiva Perfecta)
        contenedor_columnas = tk.Frame(self.main_content, bg=self.c_bg_main)
        contenedor_columnas.pack(fill="both", expand=True)

        # --- COLUMNA IZQUIERDA: CLIENTES ---
        col_izq = tk.Frame(contenedor_columnas, bg=self.c_bg_panel, bd=1, relief="flat")
        col_izq.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(col_izq, text="👥 CLIENTES", font=("Arial", 12, "bold"), bg=self.c_bg_panel, fg="white").pack(pady=10, anchor="w", padx=15)
        
        # Sub-modulo Consulta
        frame_cons = tk.Frame(col_izq, bg=self.c_bg_panel)
        frame_cons.pack(fill="x", padx=15)
        tk.Label(frame_cons, text="No. de Documento (Consultar):", bg=self.c_bg_panel, fg="#8892B0").grid(row=0, column=0, sticky="w")
        self.ent_busc_doc = tk.Entry(frame_cons, width=20, bg="#0B1426", fg="white", insertbackground="white")
        self.ent_busc_doc.grid(row=1, column=0, pady=5)
        tk.Button(frame_cons, text="🔍 Consultar", bg=self.c_bg_sidebar, fg="white", command=self.evento_consultar).grid(row=1, column=1, padx=10)

        # Sub-modulo Registro
        tk.Frame(col_izq, height=1, bg="#2A3B5C").pack(fill="x", padx=15, pady=15)
        tk.Label(col_izq, text="📝 Registro Clientes", font=("Arial", 11, "bold"), bg=self.c_bg_panel, fg="white").pack(anchor="w", padx=15)
        
        self.campos_reg = {}
        for lab in ["Nombre completo", "Teléfono celular", "Correo electrónico", "No. de Documento"]:
            tk.Label(col_izq, text=lab, bg=self.c_bg_panel, fg="#8892B0").pack(anchor="w", padx=15, pady=(5,0))
            e = tk.Entry(col_izq, width=45, bg="#0B1426", fg="white", insertbackground="white")
            e.pack(padx=15, pady=2)
            self.campos_reg[lab] = e

        tk.Button(col_izq, text="💾 GUARDAR CLIENTE", bg=self.c_accent_blue, fg="white", font=("Arial", 10, "bold"), 
                  command=self.evento_guardar, bd=0).pack(fill="x", padx=15, pady=20, ipady=8)

        # --- COLUMNA DERECHA: LIQUIDACIÓN ---
        col_der = tk.Frame(contenedor_columnas, bg=self.c_bg_panel, bd=1, relief="flat")
        col_der.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(col_der, text="💼 SERVICIOS", font=("Arial", 12, "bold"), bg=self.c_bg_panel, fg="white").pack(pady=10, anchor="w", padx=15)
        
        tk.Label(col_der, text="Vincular Cliente (Documento):", bg=self.c_bg_panel, fg="#8892B0").pack(anchor="w", padx=15)
        frame_vinc = tk.Frame(col_der, bg=self.c_bg_panel)
        frame_vinc.pack(fill="x", padx=15)
        self.ent_vinc_doc = tk.Entry(frame_vinc, width=20, bg="#0B1426", fg="white")
        self.ent_vinc_doc.pack(side="left", pady=5)
        tk.Button(frame_vinc, text="Vincular", command=self.evento_vincular).pack(side="left", padx=10)
        
        self.lbl_vinc_nom = tk.Label(col_der, text="Esperando cliente...", fg=self.c_accent_green, bg=self.c_bg_panel, font=("Arial", 9, "italic"))
        self.lbl_vinc_nom.pack(anchor="w", padx=15)

        tk.Label(col_der, text="Servicio:", bg=self.c_bg_panel, fg="#8892B0").pack(anchor="w", padx=15, pady=(15,0))
        self.cb_servs = ttk.Combobox(col_der, values=list(self.sistema._servicios_catalogo.keys()), state="readonly", width=42)
        self.cb_servs.pack(padx=15, pady=5)

        tk.Button(col_der, text="➕ Agregar Servicio", bg=self.c_bg_sidebar, fg="white", command=self.evento_agregar_serv).pack(pady=10)

        self.list_items = tk.Listbox(col_der, bg="#080F1E", fg="white", bd=0, height=8)
        self.list_items.pack(fill="x", padx=15, pady=10)

        self.lbl_total = tk.Label(col_der, text="TOTAL: $ 0", font=("Arial", 16, "bold"), bg=self.c_bg_panel, fg=self.c_accent_green)
        self.lbl_total.pack(anchor="e", padx=15)

        # --- FOOTER INTERACTIVO ---
        footer = tk.Frame(self.main_content, bg=self.c_bg_sidebar, height=50)
        footer.pack(fill="x", side="bottom", pady=10)

        # Icono/Label Clientes (Clicable)
        self.lbl_stat_cli = tk.Label(footer, text=f"👤 Clientes registrados: {len(self.sistema._clientes)}", 
                                     bg=self.c_bg_sidebar, fg="#8892B0", cursor="hand2")
        self.lbl_stat_cli.pack(side="left", padx=20)
        self.lbl_stat_cli.bind("<Button-1>", lambda e: self.abrir_lista_clientes())

        # Icono Tuerca (Clicable)
        self.lbl_tuerca = tk.Label(footer, text="⚙️ Configurar Servicios", 
                                   bg=self.c_bg_sidebar, fg="#8892B0", cursor="hand2")
        self.lbl_tuerca.pack(side="right", padx=20)
        self.lbl_tuerca.bind("<Button-1>", lambda e: self.abrir_config_servicios())

    # ==========================================
    # MODULOS EMERGENTES (Solicitados)
    # ==========================================
    def abrir_lista_clientes(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Base de Datos de Clientes")
        ventana.geometry("600x400")
        ventana.configure(bg=self.c_bg_panel)
        
        tk.Label(ventana, text="LISTA DE CLIENTES REGISTRADOS", bg=self.c_bg_panel, fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        
        tabla = ttk.Treeview(ventana, columns=("Nombre", "Doc"), show="headings")
        tabla.heading("Nombre", text="Nombre del Cliente")
        tabla.heading("Doc", text="Número de Documento")
        tabla.pack(fill="both", expand=True, padx=20, pady=10)

        for c in self.sistema._clientes:
            tabla.insert("", tk.END, values=(c.nombre, c.num_doc))

    def abrir_config_servicios(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Configuración de Servicios")
        ventana.geometry("400x300")
        ventana.configure(bg=self.c_bg_panel)

        tk.Label(ventana, text="CREAR NUEVO SERVICIO", bg=self.c_bg_panel, fg="white", font=("Arial", 11, "bold")).pack(pady=20)
        
        tk.Label(ventana, text="Nombre del Servicio:", bg=self.c_bg_panel, fg="white").pack()
        e_nom = tk.Entry(ventana, width=30)
        e_nom.pack(pady=5)

        tk.Label(ventana, text="Costo ($):", bg=self.c_bg_panel, fg="white").pack()
        e_cos = tk.Entry(ventana, width=30)
        e_cos.pack(pady=5)

        def guardar_s():
            try:
                nom = e_nom.get()
                precio = float(e_cos.get())
                self.sistema._servicios_catalogo[nom] = precio
                self.cb_servs['values'] = list(self.sistema._servicios_catalogo.keys())
                messagebox.showinfo("Éxito", "Servicio añadido al catálogo.")
                ventana.destroy()
            except: messagebox.showerror("Error", "Costo debe ser numérico.")

        tk.Button(ventana, text="Añadir Servicio", bg=self.c_accent_green, fg="white", command=guardar_s).pack(pady=20)

    # ==========================================
    # LÓGICA DE PROCESOS
    # ==========================================
    def evento_consultar(self):
        doc = self.ent_busc_doc.get()
        cli = self.sistema.buscar_cliente(doc)
        if cli:
            self.campos_reg["Nombre completo"].delete(0, tk.END)
            self.campos_reg["Nombre completo"].insert(0, cli.nombre)
            self.campos_reg["Teléfono celular"].delete(0, tk.END)
            self.campos_reg["Teléfono celular"].insert(0, cli.telefono)
            self.campos_reg["No. de Documento"].delete(0, tk.END)
            self.campos_reg["No. de Documento"].insert(0, cli.num_doc)
            messagebox.showinfo("Consulta", "Cliente cargado en formulario.")
        else: messagebox.showwarning("Atención", "Cliente no registrado.")

    def evento_guardar(self):
        try:
            nombre = self.campos_reg["Nombre completo"].get()
            tel = self.campos_reg["Teléfono celular"].get()
            mail = self.campos_reg["Correo electrónico"].get()
            doc = self.campos_reg["No. de Documento"].get()
            
            self.sistema.registrar_cliente(nombre, tel, mail, "CC", doc)
            self.lbl_stat_cli.config(text=f"👤 Clientes registrados: {len(self.sistema._clientes)}")
            messagebox.showinfo("Éxito", "Cliente guardado.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def evento_vincular(self):
        doc = self.ent_vinc_doc.get()
        cli = self.sistema.buscar_cliente(doc)
        if cli:
            self.lbl_vinc_nom.config(text=f"VINCULADO: {cli.nombre}")
            self.list_items.delete(0, tk.END)
            self.total_actual = 0
            self.lbl_total.config(text="TOTAL: $ 0")
        else: messagebox.showerror("Error", "No existe ese cliente.")

    def evento_agregar_serv(self):
        s = self.cb_servs.get()
        if s:
            precio = self.sistema._servicios_catalogo[s]
            self.list_items.insert(tk.END, f"{s} - ${precio:,.0f}")
            total = sum(self.sistema._servicios_catalogo[line.split(" - ")[0]] for line in self.list_items.get(0, tk.END))
            self.lbl_total.config(text=f"TOTAL: $ {total:,.0f}")

# ==========================================
# 4. EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    motor = SistemaFJ()
    root = tk.Tk()
    app = AppDashboardFJ(root, motor)
    root.mainloop()