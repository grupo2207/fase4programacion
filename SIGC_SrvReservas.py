import abc
import logging
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# 1. CONFIGURACIÓN DEL LOGGING Y EXCEPCIONES
# ==========================================
logging.basicConfig(
    filename='fj_errores.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

class FJErrorBase(Exception): pass
class ErrorValidacion(FJErrorBase): pass

# ==========================================
# 2. MODELO DE NEGOCIO (Backend)
# ==========================================
class Cliente:
    TIPOS_DOC_PERMITIDOS = ['CC', 'TI', 'CE', 'PSP']

    def __init__(self, nombre, telefono, correo, tipo_doc, num_doc):
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.tipo_doc = tipo_doc
        self.num_doc = num_doc

    @property
    def nombre(self): return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor_limpio = str(valor).strip()
        if not valor_limpio:
            raise ErrorValidacion("El nombre no puede estar vacío.")
        self.__nombre = valor_limpio

    @property
    def telefono(self): return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor_str = str(valor).strip()
        if not valor_str.isdigit():
            raise ErrorValidacion("El teléfono solo debe contener números.")
        self.__telefono = valor_str

    @property
    def tipo_doc(self): return self.__tipo_doc

    @tipo_doc.setter
    def tipo_doc(self, valor):
        valor_upper = str(valor).strip().upper()
        if valor_upper not in self.TIPOS_DOC_PERMITIDOS:
            raise ErrorValidacion(f"Tipo de documento '{valor}' no válido.")
        self.__tipo_doc = valor_upper

    @property
    def num_doc(self): return self.__num_doc

    @num_doc.setter
    def num_doc(self, valor):
        valor_str = str(valor).strip()
        if not valor_str.isdigit():
            raise ErrorValidacion("El número de documento es inválido. Solo números.")
        self.__num_doc = valor_str

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
        # Precarga de los dos clientes solicitados
        self.registrar_cliente("Alejandro Escobar Higuera", "3195802896", "alejandro.non2207@gmail.com", "CC", "94539614")
        self.registrar_cliente("Andres Martinez Martinez", "3195801358", "amartinezm@gmail.com", "CC", "11130258963")

    def registrar_cliente(self, nombre, telefono, correo, tipo_doc, num_doc):
        if self.buscar_cliente(num_doc):
            raise ErrorValidacion(f"El documento {num_doc} ya está registrado en el sistema.")
        try:
            nuevo_cliente = Cliente(nombre, telefono, correo, tipo_doc, num_doc)
        except ErrorValidacion as e:
            logging.error(f"Error de validación al crear cliente: {e}")
            raise e
        else:
            self._clientes.append(nuevo_cliente)
            return nuevo_cliente

    def buscar_cliente(self, num_doc):
        for cliente in self._clientes:
            if cliente.num_doc == str(num_doc).strip():
                return cliente
        return None

    def obtener_total_clientes(self):
        return len(self._clientes)
    
    def obtener_catalogo_servicios(self):
        return list(self._servicios_catalogo.keys())
    
    def obtener_precio_servicio(self, nombre_servicio):
        return self._servicios_catalogo.get(nombre_servicio, 0)

# ==========================================
# 3. INTERFAZ GRÁFICA TIPO DASHBOARD (Frontend)
# ==========================================
class AppDashboardFJ:
    def __init__(self, root, sistema):
        self.root = root
        self.sistema = sistema
        self.root.title("FJ Technology - Sistema Integral")
        self.root.geometry("1100x700")
        self.root.configure(bg="#0B1426") # Fondo oscuro principal
        
        # Paleta de colores basada en tu imagen
        self.c_bg_main = "#0B1426"
        self.c_bg_panel = "#112240"
        self.c_bg_sidebar = "#080F1E"
        self.c_text_main = "#CCD6F6"
        self.c_text_muted = "#8892B0"
        self.c_accent_blue = "#0267C1"
        self.c_accent_green = "#00A896"
        
        # Variables para la liquidación
        self.cliente_actual_liquidacion = None
        self.total_liquidacion = 0
        
        self._construir_interfaz()

    def _construir_interfaz(self):
        # Contenedor Principal (Grid: Sidebar a la izq, Contenido a la der)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # 1. SIDEBAR (Menú lateral)
        sidebar = tk.Frame(self.root, bg=self.c_bg_sidebar, width=200)
        sidebar.grid(row=0, column=0, sticky="ns")
        
        lbl_logo = tk.Label(sidebar, text="FJ\nTECHNOLOGY", font=("Helvetica", 16, "bold"), 
                            bg=self.c_bg_sidebar, fg=self.c_accent_blue, pady=30)
        lbl_logo.pack()

        menus = ["Inicio", "Clientes", "Servicios", "Reservas", "Reportes", "Configuración"]
        for menu in menus:
            bg_color = self.c_bg_panel if menu == "Inicio" else self.c_bg_sidebar
            btn = tk.Button(sidebar, text=f"  {menu}", font=("Helvetica", 11), bg=bg_color, fg=self.c_text_main, 
                            bd=0, anchor="w", padx=20, pady=10, activebackground=self.c_accent_blue)
            btn.pack(fill="x", pady=2)

        # 2. CONTENEDOR PRINCIPAL DERECHO
        main_frame = tk.Frame(self.root, bg=self.c_bg_main)
        main_frame.grid(row=0, column=1, sticky="nsew")
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # --- HEADER ---
        header = tk.Frame(main_frame, bg=self.c_bg_main, pady=20)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        lbl_title_sub = tk.Label(header, text="SISTEMA INTEGRAL DE", font=("Helvetica", 12), bg=self.c_bg_main, fg=self.c_accent_blue)
        lbl_title_sub.pack()
        lbl_title_main = tk.Label(header, text="Gestión de Clientes, Servicios y Reservas", font=("Helvetica", 20, "bold"), bg=self.c_bg_main, fg="white")
        lbl_title_main.pack()

        # --- PANEL IZQUIERDO: CLIENTES ---
        panel_clientes = tk.Frame(main_frame, bg=self.c_bg_panel, bd=1, relief="ridge")
        panel_clientes.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)
        
        tk.Label(panel_clientes, text="👥 CLIENTES - Gestión de información", font=("Helvetica", 12, "bold"), 
                 bg=self.c_bg_panel, fg=self.c_text_main).pack(pady=10, anchor="w", padx=15)

        # Sub-panel Consulta
        frame_consulta = tk.Frame(panel_clientes, bg=self.c_bg_panel)
        frame_consulta.pack(fill="x", padx=15, pady=5)
        
        tk.Label(frame_consulta, text="Tipo de Documento:", bg=self.c_bg_panel, fg=self.c_text_muted).grid(row=0, column=0, sticky="w")
        self.combo_buscar_tipo = ttk.Combobox(frame_consulta, values=Cliente.TIPOS_DOC_PERMITIDOS, state="readonly", width=15)
        self.combo_buscar_tipo.grid(row=1, column=0, sticky="w", pady=5)
        self.combo_buscar_tipo.set("CC")
        
        tk.Label(frame_consulta, text="No. de Documento (Consultar):", bg=self.c_bg_panel, fg=self.c_text_muted).grid(row=0, column=1, sticky="w", padx=10)
        self.entry_buscar_doc = tk.Entry(frame_consulta, width=20)
        self.entry_buscar_doc.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        btn_consultar = tk.Button(frame_consulta, text="🔍 Consultar", bg=self.c_bg_sidebar, fg="white", bd=1, 
                                  command=self.evento_consultar)
        btn_consultar.grid(row=1, column=2, padx=5)

        tk.Frame(panel_clientes, height=1, bg="#2A3B5C").pack(fill="x", padx=15, pady=15) # Separador

        # Sub-panel Registro
        frame_registro = tk.Frame(panel_clientes, bg=self.c_bg_panel)
        frame_registro.pack(fill="both", expand=True, padx=15)
        
        # Campos de registro
        self.entradas_registro = {}
        campos = [
            ("Nombre completo:", "nombre"),
            ("Teléfono celular:", "telefono"),
            ("Correo electrónico:", "correo")
        ]
        
        for i, (label_text, key) in enumerate(campos):
            tk.Label(frame_registro, text=label_text, bg=self.c_bg_panel, fg=self.c_text_muted).pack(anchor="w")
            ent = tk.Entry(frame_registro, width=45)
            ent.pack(anchor="w", pady=(0, 10))
            self.entradas_registro[key] = ent

        tk.Label(frame_registro, text="Tipo de Documento:", bg=self.c_bg_panel, fg=self.c_text_muted).pack(anchor="w")
        self.entradas_registro["tipo_doc"] = ttk.Combobox(frame_registro, values=Cliente.TIPOS_DOC_PERMITIDOS, state="readonly", width=42)
        self.entradas_registro["tipo_doc"].pack(anchor="w", pady=(0, 10))
        
        tk.Label(frame_registro, text="No. de Documento:", bg=self.c_bg_panel, fg=self.c_text_muted).pack(anchor="w")
        self.entradas_registro["num_doc"] = tk.Entry(frame_registro, width=45)
        self.entradas_registro["num_doc"].pack(anchor="w", pady=(0, 15))

        btn_guardar = tk.Button(frame_registro, text="💾 GUARDAR CLIENTE", bg=self.c_accent_blue, fg="white", 
                                font=("Helvetica", 10, "bold"), bd=0, command=self.evento_guardar_cliente)
        btn_guardar.pack(fill="x", pady=10, ipady=5)


        # --- PANEL DERECHO: SERVICIOS Y LIQUIDACIÓN ---
        panel_servicios = tk.Frame(main_frame, bg=self.c_bg_panel, bd=1, relief="ridge")
        panel_servicios.grid(row=1, column=1, sticky="nsew", padx=15, pady=10)

        tk.Label(panel_servicios, text="💼 SERVICIOS - Módulo de Liquidación", font=("Helvetica", 12, "bold"), 
                 bg=self.c_bg_panel, fg=self.c_text_main).pack(pady=10, anchor="w", padx=15)

        # Buscar cliente para liquidar
        frame_liq_cliente = tk.Frame(panel_servicios, bg=self.c_bg_panel)
        frame_liq_cliente.pack(fill="x", padx=15, pady=5)
        
        tk.Label(frame_liq_cliente, text="Documento del Cliente:", bg=self.c_bg_panel, fg=self.c_text_muted).grid(row=0, column=0, sticky="w")
        self.entry_liq_doc = tk.Entry(frame_liq_cliente, width=15)
        self.entry_liq_doc.grid(row=0, column=1, padx=10)
        btn_liq_buscar = tk.Button(frame_liq_cliente, text="Vincular Cliente", bg=self.c_bg_sidebar, fg="white", bd=1, command=self.evento_buscar_liq)
        btn_liq_buscar.grid(row=0, column=2)
        
        self.lbl_liq_nombre = tk.Label(panel_servicios, text="Cliente no seleccionado", bg=self.c_bg_panel, fg=self.c_accent_green, font=("Helvetica", 10, "italic"))
        self.lbl_liq_nombre.pack(anchor="w", padx=15, pady=5)

        tk.Frame(panel_servicios, height=1, bg="#2A3B5C").pack(fill="x", padx=15, pady=10) # Separador

        # Seleccionar servicio
        tk.Label(panel_servicios, text="Servicios disponibles:", bg=self.c_bg_panel, fg=self.c_text_muted).pack(anchor="w", padx=15)
        self.combo_servicios = ttk.Combobox(panel_servicios, values=self.sistema.obtener_catalogo_servicios(), state="readonly", width=45)
        self.combo_servicios.pack(anchor="w", padx=15, pady=5)
        
        frame_cant = tk.Frame(panel_servicios, bg=self.c_bg_panel)
        frame_cant.pack(fill="x", padx=15, pady=5)
        tk.Label(frame_cant, text="Cantidad / Días:", bg=self.c_bg_panel, fg=self.c_text_muted).pack(side="left")
        self.entry_cantidad = tk.Entry(frame_cant, width=10)
        self.entry_cantidad.pack(side="left", padx=10)
        self.entry_cantidad.insert(0, "1")
        
        btn_add_servicio = tk.Button(frame_cant, text="➕ Agregar", bg=self.c_bg_sidebar, fg="white", bd=1, command=self.evento_agregar_servicio)
        btn_add_servicio.pack(side="left", padx=10)

        # Lista de liquidación (Carrito)
        self.lista_liquidacion = tk.Listbox(panel_servicios, bg="#080F1E", fg="white", bd=0, height=8, font=("Courier", 9))
        self.lista_liquidacion.pack(fill="both", expand=True, padx=15, pady=10)

        # Total y Botón Final
        self.lbl_total = tk.Label(panel_servicios, text="TOTAL: $ 0", font=("Helvetica", 16, "bold"), bg=self.c_bg_panel, fg=self.c_accent_green)
        self.lbl_total.pack(anchor="e", padx=15)
        
        btn_liquidar = tk.Button(panel_servicios, text="✓ GENERAR LIQUIDACIÓN", bg=self.c_accent_green, fg="white", 
                                font=("Helvetica", 10, "bold"), bd=0, command=self.evento_facturar)
        btn_liquidar.pack(fill="x", padx=15, pady=10, ipady=5)


        # --- FOOTER (Barra de estado inferior) ---
        footer = tk.Frame(main_frame, bg=self.c_bg_sidebar, height=40)
        footer.grid(row=2, column=0, columnspan=2, sticky="ew", padx=15, pady=10)
        footer.grid_propagate(False)
        
        self.lbl_count_clientes = tk.Label(footer, text=f"👥 Clientes registrados: {self.sistema.obtener_total_clientes()}", 
                                           bg=self.c_bg_sidebar, fg=self.c_text_muted)
        self.lbl_count_clientes.pack(side="left", padx=20, pady=10)
        
        tk.Label(footer, text="📋 Servicios activos: 5", bg=self.c_bg_sidebar, fg=self.c_text_muted).pack(side="left", padx=20, pady=10)
        tk.Label(footer, text="🟢 Sistema Operativo", bg=self.c_bg_sidebar, fg=self.c_accent_green).pack(side="right", padx=20, pady=10)

    # ==========================================
    # LOGICA DE LA INTERFAZ
    # ==========================================
    def evento_consultar(self):
        doc = self.entry_buscar_doc.get().strip()
        if not doc:
            messagebox.showwarning("Atención", "Ingrese el número de documento a consultar.")
            return
            
        cliente = self.sistema.buscar_cliente(doc)
        if cliente:
            # Llenar el formulario de registro con los datos encontrados
            for ent in self.entradas_registro.values():
                if isinstance(ent, tk.Entry):
                    ent.delete(0, tk.END)
            self.entradas_registro["nombre"].insert(0, cliente.nombre)
            self.entradas_registro["telefono"].insert(0, cliente.telefono)
            self.entradas_registro["correo"].insert(0, cliente.correo)
            self.entradas_registro["tipo_doc"].set(cliente.tipo_doc)
            self.entradas_registro["num_doc"].insert(0, cliente.num_doc)
            messagebox.showinfo("Búsqueda", "Cliente encontrado y cargado en el formulario.")
        else:
            messagebox.showinfo("Búsqueda", "Cliente no encontrado. Puede usar el formulario para registrarlo.")

    def evento_guardar_cliente(self):
        try:
            nombre = self.entradas_registro["nombre"].get()
            telefono = self.entradas_registro["telefono"].get()
            correo = self.entradas_registro["correo"].get()
            tipo_doc = self.entradas_registro["tipo_doc"].get()
            num_doc = self.entradas_registro["num_doc"].get()

            if not all([nombre, telefono, correo, tipo_doc, num_doc]):
                raise ErrorValidacion("Por favor, complete todos los campos.")

            self.sistema.registrar_cliente(nombre, telefono, correo, tipo_doc, num_doc)
            
            messagebox.showinfo("Éxito", f"Cliente {nombre} registrado exitosamente.")
            
            # Limpiar formulario
            for ent in self.entradas_registro.values():
                if isinstance(ent, tk.Entry):
                    ent.delete(0, tk.END)
            self.entradas_registro["tipo_doc"].set("")
            
            # Actualizar el contador inferior dinámicamente
            total = self.sistema.obtener_total_clientes()
            self.lbl_count_clientes.config(text=f"👥 Clientes registrados: {total}")
            
        except ErrorValidacion as e:
            messagebox.showerror("Error de Validación", str(e))

    def evento_buscar_liq(self):
        doc = self.entry_liq_doc.get().strip()
        cliente = self.sistema.buscar_cliente(doc)
        if cliente:
            self.cliente_actual_liquidacion = cliente
            self.lbl_liq_nombre.config(text=f"Cliente vinculado: {cliente.nombre} ({cliente.num_doc})")
            # Reiniciamos la liquidación actual
            self.lista_liquidacion.delete(0, tk.END)
            self.total_liquidacion = 0
            self.lbl_total.config(text="TOTAL: $ 0")
        else:
            messagebox.showwarning("Error", "Cliente no encontrado. Regístrelo primero en el panel izquierdo.")

    def evento_agregar_servicio(self):
        if not self.cliente_actual_liquidacion:
            messagebox.showwarning("Atención", "Primero debe vincular un cliente usando su documento.")
            return
            
        servicio = self.combo_servicios.get()
        if not servicio:
            messagebox.showwarning("Atención", "Seleccione un servicio de la lista.")
            return
            
        try:
            cant = int(self.entry_cantidad.get())
            if cant <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Error", "La cantidad debe ser un número entero mayor a 0.")
            return

        precio_uni = self.sistema.obtener_precio_servicio(servicio)
        subtotal = precio_uni * cant
        self.total_liquidacion += subtotal
        
        # Formatear el texto para la lista
        texto_item = f"{cant}x {servicio[:20]}... | Sub: ${subtotal:,.0f}"
        self.lista_liquidacion.insert(tk.END, texto_item)
        
        self.lbl_total.config(text=f"TOTAL: $ {self.total_liquidacion:,.0f}")

    def evento_facturar(self):
        if not self.cliente_actual_liquidacion or self.total_liquidacion == 0:
            messagebox.showwarning("Atención", "No hay servicios para liquidar.")
            return
            
        messagebox.showinfo("Liquidación Generada", 
                            f"Se ha liquidado la cuenta para:\n{self.cliente_actual_liquidacion.nombre}\n\n"
                            f"Total a pagar: ${self.total_liquidacion:,.0f}")
        
        # Limpiar módulo tras facturar
        self.cliente_actual_liquidacion = None
        self.lbl_liq_nombre.config(text="Cliente no seleccionado")
        self.lista_liquidacion.delete(0, tk.END)
        self.total_liquidacion = 0
        self.lbl_total.config(text="TOTAL: $ 0")
        self.entry_liq_doc.delete(0, tk.END)

# ==========================================
# 4. EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    motor = SistemaFJ()
    root = tk.Tk()
    app = AppDashboardFJ(root, motor)
    root.mainloop()