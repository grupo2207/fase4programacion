import abc
import logging
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DEL LOGGING
# ==========================================
# Se configura para guardar los errores en un archivo de texto mientras la app se ejecuta.
logging.basicConfig(
    filename='fj_errores.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# ==========================================
# 2. MANEJO AVANZADO DE EXCEPCIONES
# ==========================================
class FJErrorBase(Exception):
    """Clase base abstracta para las excepciones personalizadas del sistema FJ."""
    pass

class ErrorValidacionCliente(FJErrorBase):
    """Excepción lanzada cuando los datos del cliente no cumplen los formatos requeridos."""
    pass

class ErrorReserva(FJErrorBase):
    """Excepción lanzada cuando hay un problema lógico al crear una reserva."""
    pass

# ==========================================
# 3. MODELO DE CLIENTE (Encapsulación y Validaciones)
# ==========================================
class Cliente:
    """Clase que representa a un cliente de FJ. Aplica encapsulación estricta."""
    
    TIPOS_DOC_PERMITIDOS = ['CC', 'TI', 'CE', 'PSP']

    def __init__(self, nombre, tipo_doc, num_doc):
        # Se utilizan los setters para invocar las validaciones inmediatamente
        self.nombre = nombre
        self.tipo_doc = tipo_doc
        self.num_doc = num_doc

    # Propiedad y Setter para Nombre
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Valida que solo contenga letras y espacios
        valor_limpio = str(valor).strip()
        if not all(caracter.isalpha() or caracter.isspace() for caracter in valor_limpio):
            raise ErrorValidacionCliente(f"El nombre '{valor}' es inválido. Solo se permite texto.")
        self.__nombre = valor_limpio

    # Propiedad y Setter para Tipo de Documento
    @property
    def tipo_doc(self):
        return self.__tipo_doc

    @tipo_doc.setter
    def tipo_doc(self, valor):
        valor_upper = str(valor).strip().upper()
        if valor_upper not in self.TIPOS_DOC_PERMITIDOS:
            raise ErrorValidacionCliente(f"Tipo de documento '{valor}' no válido. Opciones: {self.TIPOS_DOC_PERMITIDOS}")
        self.__tipo_doc = valor_upper

    # Propiedad y Setter para Número de Documento
    @property
    def num_doc(self):
        return self.__num_doc

    @num_doc.setter
    def num_doc(self, valor):
        valor_str = str(valor).strip()
        if not valor_str.isdigit():
            raise ErrorValidacionCliente(f"El número de documento '{valor}' es inválido. Solo se permiten números.")
        self.__num_doc = valor_str

    def __str__(self):
        return f"{self.nombre} ({self.tipo_doc} {self.num_doc})"


# ==========================================
# 4. MODELO DE SERVICIOS (Abstracción, Herencia y Polimorfismo)
# ==========================================
class Servicio(abc.ABC):
    """Clase abstracta base para todos los servicios ofrecidos por FJ."""
    
    def __init__(self, id_servicio, descripcion, precio_base):
        self.id_servicio = id_servicio
        self.descripcion = descripcion
        self.precio_base = precio_base

    @abc.abstractmethod
    def calcular_costo_final(self):
        """Método abstracto que las clases derivadas deben implementar (Polimorfismo)."""
        pass

class ReservaSala(Servicio):
    def __init__(self, id_servicio, descripcion, precio_base, horas, requiere_catering=False):
        super().__init__(id_servicio, descripcion, precio_base)
        self.horas = horas
        self.requiere_catering = requiere_catering

    def calcular_costo_final(self):
        costo = self.precio_base * self.horas
        if self.requiere_catering:
            costo += 50000  # Costo adicional fijo simulado
        return costo

class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, descripcion, precio_base, dias, incluye_seguro=True):
        super().__init__(id_servicio, descripcion, precio_base)
        self.dias = dias
        self.incluye_seguro = incluye_seguro

    def calcular_costo_final(self):
        costo = self.precio_base * self.dias
        if self.incluye_seguro:
            costo += (self.precio_base * 0.10) * self.dias # 10% extra por día de seguro
        return costo

class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, descripcion, precio_base, nivel_experto="Senior"):
        super().__init__(id_servicio, descripcion, precio_base)
        self.nivel_experto = nivel_experto

    def calcular_costo_final(self):
        multiplicador = 1.5 if self.nivel_experto == "Senior" else 1.0
        return self.precio_base * multiplicador


# ==========================================
# 5. MODELO DE RESERVAS
# ==========================================
class Reserva:
    """Clase que asocia un Cliente con un Servicio."""
    
    contador_reservas = 1

    def __init__(self, cliente, servicio):
        self.id_reserva = Reserva.contador_reservas
        Reserva.contador_reservas += 1
        self.cliente = cliente
        self.servicio = servicio
        self.fecha_registro = datetime.now()

    def obtener_resumen(self):
        return (f"Reserva #{self.id_reserva} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.descripcion} | Total: ${self.servicio.calcular_costo_final():.2f}")


# ==========================================
# 6. GESTOR PRINCIPAL DEL SISTEMA
# ==========================================
class SistemaFJ:
    """Clase principal para administrar listas internas y lógica de negocio."""
    
    def __init__(self):
        self._clientes = []
        self._reservas = []

    def registrar_cliente(self, nombre, tipo_doc, num_doc):
        """Intenta registrar un cliente usando manejo robusto de excepciones."""
        print(f"\n--- Intentando registrar cliente: {nombre} ---")
        try:
            # Podría generar un ValueError nativo si se pasa un tipo de dato irrecuperable
            # o nuestra excepción personalizada ErrorValidacionCliente
            nuevo_cliente = Cliente(nombre, tipo_doc, num_doc)
            
        except ErrorValidacionCliente as e:
            # Capturamos la excepción específica de negocio
            mensaje_error = f"Error de validación al crear cliente: {e}"
            print(f"❌ FALLO: {mensaje_error}")
            logging.error(mensaje_error)
            
        except Exception as e:
            # Encadenamiento de excepciones (Exception Chaining) por si ocurre un error inesperado
            mensaje_fatal = "Error crítico inesperado durante la creación del cliente."
            logging.critical(f"{mensaje_fatal} Detalles: {e}")
            raise FJErrorBase(mensaje_fatal) from e
            
        else:
            # Se ejecuta SOLO si el bloque try fue exitoso
            self._clientes.append(nuevo_cliente)
            print(f"✅ ÉXITO: Cliente {nuevo_cliente.nombre} registrado correctamente.")
            return nuevo_cliente
            
        finally:
            # Se ejecuta SIEMPRE, haya error o no
            print("-> Proceso de registro finalizado (Verificación de recursos completada).")

    # Simulación de "Sobrecarga de Métodos" (Overloading) usando valores por defecto
    # En Python la sobrecarga clásica no existe, se logra mediante argumentos opcionales.
    def buscar_cliente(self, num_doc=None, nombre=None):
        """Busca un cliente por documento O por nombre (comportamiento sobrecargado)."""
        for cliente in self._clientes:
            if num_doc and cliente.num_doc == num_doc:
                return cliente
            if nombre and cliente.nombre.lower() in nombre.lower():
                return cliente
        return None

    def crear_reserva(self, cliente, servicio):
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("El cliente proporcionado no es válido.")
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("El servicio proporcionado no es válido.")
            
        nueva_reserva = Reserva(cliente, servicio)
        self._reservas.append(nueva_reserva)
        return nueva_reserva

    def mostrar_todas_las_reservas(self):
        print("\n=== LISTADO DE RESERVAS FJ ===")
        if not self._reservas:
            print("No hay reservas en el sistema.")
        for r in self._reservas:
            print(r.obtener_resumen())
        print("==============================\n")


# ==========================================
# 7. EJECUCIÓN DE PRUEBA (Main)
# ==========================================
if __name__ == "__main__":
    # Instanciamos el sistema
    empresa_fj = SistemaFJ()

    # 1. Pruebas de Validaciones y Excepciones (try/except/else/finally en acción)
    
    # Cliente 1: Datos perfectos
    c1 = empresa_fj.registrar_cliente("Juan Perez", "CC", "10203040")
    
    # Cliente 2: Falla el nombre (contiene números)
    c2 = empresa_fj.registrar_cliente("Maria 123", "CE", "99887766")
    
    # Cliente 3: Falla el tipo de documento (invento de sigla)
    c3 = empresa_fj.registrar_cliente("Carlos Ruiz", "PAS", "112233")
    
    # Cliente 4: Falla el número de documento (contiene letras)
    c4 = empresa_fj.registrar_cliente("Ana Gomez", "TI", "123ABC")

    # 2. Creación de Servicios (Polimorfismo en acción)
    if c1:
        # Se crean instancias de clases derivadas con atributos únicos
        servicio_sala = ReservaSala(id_servicio="S01", descripcion="Sala de Juntas VIP", precio_base=25000, horas=4, requiere_catering=True)
        servicio_equipo = AlquilerEquipo(id_servicio="E01", descripcion="Portátil Core i7", precio_base=80000, dias=3, incluye_seguro=True)
        servicio_asesoria = AsesoriaEspecializada(id_servicio="A01", descripcion="Consultoría de Redes", precio_base=200000, nivel_experto="Senior")

        # 3. Creación de Reservas
        empresa_fj.crear_reserva(c1, servicio_sala)
        empresa_fj.crear_reserva(c1, servicio_equipo)
        empresa_fj.crear_reserva(c1, servicio_asesoria)

    # 4. Listado final que demuestra el cálculo polimórfico de costos
    empresa_fj.mostrar_todas_las_reservas()