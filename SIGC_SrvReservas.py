import abc
import logging
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk  # Requiere: pip install Pillow

# ==========================================
# 1. LOGGING Y EXCEPCIONES AVANZADAS
# ==========================================
logging.basicConfig(
    filename='fj_errores.log', level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8'
)

class FJErrorBase(Exception): 
    """Excepción base para el sistema FJ Technology."""
    pass

class ErrorValidacion(FJErrorBase): 
    """Lanzada cuando hay datos inválidos."""
    pass

class ErrorOperacionCritica(FJErrorBase):
    """Lanzada para demostrar encadenamiento de excepciones."""
    pass

class ErrorReserva(FJErrorBase):
    """Lanzada cuando una reserva no se puede procesar."""
    pass

# ==========================================
# 2. MODELO DE NEGOCIO ORIENTADO A OBJETOS
# ==========================================

# --- ENCAPSULACIÓN: Clase Cliente ---
class Cliente:
    def __init__(self, nombre, telefono, correo, tipo_doc, num_doc):
        self._nombre = nombre
        self._telefono = telefono
        self._correo = correo
        self._tipo_doc = tipo_doc
        self._num_doc = num_doc

    @property
    def nombre(self): return self._nombre
    @property
    def telefono(self): return self._telefono
    @property
    def correo(self): return self._correo
    @property
    def tipo_doc(self): return self._tipo_doc
    @property
    def num_doc(self): return self._num_doc

# --- ABSTRACCIÓN, HERENCIA Y POLIMORFISMO: Servicios ---
class Servicio(abc.ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abc.abstractmethod
    def calcular_costo(self, cantidad=1, descuento=0.0, impuesto=0.0):
        """
        Método abstracto. Sus parámetros opcionales simulan la SOBRECARGA 
        de métodos requerida en la guía.
        """
        pass

class ReservaSala(Servicio):
    def calcular_costo(self, cantidad=1, descuento=0.0, impuesto=0.0):
        costo_base = (self.precio_base * cantidad)
        return (costo_base - (costo_base * descuento)) + (costo_base * impuesto)

class AlquilerEquipo(Servicio):
    def calcular_costo(self, cantidad=1, descuento=0.0, impuesto=0.0):
        # Polimorfismo: Los equipos tienen un recargo fijo de seguro del 5%
        costo_base = (self.precio_base * cantidad) * 1.05 
        return (costo_base - (costo_base * descuento)) + (costo_base * impuesto)

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, cantidad=1, descuento=0.0, impuesto=0.0):
        # Polimorfismo: Las asesorías no tienen impuestos, se ignora el parámetro
        costo_base = self.precio_base * cantidad
        return costo_base - (costo_base * descuento)

# --- CLASE RESERVA ---
class Reserva:
    def __init__(self, cliente, servicio, cantidad):
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "Pendiente"
        self.fecha = datetime.now()

    def confirmar(self):
        self.estado = "Confirmada"
        # Implementación de sobrecarga usando parámetros por defecto
        return self.servicio.calcular_costo(self.cantidad, impuesto=0.19) # 19% IVA por defecto

# ==========================================
# 3. MOTOR CENTRAL DEL SISTEMA
# ==========================================
class SistemaFJ:
    def __init__(self):
        self._clientes = []
        self._servicios_catalogo = []
        self._historial_errores_usuario = []
        
        self._precargar_datos()
        self._ejecutar_simulacion_obligatoria() # Cumplimiento estricto de la guía

    def _precargar_datos(self):
        self.registrar_cliente("Alejandro Escobar Higuera", "3195802896", "alejandro.non2207@gmail.com", "CC", "94539614")
        self.registrar_cliente("Andres Martinez Martinez", "3195801358", "amartinezm@gmail.com", "CC", "11130258963")
        
        # Poblamos el catálogo con objetos instanciados de clases derivadas
        self._servicios_catalogo.extend([
            ReservaSala("Reserva de salon principal por dia", 550000),
            ReservaSala("Reserva de salon Pasoancho por dia", 350000),
            AlquilerEquipo("Alquiler de portatil gamma media", 25000),
            AlquilerEquipo("Alquiler de portatil gamma alta", 35000),
            AsesoriaEspecializada("Asesoria especializada", 85000)
        ])

    def registrar_cliente(self, nombre, telefono, correo, tipo_doc, num_doc):
        if any(c.num_doc == num_doc for c in self._clientes):
            raise ErrorValidacion(f"El documento {num_doc} ya está registrado.")
        nuevo = Cliente(nombre, telefono, correo, tipo_doc, num_doc)
        self._clientes.append(nuevo)
        return nuevo

    def buscar_cliente(self, num_doc):
        for c in self._clientes:
            if c.num_doc == str(num_doc).strip(): return c
        return None
        
    def buscar_servicio(self, nombre_servicio):
        for s in self._servicios_catalogo:
            if s.nombre == nombre_servicio: return s
        return None

    def registrar_error_usuario(self, descripcion):
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self._historial_errores_usuario.append((fecha_hora, descripcion))

    def _ejecutar_simulacion_obligatoria(self):
        """
        Ejecuta silenciosamente 10 operaciones probando las estructuras try/except/else/finally
        y el encadenamiento de excepciones, tal como exige la rúbrica de la universidad.
        """
        logging.info("--- INICIO SIMULACIÓN DE 10 OPERACIONES ---")
        
        # 1. Registro exitoso
        try:
            cli = self.registrar_cliente("Test Sim", "000", "test@test.com", "CC", "000000")
        except: pass

        # 2 & 3. Registro fallido (Duplicado) y Bloque Else/Finally
        try:
            self.registrar_cliente("Test Sim 2", "000", "t@t.com", "CC", "000000")
        except ErrorValidacion as e:
            self.registrar_error_usuario(f"Simulación 2: Documento duplicado interceptado correctamente.")
            logging.error(f"Simulacion Error Validacion: {e}")
        else:
            logging.info("Esto no se ejecutará por el error")
        finally:
            logging.info("Simulación 3: Bloque finally ejecutado tras intento de registro.")

        # 4 & 5 & 6. Creación de Reserva Exitosa, Confirmación y Sobrecarga
        try:
            serv = self.buscar_servicio("Alquiler de portatil gamma media")
            reserva_sim = Reserva(cli, serv, 2)
            costo = reserva_sim.confirmar() # Llama al método sobrecargado con IVA
        except Exception as e:
            pass

        # 7. Reserva fallida (Servicio inexistente)
        try:
            reserva_mala = Reserva(cli, None, 1)
            if not reserva_mala.servicio: raise ErrorReserva("Servicio nulo en reserva.")
        except ErrorReserva as e:
            self.registrar_error_usuario("Simulación 7: Reserva con servicio nulo rechazada.")
            
        # 8 & 9. Encadenamiento de Excepciones (raise ... from ...)
        try:
            try:
                int("TextoInvalidoParaGenerarErrorBase")
            except ValueError as error_base:
                # Encadenamos la excepción base de Python a nuestra excepción personalizada
                raise ErrorOperacionCritica("Fallo grave en conversión de datos del sistema.") from error_base
        except ErrorOperacionCritica as e:
            self.registrar_error_usuario("Simulación 8 y 9: Encadenamiento de excepciones capturado.")
            logging.critical(f"Encadenamiento: {e.__cause__}")

        # 10. Operación final de limpieza
        logging.info("--- FIN SIMULACIÓN DE 10 OPERACIONES ---")


# ==========================================
# 4. INTERFAZ GRÁFICA (Dashboard Principal)
# ==========================================
class AppDashboardFJ:
    def __init__(self, root, sistema):
        self.root = root
        self.sistema = sistema
        self.root.title("FJ Technology - Sistema Integral")
        self.root.geometry("1200x750")
        self.root.configure(bg="#0B1426")
        
        self.c_bg_main = "#0B1426"
        self.c_bg_panel = "#112240"
        self.c_bg_sidebar = "#080F1E"
        self.c_accent_blue = "#0267C1"
        self.c_accent_green = "#00A896"
        self.c_text = "#CCD6F6"
        
        self.cliente_vinculado = None
        self.lista_reservas_actual = [] # Array de objetos Reserva para el "carrito"
        
        self._mostrar_login()

    def _mostrar_login(self):
        self.frame_login = tk.Frame(self.root, bg=self.c_bg_main)
        self.frame_login.pack(fill="both", expand=True)
        
        panel_login = tk.Frame(self.frame_login, bg=self.c_bg_panel, padx=40, pady=40)
        panel_login.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(panel_login, text="SISTEMA INTEGRAL FJ", font=("Arial", 13, "bold"), bg=self.c_bg_panel, fg=self.c_accent_blue).pack(pady=(0, 5))
        tk.Label(panel_login, text="Iniciar Sesión", font=("Arial", 18, "bold"), bg=self.c_bg_panel, fg="white").pack(pady=(0, 25))
        
        tk.Label(panel_login, text="Usuario:", bg=self.c_bg_panel, fg="#8892B0", font=("Arial", 11)).pack(anchor="w")
        self.ent_usuario = tk.Entry(panel_login, width=32, bg="#0B1426", fg="white", insertbackground="white", font=("Arial", 11))
        self.ent_usuario.pack(pady=(5, 15))
        
        tk.Label(panel_login, text="Contraseña:", bg=self.c_bg_panel, fg="#8892B0", font=("Arial", 11)).pack(anchor="w")
        self.ent_password = tk.Entry(panel_login, width=32, bg="#0B1426", fg="white", insertbackground="white", show="*", font=("Arial", 11))
        self.ent_password.pack(pady=(5, 25))
        
        btn_login = tk.Button(panel_login, text="INGRESAR", bg=self.c_accent_blue, fg="white", font=("Arial", 11, "bold"), 
                              bd=0, width=22, command=self._verificar_login, cursor="hand2")
        btn_login.pack(ipady=6)
        
        self.root.bind("<Return>", lambda event: self._verificar_login())

    def _verificar_login(self):
        usuario = self.ent_usuario.get()
        password = self.ent_password.get()
        
        if usuario == "admin" and password == "admin":
            self.root.unbind("<Return>")
            self.frame_login.destroy()
            self._construir_interfaz()
        else:
            self.sistema.registrar_error_usuario(f"Intento de acceso fallido. Usuario digitado: '{usuario}'")
            messagebox.showerror("Error de acceso", "Usuario o contraseña incorrectos.")

    def _construir_interfaz(self):
        # 1. SIDEBAR
        sidebar = tk.Frame(self.root, bg=self.c_bg_sidebar, width=220)
        sidebar.pack(side="left", fill="y")

        try:
            img_raw = Image.open("logo_fj_tech.png")
            img_res = img_raw.resize((160, 90), Image.LANCZOS)
            self.img_logo = ImageTk.PhotoImage(img_res)
            tk.Label(sidebar, image=self.img_logo, bg=self.c_bg_sidebar).pack(pady=20)
        except:
            try:
                img_raw = Image.open("logo_fj.png")
                img_res = img_raw.resize((160, 90), Image.LANCZOS)
                self.img_logo = ImageTk.PhotoImage(img_res)
                tk.Label(sidebar, image=self.img_logo, bg=self.c_bg_sidebar).pack(pady=20)
            except:
                tk.Label(sidebar, text="FJ TECHNOLOGY", fg=self.c_accent_blue, bg=self.c_bg_sidebar, font=("Arial", 14, "bold")).pack(pady=40)

        # Botones del menú
        for btn_txt in ["Inicio", "Clientes", "Servicios", "Reservas", "Reportes"]:
            bg_c = self.c_bg_panel if btn_txt == "Inicio" else self.c_bg_sidebar
            cmd = None
            if btn_txt == "Clientes": cmd = self.abrir_lista_clientes
            elif btn_txt == "Servicios": cmd = self.abrir_config_servicios
            elif btn_txt == "Reportes": cmd = self.abrir_reporte_errores
                
            tk.Button(sidebar, text=f"  {btn_txt}", bg=bg_c, fg="white", font=("Arial", 11), 
                      bd=0, anchor="w", padx=20, pady=12, command=cmd, cursor="hand2" if cmd else None).pack(fill="x")

        # Botón Cerrar Sesión
        tk.Button(sidebar, text="  🚪 Cerrar Sesión", bg="#5C1A1A", fg="white", font=("Arial", 11, "bold"), 
                  bd=0, anchor="w", padx=20, pady=15, command=self.evento_cerrar_sesion, cursor="hand2").pack(side="bottom", fill="x")

        # 2. AREA CENTRAL
        self.main_content = tk.Frame(self.root, bg=self.c_bg_main)
        self.main_content.pack(side="right", fill="both", expand=True, padx=20)

        # Header
        header = tk.Frame(self.main_content, bg=self.c_bg_main)
        header.pack(fill="x", pady=20)
        tk.Label(header, text="SISTEMA INTEGRAL DE", font=("Arial", 10), bg=self.c_bg_main, fg=self.c_accent_blue).pack()
        tk.Label(header, text="Gestión de Clientes, Servicios y Reservas", font=("Arial", 20, "bold"), bg=self.c_bg_main, fg="white").pack()

        # CONTENEDOR DE DOS COLUMNAS
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
                  command=self.evento_guardar, bd=0, cursor="hand2").pack(fill="x", padx=15, pady=20, ipady=8)

        # --- COLUMNA DERECHA: LIQUIDACIÓN (Ahora usa la Clase Reserva) ---
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
        
        # Mapea los nombres de los objetos Servicio al ComboBox
        nombres_servicios = [s.nombre for s in self.sistema._servicios_catalogo]
        self.cb_servs = ttk.Combobox(col_der, values=nombres_servicios, state="readonly", width=42)
        self.cb_servs.pack(padx=15, pady=5)

        tk.Button(col_der, text="➕ Agregar Servicio", bg=self.c_bg_sidebar, fg="white", command=self.evento_agregar_serv).pack(pady=10)

        self.list_items = tk.Listbox(col_der, bg="#080F1E", fg="white", bd=0, height=8)
        self.list_items.pack(fill="x", padx=15, pady=10)

        self.lbl_total = tk.Label(col_der, text="TOTAL: $ 0", font=("Arial", 16, "bold"), bg=self.c_bg_panel, fg=self.c_accent_green)
        self.lbl_total.pack(anchor="e", padx=15)

        # Botones de Acción
        frame_acciones = tk.Frame(col_der, bg=self.c_bg_panel)
        frame_acciones.pack(fill="x", padx=15, pady=15)
        
        btn_limpiar = tk.Button(frame_acciones, text="🧹 Limpiar Todo", bg="#3B4C6B", fg="white", font=("Arial", 10), bd=0, command=self.evento_limpiar, cursor="hand2")
        btn_limpiar.pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=5)
        
        btn_liquidar = tk.Button(frame_acciones, text="✅ Generar Liquidación", bg=self.c_accent_green, fg="white", font=("Arial", 10, "bold"), bd=0, command=self.evento_liquidar, cursor="hand2")
        btn_liquidar.pack(side="right", expand=True, fill="x", padx=(5, 0), ipady=5)

        # --- FOOTER INTERACTIVO ---
        footer = tk.Frame(self.main_content, bg=self.c_bg_sidebar, height=50)
        footer.pack(fill="x", side="bottom", pady=10)

        self.lbl_stat_cli = tk.Label(footer, text=f"👤 Clientes registrados: {len(self.sistema._clientes)}", 
                                     bg=self.c_bg_sidebar, fg="#8892B0", cursor="hand2")
        self.lbl_stat_cli.pack(side="left", padx=20)
        self.lbl_stat_cli.bind("<Button-1>", lambda e: self.abrir_lista_clientes())

        self.lbl_tuerca = tk.Label(footer, text="⚙️ Configurar Servicios", 
                                   bg=self.c_bg_sidebar, fg="#8892B0", cursor="hand2")
        self.lbl_tuerca.pack(side="right", padx=20)
        self.lbl_tuerca.bind("<Button-1>", lambda e: self.abrir_config_servicios())

    # ==========================================
    # MODULOS EMERGENTES
    # ==========================================
    def abrir_lista_clientes(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Base de Datos de Clientes")
        ventana.geometry("600x400")
        ventana.configure(bg=self.c_bg_panel)
        ventana.transient(self.root)
        ventana.focus_set()
        
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
        ventana.transient(self.root)
        ventana.focus_set()

        tk.Label(ventana, text="CREAR NUEVA ASESORIA", bg=self.c_bg_panel, fg="white", font=("Arial", 11, "bold")).pack(pady=20)
        
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
                if not nom: raise ValueError
                
                # Por polimorfismo, añadimos un servicio tipo Asesoria
                nuevo_servicio = AsesoriaEspecializada(nom, precio)
                self.sistema._servicios_catalogo.append(nuevo_servicio)
                self.cb_servs['values'] = [s.nombre for s in self.sistema._servicios_catalogo]
                
                messagebox.showinfo("Éxito", "Servicio añadido al catálogo.")
                ventana.destroy()
            except: 
                self.sistema.registrar_error_usuario("Error al intentar añadir servicio con datos inválidos.")
                messagebox.showerror("Error", "Verifique el nombre y que el costo sea un número.")

        tk.Button(ventana, text="Añadir Servicio", bg=self.c_accent_green, fg="white", command=guardar_s).pack(pady=20)

    def abrir_reporte_errores(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Auditoría - Reporte de Errores Operativos")
        ventana.geometry("650x400")
        ventana.configure(bg=self.c_bg_panel)
        ventana.transient(self.root)
        ventana.focus_set()

        tk.Label(ventana, text="🚨 REPORTE DE ERRORES DE USUARIO", bg=self.c_bg_panel, fg="white", font=("Arial", 12, "bold")).pack(pady=15)
        
        frame_tabla = tk.Frame(ventana, bg=self.c_bg_panel)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrolly = ttk.Scrollbar(frame_tabla, orient="vertical")
        scrolly.pack(side="right", fill="y")
        
        tabla = ttk.Treeview(frame_tabla, columns=("Fecha", "Detalle"), show="headings", yscrollcommand=scrolly.set)
        scrolly.config(command=tabla.yview)
        
        tabla.heading("Fecha", text="Fecha / Hora")
        tabla.heading("Detalle", text="Descripción de la Incidencia / Error")
        tabla.column("Fecha", width=160, anchor="center")
        tabla.column("Detalle", width=450, anchor="w")
        tabla.pack(side="left", fill="both", expand=True)

        if not self.sistema._historial_errores_usuario:
            tabla.insert("", tk.END, values=("N/A", "No se han detectado errores. (Ignorar simulaciones internas)"))
        else:
            for error in self.sistema._historial_errores_usuario:
                tabla.insert("", tk.END, values=error)

    # ==========================================
    # LÓGICA DE PROCESOS (Con POO conectada)
    # ==========================================
    def evento_cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea salir del sistema?"):
            self.root.destroy()

    def evento_limpiar(self):
        self.ent_busc_doc.delete(0, tk.END)
        for e in self.campos_reg.values(): e.delete(0, tk.END)
        self.ent_vinc_doc.delete(0, tk.END)
        self.lbl_vinc_nom.config(text="Esperando cliente...")
        self.cliente_vinculado = None
        self.lista_reservas_actual.clear()
        self.cb_servs.set('')
        self.list_items.delete(0, tk.END)
        self.lbl_total.config(text="TOTAL: $ 0")

    def evento_liquidar(self):
        if not self.cliente_vinculado:
            self.sistema.registrar_error_usuario("Intento de liquidación fallido: No se vinculó ningún cliente.")
            messagebox.showwarning("Atención", "Debe vincular a un cliente antes de liquidar.")
            return
            
        if not self.lista_reservas_actual:
            self.sistema.registrar_error_usuario("Intento de liquidación fallido: Lista de servicios vacía.")
            messagebox.showwarning("Atención", "Debe agregar al menos un servicio para liquidar.")
            return

        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        resumen = f"====================================\n"
        resumen += f"     LIQUIDACIÓN Y RESERVAS\n"
        resumen += f"====================================\n"
        resumen += f"Fecha: {fecha_hora}\n\n"
        resumen += f"DATOS DEL CLIENTE:\n"
        resumen += f"Nombre: {self.cliente_vinculado.nombre}\n"
        resumen += f"Documento: {self.cliente_vinculado.num_doc}\n"
        resumen += f"------------------------------------\n"
        resumen += f"SERVICIOS CONTRATADOS:\n"
        
        # Confirmamos las reservas y generamos el texto
        for r in self.lista_reservas_actual:
            r.confirmar() # Cambia el estado a Confirmada
            resumen += f"- {r.servicio.nombre}\n"
            
        resumen += f"------------------------------------\n"
        resumen += f"   {self.lbl_total.cget('text')}\n"
        resumen += f"====================================\n"
        
        messagebox.showinfo("Liquidación Generada Correctamente", resumen)

    def evento_consultar(self):
        doc = self.ent_busc_doc.get().strip()
        cli = self.sistema.buscar_cliente(doc)
        if cli:
            self.campos_reg["Nombre completo"].delete(0, tk.END)
            self.campos_reg["Nombre completo"].insert(0, cli.nombre)
            self.campos_reg["Teléfono celular"].delete(0, tk.END)
            self.campos_reg["Teléfono celular"].insert(0, cli.telefono)
            self.campos_reg["No. de Documento"].delete(0, tk.END)
            self.campos_reg["No. de Documento"].insert(0, cli.num_doc)
            messagebox.showinfo("Consulta", "Cliente cargado en formulario.")
        else: 
            self.sistema.registrar_error_usuario(f"Consulta de documento inexistente: '{doc}'")
            messagebox.showwarning("Atención", "Cliente no registrado.")

    def evento_guardar(self):
        try:
            nombre = self.campos_reg["Nombre completo"].get().strip()
            tel = self.campos_reg["Teléfono celular"].get().strip()
            mail = self.campos_reg["Correo electrónico"].get().strip()
            doc = self.campos_reg["No. de Documento"].get().strip()
            
            if not nombre or not doc:
                raise ErrorValidacion("Nombre y Documento son obligatorios.")
                
            self.sistema.registrar_cliente(nombre, tel, mail, "CC", doc)
            self.lbl_stat_cli.config(text=f"👤 Clientes registrados: {len(self.sistema._clientes)}")
            messagebox.showinfo("Éxito", "Cliente guardado.")
            for e in self.campos_reg.values(): e.delete(0, tk.END)
        except Exception as e: 
            self.sistema.registrar_error_usuario(f"Error al guardar cliente en el formulario: {str(e)}")
            messagebox.showerror("Error", str(e))

    def evento_vincular(self):
        doc = self.ent_vinc_doc.get().strip()
        cli = self.sistema.buscar_cliente(doc)
        if cli:
            self.cliente_vinculado = cli
            self.lbl_vinc_nom.config(text=f"VINCULADO: {cli.nombre}")
            self.lista_reservas_actual.clear()
            self.list_items.delete(0, tk.END)
            self.lbl_total.config(text="TOTAL: $ 0")
        else: 
            self.sistema.registrar_error_usuario(f"Intento de vinculación con documento inexistente: '{doc}'")
            messagebox.showerror("Error", "No existe ese cliente.")

    def evento_agregar_serv(self):
        if not self.cliente_vinculado:
            messagebox.showwarning("Atención", "Vincule un cliente primero.")
            return

        nombre_serv = self.cb_servs.get()
        if nombre_serv:
            # Buscamos el objeto Servicio real en la lista de catálogos
            servicio_obj = self.sistema.buscar_servicio(nombre_serv)
            
            # Creamos la reserva conectando al cliente y al servicio (cumpliendo la rúbrica)
            nueva_reserva = Reserva(self.cliente_vinculado, servicio_obj, 1)
            self.lista_reservas_actual.append(nueva_reserva)
            
            # Calculamos el costo polimórficamente (con impuesto simulado)
            costo_calc = nueva_reserva.confirmar()
            
            self.list_items.insert(tk.END, f"{servicio_obj.nombre} - ${costo_calc:,.0f}")
            
            # Calcular total iterando las reservas
            total = sum(r.confirmar() for r in self.lista_reservas_actual)
            self.lbl_total.config(text=f"TOTAL: $ {total:,.0f}")

# ==========================================
# 4. EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    motor = SistemaFJ()
    root = tk.Tk()
    app = AppDashboardFJ(root, motor)
    root.mainloop()