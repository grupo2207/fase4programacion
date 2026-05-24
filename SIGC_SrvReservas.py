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

class ErrorValidacion(Exception): pass

# ==========================================
# 2. MODELO DE NEGOCIO (Backend)
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
            raise ErrorValidacion(f"El documento {num_doc} ya existe.")
        nuevo = Cliente(nombre, telefono, correo, tipo_doc, num_doc)
        self._clientes.append(nuevo)

    def registrar_servicio(self, nombre, costo):
        if not nombre or costo <= 0:
            raise ErrorValidacion("Datos de servicio inválidos.")
        self._servicios_catalogo[nombre] = costo

# ==========================================
# 3. INTERFAZ GRÁFICA (Dashboard)
# ==========================================
class AppDashboardFJ:
    def __init__(self, root, sistema):
        self.root = root
        self.sistema = sistema
        self.root.title("FJ TECHNOLOGY - Sistema Integral")
        self.root.geometry("1200://750")
        self.root.geometry("1250x750")
        self.root.configure(bg="#0B1426")
        
        # Colores
        self.c_bg_main = "#0B1426"
        self.c_bg_panel = "#112240"
        self.c_bg_sidebar = "#080F1E"
        self.c_accent = "#0267C1"
        self.c_text = "#CCD6F6"
        
        # Contenedores
        self.frames = {}
        self._crear_estructura()
        self.mostrar_frame("Inicio")

    def _crear_estructura(self):
        # SIDEBAR
        self.sidebar = tk.Frame(self.root, bg=self.c_bg_sidebar, width=250)
        self.sidebar.pack(side="left", fill="y")

        # LOGO (Uso de Pillow)
        try:
            img = Image.open("logo_fj.png")
            img = img.resize((180, 100), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            lbl_logo = tk.Label(self.sidebar, image=self.logo_img, bg=self.c_bg_sidebar)
            lbl_logo.pack(pady=20)
        except:
            tk.Label(self.sidebar, text="FJ TECHNOLOGY", fg=self.c_accent, bg=self.c_bg_sidebar, font=("Arial", 16, "bold")).pack(pady=40)

        # BOTONES MENU
        botones = [
            ("🏠 Inicio", "Inicio"),
            ("👥 Registro Clientes", "Registro"),
            ("📋 Lista de Clientes", "Lista"),
            ("🛠 Configurar Servicios", "ConfigServ"),
            ("🚪 Cerrar Sesión", "Exit")
        ]
        for txt, target in botones:
            btn = tk.Button(self.sidebar, text=txt, bg=self.c_bg_sidebar, fg=self.c_text, font=("Helvetica", 11),
                            bd=0, padx=20, pady=12, anchor="w", command=lambda t=target: self.mostrar_frame(t))
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.c_bg_panel))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.c_bg_sidebar))

        # CONTENEDOR DERECHO
        self.container = tk.Frame(self.root, bg=self.c_bg_main)
        self.container.pack(side="right", fill="both", expand=True)

        # INICIALIZAR SECCIONES
        self._init_frame_inicio()
        self._init_frame_registro()
        self._init_frame_lista()
        self._init_frame_config_serv()

    def mostrar_frame(self, target):
        if target == "Exit": self.root.quit()
        for f in self.frames.values(): f.pack_forget()
        self.frames[target].pack(fill="both", expand=True)
        if target == "Lista": self._actualizar_tabla_clientes()

    # --- SECCIÓN 1: INICIO (Liquidación) ---
    def _init_frame_inicio(self):
        f = tk.Frame(self.container, bg=self.c_bg_main)
        self.frames["Inicio"] = f
        
        tk.Label(f, text="MODULO DE LIQUIDACIÓN DE SERVICIOS", font=("Arial", 18, "bold"), bg=self.c_bg_main, fg="white").pack(pady=20)
        
        panel = tk.Frame(f, bg=self.c_bg_panel, padx=30, pady=30)
        panel.pack(pady=10)

        tk.Label(panel, text="Documento del Cliente:", bg=self.c_bg_panel, fg=self.c_text).grid(row=0, column=0, sticky="w")
        self.ent_liq_doc = tk.Entry(panel, width=20)
        self.ent_liq_doc.grid(row=0, column=1, padx=10)
        
        self.lbl_cli_nom = tk.Label(panel, text="No vinculado", fg="#00F5D4", bg=self.c_bg_panel, font=("Arial", 10, "italic"))
        self.lbl_cli_nom.grid(row=1, column=0, columnspan=2, pady=10)

        tk.Button(panel, text="Vincular", command=self._vincular_cliente_liq).grid(row=0, column=2)

        tk.Label(panel, text="Seleccione Servicio:", bg=self.c_bg_panel, fg=self.c_text).grid(row=2, column=0, sticky="w", pady=10)
        self.cb_servs = ttk.Combobox(panel, values=list(self.sistema._servicios_catalogo.keys()), width=40, state="readonly")
        self.cb_servs.grid(row=2, column=1, columnspan=2)

        self.list_liq = tk.Listbox(panel, width=60, height=10, bg="#080F1E", fg="white", bd=0)
        self.list_liq.grid(row=3, column=0, columnspan=3, pady=20)

        self.lbl_total = tk.Label(panel, text="TOTAL: $0", font=("Arial", 16, "bold"), bg=self.c_bg_panel, fg="#00F5D4")
        self.lbl_total.grid(row=4, column=2)

        tk.Button(panel, text="Agregar Servicio", bg=self.c_accent, fg="white", command=self._agregar_serv_liq).grid(row=4, column=0)

    # --- SECCIÓN 2: REGISTRO ---
    def _init_frame_registro(self):
        f = tk.Frame(self.container, bg=self.c_bg_main)
        self.frames["Registro"] = f
        tk.Label(f, text="REGISTRO DE NUEVOS CLIENTES", font=("Arial", 18, "bold"), bg=self.c_bg_main, fg="white").pack(pady=20)
        
        panel = tk.Frame(f, bg=self.c_bg_panel, padx=40, pady=40)
        panel.pack()

        campos = ["Nombre Completo", "Teléfono", "Correo", "Tipo Doc (CC/TI/CE/PSP)", "Número Documento"]
        self.ents_reg = []
        for c in campos:
            tk.Label(panel, text=c, bg=self.c_bg_panel, fg=self.c_text).pack(anchor="w")
            e = tk.Entry(panel, width=50)
            e.pack(pady=5)
            self.ents_reg.append(e)
        
        tk.Button(panel, text="GUARDAR CLIENTE", bg=self.c_accent, fg="white", font=("Arial", 10, "bold"),
                  command=self._guardar_cliente).pack(pady=20, fill="x")

    # --- SECCIÓN 3: LISTA DE CLIENTES (Nueva solicitada) ---
    def _init_frame_lista(self):
        f = tk.Frame(self.container, bg=self.c_bg_main)
        self.frames["Lista"] = f
        tk.Label(f, text="BASE DE DATOS DE CLIENTES", font=("Arial", 18, "bold"), bg=self.c_bg_main, fg="white").pack(pady=20)
        
        # Tabla
        style = ttk.Style()
        style.configure("Treeview", background="#112240", foreground="white", fieldbackground="#112240", rowheight=30)
        style.map("Treeview", background=[('selected', '#0267C1')])

        columnas = ("nombre", "doc", "tipo", "tel")
        self.tabla = ttk.Treeview(f, columns=columnas, show="headings", height=15)
        self.tabla.heading("nombre", text="Nombre Completo")
        self.tabla.heading("doc", text="No. Documento")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.heading("tel", text="Celular")
        self.tabla.pack(padx=30, pady=10, fill="both")
        
        tk.Label(f, text="* Seleccione un cliente para ver su No. de Documento y usarlo en liquidación", 
                 bg=self.c_bg_main, fg=self.c_text, font=("Arial", 9, "italic")).pack()

    # --- SECCIÓN 4: CONFIGURAR SERVICIOS (Nueva solicitada) ---
    def _init_frame_config_serv(self):
        f = tk.Frame(self.container, bg=self.c_bg_main)
        self.frames["ConfigServ"] = f
        tk.Label(f, text="GESTIÓN DE SERVICIOS Y PRECIOS", font=("Arial", 18, "bold"), bg=self.c_bg_main, fg="white").pack(pady=20)
        
        panel = tk.Frame(f, bg=self.c_bg_panel, padx=30, pady=30)
        panel.pack(pady=10)

        tk.Label(panel, text="Nombre del Servicio:", bg=self.c_bg_panel, fg=self.c_text).pack(anchor="w")
        self.ent_serv_nom = tk.Entry(panel, width=40)
        self.ent_serv_nom.pack(pady=5)

        tk.Label(panel, text="Costo del Servicio ($):", bg=self.c_bg_panel, fg=self.c_text).pack(anchor="w")
        self.ent_serv_costo = tk.Entry(panel, width=40)
        self.ent_serv_costo.pack(pady=5)

        tk.Button(panel, text="AÑADIR AL CATÁLOGO", bg="#00A896", fg="white", font=("Arial", 10, "bold"),
                  command=self._crear_nuevo_servicio).pack(pady=20, fill="x")

    # --- LOGICA ---
    def _vincular_cliente_liq(self):
        doc = self.ent_liq_doc.get()
        cli = next((c for c in self.sistema._clientes if c.num_doc == doc), None)
        if cli:
            self.lbl_cli_nom.config(text=f"VINCULADO: {cli.nombre}")
            self.cliente_actual = cli
        else:
            messagebox.showerror("Error", "Cliente no encontrado.")

    def _agregar_serv_liq(self):
        s_nom = self.cb_servs.get()
        if s_nom:
            precio = self.sistema._servicios_catalogo[s_nom]
            self.list_liq.insert(tk.END, f"{s_nom} --- ${precio:,.0f}")
            # Calculo total simple
            total = sum(self.sistema._servicios_catalogo[line.split(" --- ")[0]] for line in self.list_liq.get(0, tk.END))
            self.lbl_total.config(text=f"TOTAL: ${total:,.0f}")

    def _guardar_cliente(self):
        try:
            datos = [e.get() for e in self.ents_reg]
            self.sistema.registrar_cliente(datos[0], datos[1], datos[2], datos[3], datos[4])
            messagebox.showinfo("Éxito", "Cliente guardado.")
            for e in self.ents_reg: e.delete(0, tk.END)
        except Exception as e: messagebox.showerror("Error", str(e))

    def _actualizar_tabla_clientes(self):
        for i in self.tabla.get_children(): self.tabla.delete(i)
        for c in self.sistema._clientes:
            self.tabla.insert("", tk.END, values=(c.nombre, c.num_doc, c.tipo_doc, c.telefono))

    def _crear_nuevo_servicio(self):
        try:
            nom = self.ent_serv_nom.get()
            costo = float(self.ent_serv_costo.get())
            self.sistema.registrar_servicio(nom, costo)
            self.cb_servs['values'] = list(self.sistema._servicios_catalogo.keys())
            messagebox.showinfo("Éxito", f"Servicio '{nom}' añadido.")
            self.ent_serv_nom.delete(0, tk.END); self.ent_serv_costo.delete(0, tk.END)
        except: messagebox.showerror("Error", "Verifique el nombre y que el costo sea un número.")

if __name__ == "__main__":
    sistema = SistemaFJ()
    root = tk.Tk()
    app = AppDashboardFJ(root, sistema)
    root.mainloop()