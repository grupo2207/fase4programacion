import abc                              # Para definir clases abstractas y métodos abstractos
import logging                          # Para el manejo avanzado de errores y auditoría
import tkinter as tk                    # Para la interfaz gráfica
from tkinter import ttk, messagebox     # Para widgets avanzados y cuadros de diálogo
from datetime import datetime           # Para manejar fechas y horas en registros y reportes
from PIL import Image, ImageTk  # Requiere: pip install Pillow

# ==========================================
# 1. LOGGING Y EXCEPCIONES AVANZADAS
# ==========================================
logging.basicConfig(                    # Configuración del logging para errores críticos y encadenados
    filename='fj_errores.log', level=logging.ERROR,                         # Solo errores críticos y encadenados se registrarán en el archivo
    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8'    # Configuración de formato y codificación para el archivo de log
)

class FJErrorBase(Exception):           # Excepción base personalizada para el sistema, permite un manejo más específico y organizado de errores
    """Excepción base para el sistema FJ Technology."""
    pass

class ErrorValidacion(FJErrorBase):     # Excepción específica para errores de validación, como datos duplicados o formatos incorrectos, lo que mejora la claridad y el manejo de errores en el sistema. 
    """Lanzada cuando hay datos inválidos."""
    pass

class ErrorOperacionCritica(FJErrorBase): # Excepción para operaciones críticas que fallan, diseñada para demostrar el enc 
    """Lanzada para demostrar encadenamiento de excepciones."""
    pass

class ErrorReserva(FJErrorBase):        # Excepción específica para problemas relacionados con reservas, como intentar reservar un servicio inexistente o con datos incompletos, lo que ayuda a mantener la lógica de negocio clara y manejable.
    """Lanzada cuando una reserva no se puede procesar."""
    pass

# ==========================================
# 2. MODELO DE NEGOCIO ORIENTADO A OBJETOS
# ==========================================

# --- ENCAPSULACIÓN: Clase Cliente ---
class Cliente:
    def __init__(self, nombre, telefono, correo, tipo_doc, num_doc): # El constructor de la clase Cliente, que inicializa los atributos privados con los datos proporcionados al crear una instancia de Cliente.
        self._nombre = nombre 
        self._telefono = telefono
        self._correo = correo
        self._tipo_doc = tipo_doc
        self._num_doc = num_doc

    @property # Decoradores @property para acceder a los atributos privados de manera controlada, permitiendo la lectura de los datos del cliente sin exponer directamente los atributos internos.
    def nombre(self): return self._nombre
    @property # Decorador @property para el atributo teléfono, que permite acceder al número de teléfono del cliente de forma segura y controlada, manteniendo la integridad de los datos.
    def telefono(self): return self._telefono
    @property # Decorador @property para el atributo correo, que proporciona una forma segura de acceder a la dirección de correo electrónico del cliente, manteniendo la encapsulación y protegiendo los datos internos de la clase.
    def correo(self): return self._correo
    @property # Decorador @property para el tipo de documento, que permite acceder al tipo de documento del cliente de manera controlada, manteniendo la integridad de los datos y la encapsulación dentro de la clase Cliente.
    def tipo_doc(self): return self._tipo_doc
    @property # Decorador @property para el número de documento, que proporciona una forma segura de acceder al número de documento del cliente, manteniendo la encapsulación y protegiendo los datos internos de la clase Cliente.
    def num_doc(self): return self._num_doc

# --- ABSTRACCIÓN, HERENCIA Y POLIMORFISMO: Servicios ---
class Servicio(abc.ABC):        # Clase abstracta que define la estructura general de un servicio, con un método abstracto para calcular el costo, lo que obliga a las clases derivadas a implementar su propia lógica de cálculo, demostrando así la abstracción, herencia y polimorfismo en el diseño del sistema.
    def __init__(self, nombre, precio_base): # El constructor de la clase Servicio, que inicializa los atributos nombre y precio_base, proporcionando una base común para todos los servicios derivados, lo que permite la reutilización de código y la implementación de diferentes tipos de servicios con su propia lógica de cálculo.
        self.nombre = nombre 
        self.precio_base = precio_base

    @abc.abstractmethod         # Decorador @abc.abstractmethod para el método calcular_costo, que obliga a las clases derivadas a implementar su propia versión de este método, permitiendo la flexibilidad y la personalización del cálculo de costos según el tipo de servicio, demostrando así el polimorfismo en la estructura del sistema.
    def calcular_costo(self, cantidad=1, descuento=0.0, impuesto=0.0): # El método abstracto calcular_costo, que define la firma del método que debe ser implementado por todas las clases derivadas de Servicio, con parámetros opcionales para cantidad, descuento e impuesto, lo que permite la sobrecarga de métodos simulada en Python y proporciona una estructura flexible para el cálculo de costos en diferentes tipos de servicios.
        """
        Método abstracto. Sus parámetros opcionales simulan la SOBRECARGA 
        de métodos requerida en la guía.
        """
        pass

class ReservaSala(Servicio):    # Clase que representa la reserva de una sala, heredando de la clase Servicio y proporcionando su propia implementación del método calcular_costo, que calcula el costo total de la reserva teniendo en cuenta la cantidad, el descuento y el impuesto, demostrando así el polimorfismo en la estructura del sistema.
    def calcular_costo(self, cantidad=1, descuento=0.0, impuesto=0.0): # Implementación del método calcular_costo para la clase ReservaSala, que calcula el costo total de la reserva de una sala multiplicando el precio base por la cantidad, aplicando el descuento y sumando el impuesto, lo que permite una lógica de cálculo específica para este tipo de servicio, demostrando así el polimorfismo en la estructura del sistema.
        costo_base = (self.precio_base * cantidad)  # Costo base sin impuestos ni descuentos
        return (costo_base - (costo_base * descuento)) + (costo_base * impuesto)

class AlquilerEquipo(Servicio): # Clase que representa el alquiler de un equipo, heredando de la clase Servicio y proporcionando su propia implementación del método calcular_costo, que calcula el costo total del alquiler teniendo en cuenta la cantidad, el descuento y el impuesto, además de aplicar un recargo fijo de seguro del 5% al costo base, lo que demuestra el polimorfismo en la estructura del sistema al permitir una lógica de cálculo específica para este tipo de servicio.
    def calcular_costo(self, cantidad=1, descuento=0.0, impuesto=0.0): # Implementación del método calcular_costo para la clase AlquilerEquipo, que calcula el costo total del alquiler de un equipo multiplicando el precio base por la cantidad, aplicando un recargo fijo de seguro del 5%, luego aplicando el descuento y sumando el impuesto, lo que permite una lógica de cálculo específica para este tipo de servicio, demostrando así el polimorfismo en la estructura del sistema.
        # Polimorfismo: Los equipos tienen un recargo fijo de seguro del 5%
        costo_base = (self.precio_base * cantidad) * 1.05  # Recargo del 5% por seguro
        return (costo_base - (costo_base * descuento)) + (costo_base * impuesto) # Aplicación de descuento e impuesto al costo base con recargo

class AsesoriaEspecializada(Servicio): # Clase que representa una asesoría especializada, heredando de la clase Servicio y proporcionando su propia implementación del método calcular_costo, que calcula el costo total de la asesoría teniendo en cuenta la cantidad y el descuento, pero ignorando el impuesto ya que las asesorías no tienen impuestos, lo que demuestra el polimorfismo en la estructura del sistema al permitir una lógica de cálculo específica para este tipo de servicio.
    def calcular_costo(self, cantidad=1, descuento=0.0, impuesto=0.0): # Implementación del método calcular_costo para la clase AsesoriaEspecializada, que calcula el costo total de una asesoría especializada multiplicando el precio base por la cantidad y aplicando el descuento, pero ignorando el impuesto ya que las asesorías no tienen impuestos, lo que permite una lógica de cálculo específica para este tipo de servicio, demostrando así el polimorfismo en la estructura del sistema.
        # Polimorfismo: Las asesorías no tienen impuestos, se ignora el parámetro
        costo_base = self.precio_base * cantidad # Costo base sin impuestos
        return costo_base - (costo_base * descuento) # Descuento aplicado, sin impuestos

# --- CLASE RESERVA ---
class Reserva: # Clase que representa una reserva realizada por un cliente para un servicio específico, con atributos para el cliente, el servicio, la cantidad, el estado de la reserva y la fecha de creación, además de un método confirmar que cambia el estado de la reserva a "Confirmada" y calcula el costo total utilizando el método calcular_costo del servicio asociado, demostrando así la conexión entre las clases Cliente y Servicio en la lógica de negocio del sistema.
    def __init__(self, cliente, servicio, cantidad): # El constructor de la clase Reserva, que inicializa los atributos cliente, servicio, cantidad, estado y fecha, estableciendo el estado inicial de la reserva como "Pendiente" y registrando la fecha de creación, lo que permite gestionar el proceso de reserva de manera organizada y estructurada dentro del sistema.
        self.cliente = cliente      # Referencia al objeto Cliente que realiza la reserva, lo que permite acceder a los datos del cliente asociado a la reserva y mantener una relación clara entre las clases Cliente y Reserva en la lógica de negocio del sistema.
        self.servicio = servicio    # Referencia al objeto Servicio que se está reservando, lo que permite acceder a los detalles del servicio reservado y utilizar su método calcular_costo para determinar el costo total de la reserva, demostrando así la conexión entre las clases Servicio y Reserva en la lógica de negocio del sistema.
        self.cantidad = cantidad    # Cantidad de unidades del servicio reservado, lo que permite calcular el costo total de la reserva en función de la cantidad y aplicar descuentos o impuestos según sea necesario, demostrando así la flexibilidad en la gestión de reservas dentro del sistema.
        self.estado = "Pendiente"   # Estado inicial de la reserva, que puede cambiar a "Confirmada" u otros estados según el proceso de gestión de reservas, lo que permite un seguimiento claro del estado de cada reserva dentro del sistema.
        self.fecha = datetime.now() # Fecha y hora de creación de la reserva, lo que permite llevar un registro temporal de las reservas realizadas y facilitar la gestión de reservas en función del tiempo dentro del sistema.

    def confirmar(self):    # Método para confirmar la reserva, que cambia el estado de la reserva a "Confirmada" y calcula el costo total utilizando el método calcular_costo del servicio asociado, lo que permite finalizar el proceso de reserva y obtener el costo total de la reserva de manera organizada y estructurada dentro del sistema.
        self.estado = "Confirmada"  # Cambia el estado de la reserva a "Confirmada", lo que indica que la reserva ha sido finalizada y está lista para ser procesada o facturada, lo que permite un seguimiento claro del estado de cada reserva dentro del sistema.
        # Implementación de sobrecarga usando parámetros por defecto
        return self.servicio.calcular_costo(self.cantidad, impuesto=0.19) # 19% IVA por defecto

# ==========================================
# 3. MOTOR CENTRAL DEL SISTEMA
# ==========================================
class SistemaFJ:                                # Clase principal del sistema que gestiona clientes, servicios y reservas, con métodos para registrar clientes, buscar clientes y servicios, registrar errores de usuario y ejecutar una simulación de operaciones para demostrar el manejo avanzado de excepciones, lo que proporciona la lógica central del sistema y conecta las diferentes partes del modelo de negocio orientado a objetos.
    def __init__(self):                         # El constructor de la clase SistemaFJ, que inicializa las listas para clientes, servicios y el historial de errores de usuario, además de llamar a los métodos para precargar datos y ejecutar la simulación obligatoria, lo que establece la base de datos inicial del sistema y demuestra el manejo avanzado de excepciones desde el inicio.
        self._clientes = []                     # Lista para almacenar objetos Cliente registrados en el sistema, lo que permite gestionar y acceder a los clientes de manera organizada dentro del sistema.
        self._servicios_catalogo = []           # Lista para almacenar objetos Servicio disponibles en el catálogo del sistema, lo que permite gestionar y acceder a los servicios de manera organizada dentro del sistema. 
        self._historial_errores_usuario = []    # Lista para almacenar registros de errores operativos cometidos por los usuarios, lo que permite llevar un seguimiento de las incidencias y mejorar la auditoría y el manejo de errores dentro del sistema.
        
        self._precargar_datos()                 # Método para precargar datos de clientes y servicios en el sistema, lo que permite tener una base de datos inicial para pruebas y demostraciones, facilitando el desarrollo y la validación del sistema.
        self._ejecutar_simulacion_obligatoria() # Cumplimiento estricto de la guía

    def _precargar_datos(self):                 # Método para precargar datos de clientes y servicios en el sistema, que registra clientes con información de contacto y documentos, y añade servicios al catálogo con sus respectivos precios, lo que establece una base de datos inicial para pruebas y demostraciones, facilitando el desarrollo y la validación del sistema.
        self.registrar_cliente("Alejandro Escobar Higuera", "3195802896", "alejandro.non2207@gmail.com", "CC", "94539614") # Registro de cliente con datos de contacto y documento, lo que permite tener un cliente inicial para pruebas y demostraciones dentro del sistema.
        self.registrar_cliente("Andres Martinez Martinez", "3195801358", "amartinezm@gmail.com", "CC", "11130258963") # Registro de cliente con datos de contacto y documento, lo que permite tener un cliente adicional para pruebas y demostraciones dentro del sistema.
        
        # Poblamos el catálogo con objetos instanciados de clases derivadas
        self._servicios_catalogo.extend([       # Añade servicios al catálogo utilizando objetos instanciados de las clases derivadas de Servicio, lo que permite tener una variedad de servicios disponibles para reservas y demuestra la aplicación de la herencia y el polimorfismo en el diseño del sistema.
            ReservaSala("Reserva de salon principal por dia", 550000),  # Servicio de reserva de sala principal con un precio base, lo que permite ofrecer una opción de reserva de sala con un costo específico dentro del catálogo de servicios del sistema.
            ReservaSala("Reserva de salon Pasoancho por dia", 350000),  # Servicio de reserva de sala Pasoancho con un precio base, lo que permite ofrecer una opción de reserva de sala adicional con un costo específico dentro del catálogo de servicios del sistema.
            AlquilerEquipo("Alquiler de portatil gamma media", 25000),  # Servicio de alquiler de portátil gamma media con un precio base, lo que permite ofrecer una opción de alquiler de equipo con un costo específico dentro del catálogo de servicios del sistema.
            AlquilerEquipo("Alquiler de portatil gamma alta", 35000),   # Servicio de alquiler de portátil gamma alta con un precio base, lo que permite ofrecer una opción de alquiler de equipo adicional con un costo específico dentro del catálogo de servicios del sistema.
            AsesoriaEspecializada("Asesoria especializada", 85000)      # Servicio de asesoría especializada con un precio base, lo que permite ofrecer una opción de asesoría con un costo específico dentro del catálogo de servicios del sistema, demostrando así la aplicación de la herencia y el polimorfismo en el diseño del sistema al incluir diferentes tipos de servicios con su propia lógica de cálculo de costos.
        ])

    def registrar_cliente(self, nombre, telefono, correo, tipo_doc, num_doc):       # Método para registrar un nuevo cliente en el sistema, que verifica si el número de documento ya está registrado para evitar duplicados, y si no lo está, crea un nuevo objeto Cliente y lo añade a la lista de clientes, lo que permite gestionar los clientes de manera organizada dentro del sistema y mantener la integridad de los datos.
        if any(c.num_doc == num_doc for c in self._clientes):                       # Verificación de documento duplicado, lo que permite evitar la creación de clientes con el mismo número de documento y mantener la integridad de los datos dentro del sistema.
            raise ErrorValidacion(f"El documento {num_doc} ya está registrado.")    # Lanza una excepción de validación si el número de documento ya está registrado, lo que permite manejar este tipo de error de manera específica y mejorar la experiencia del usuario al proporcionar retroalimentación clara sobre el problema.
        nuevo = Cliente(nombre, telefono, correo, tipo_doc, num_doc)                # Creación de un nuevo objeto Cliente con los datos proporcionados, lo que permite encapsular la información del cliente en una instancia de la clase Cliente y facilitar su gestión dentro del sistema.
        self._clientes.append(nuevo)                                                # Añade el nuevo cliente a la lista de clientes del sistema, lo que permite mantener un registro organizado de todos los clientes registrados y facilitar su acceso y gestión dentro del sistema.
        return nuevo                                                                # Retorna el nuevo cliente registrado, lo que permite utilizar el objeto Cliente creado para otras operaciones dentro del sistema, como realizar reservas o consultas, facilitando la integración de las diferentes partes del sistema y mejorando la eficiencia en la gestión de clientes. 

    def buscar_cliente(self, num_doc):                          # Método para buscar un cliente en el sistema por su número de documento, que recorre la lista de clientes y devuelve el cliente que coincide con el número de documento proporcionado, o None si no se encuentra, lo que permite acceder a la información del cliente de manera eficiente dentro del sistema y facilita la gestión de clientes en operaciones como reservas o consultas.
        for c in self._clientes:                                # Recorre la lista de clientes para encontrar una coincidencia con el número de documento proporcionado, lo que permite realizar una búsqueda eficiente y directa dentro del sistema para acceder a la información del cliente.
            if c.num_doc == str(num_doc).strip(): return c      # Compara el número de documento de cada cliente con el número proporcionado, después de convertirlo a cadena y eliminar espacios en blanco, lo que permite una comparación más robusta y evita problemas con formatos de entrada, mejorando la experiencia del usuario al permitir búsquedas más flexibles.
        return None                                             # Retorna None si no se encuentra ningún cliente con el número de documento proporcionado, lo que permite manejar el caso de búsqueda fallida de manera clara y proporciona una respuesta consistente para las operaciones que dependen de la búsqueda de clientes dentro del sistema.    
        
    def buscar_servicio(self, nombre_servicio):                 # Método para buscar un servicio en el catálogo por su nombre, que recorre la lista de servicios y devuelve el servicio que coincide con el nombre proporcionado, o None si no se encuentra, lo que permite acceder a la información del servicio de manera eficiente dentro del sistema y facilita la gestión de servicios en operaciones como reservas o consultas.
        for s in self._servicios_catalogo:                      # Recorre la lista de servicios en el catálogo para encontrar una coincidencia con el nombre del servicio proporcionado, lo que permite realizar una búsqueda eficiente y directa dentro del sistema para acceder a la información del servicio.
            if s.nombre == nombre_servicio: return s            # Compara el nombre de cada servicio con el nombre proporcionado, lo que permite una comparación directa y eficiente para encontrar el servicio deseado dentro del sistema, mejorando la experiencia del usuario al permitir búsquedas rápidas y precisas.
        return None

    def registrar_error_usuario(self, descripcion):                         # Método para registrar un error operativo cometido por un usuario, que añade una entrada al historial de errores de usuario con la descripción del error y la fecha y hora en que ocurrió, lo que permite llevar un seguimiento de las incidencias y mejorar la auditoría y el manejo de errores dentro del sistema.
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")           # Obtiene la fecha y hora actual formateada como una cadena legible, lo que permite registrar el momento exacto en que ocurrió el error para facilitar la auditoría y el seguimiento de incidencias dentro del sistema.
        self._historial_errores_usuario.append((fecha_hora, descripcion))   # Añade una tupla con la fecha y hora y la descripción del error al historial de errores de usuario, lo que permite mantener un registro organizado de todas las incidencias y proporciona una base de datos para análisis y mejoras en el manejo de errores dentro del sistema.

    def _ejecutar_simulacion_obligatoria(self): # Método para ejecutar una simulación de 10 operaciones que demuestran el manejo avanzado de excepciones, incluyendo el uso de try/except/else/finally y el encadenamiento de excepciones, lo que cumple con los requisitos de la guía de la universidad y proporciona una demostración práctica del manejo de errores en el sistema.
        """
        Ejecuta silenciosamente 10 operaciones probando las estructuras try/except/else/finally
        y el encadenamiento de excepciones, tal como exige la rúbrica de la universidad.
        """
        logging.info("--- INICIO SIMULACIÓN DE 10 OPERACIONES ---") # Registro de inicio de la simulación en el log, lo que permite identificar claramente el comienzo de la sección de pruebas y facilita la revisión de los resultados en el archivo de log para verificar el manejo avanzado de excepciones implementado en el sistema.
        
        # 1. Registro exitoso
        try:
            cli = self.registrar_cliente("Sujeto de prueba 1", "123456789", "prueba1@prueba.com", "CC", "123456789") # Registro de un cliente de prueba con datos válidos, lo que permite demostrar el proceso de registro exitoso dentro del sistema y proporciona un cliente para utilizar en las operaciones posteriores de la simulación.
        except: pass

        # 2 & 3. Registro fallido (Duplicado) y Bloque Else/Finally
        try:
            self.registrar_cliente("Sujeto de prueba 2", "1234567890", "prueba2@prueba.com", "CC", "1234567890") # Registro de un cliente de prueba con un número de documento que ya está registrado, lo que permite demostrar el manejo de errores de validación para datos duplicados dentro del sistema y proporciona una situación para probar el bloque except específico para este tipo de error.
        except ErrorValidacion as e:
            self.registrar_error_usuario(f"Simulación 2: Documento duplicado interceptado correctamente.") # Registro de un error de validación específico para el caso de documento duplicado, lo que permite demostrar la capacidad del sistema para manejar este tipo de error de manera específica y mejorar la experiencia del usuario al proporcionar retroalimentación clara sobre el problema, además de cumplir con los requisitos de la guía de la universidad para el manejo avanzado de excepciones.
            logging.error(f"Simulacion Error Validacion: {e}") # Registro del error de validación en el log, lo que permite mantener un registro detallado de las incidencias y facilita la revisión de los resultados en el archivo de log para verificar el manejo avanzado de excepciones implementado en el sistema.
        else:
            logging.info("Esto no se ejecutará por el error") # Bloque else que no se ejecutará debido al error de validación, lo que permite demostrar la estructura completa de manejo de excepciones con try/except/else y resalta la importancia de cada bloque en el flujo de control del programa, además de cumplir con los requisitos de la guía de la universidad para el manejo avanzado de excepciones.
        finally:
            logging.info("Simulación 3: Bloque finally ejecutado tras intento de registro.") # Bloque finally que se ejecuta después del intento de registro, lo que permite demostrar que este bloque se ejecuta independientemente de si ocurrió una excepción o no, y proporciona un punto de registro para indicar que se ha completado el proceso de manejo de excepciones para esta operación, además de cumplir con los requisitos de la guía de la universidad para el manejo avanzado de excepciones.

        # 4 & 5 & 6. Creación de Reserva Exitosa, Confirmación y Sobrecarga
        try:
            serv = self.buscar_servicio("Alquiler de portatil gamma media") # Búsqueda de un servicio específico en el catálogo para utilizar en la creación de una reserva, lo que permite demostrar la capacidad del sistema para gestionar servicios y preparar una operación de reserva que se utilizará para probar la creación exitosa de una reserva, su confirmación y la sobrecarga de métodos simulada a través de parámetros por defecto.
            reserva_sim = Reserva(cli, serv, 2) # Creación de una reserva con el cliente y servicio encontrados, utilizando un número de días específico.
            costo = reserva_sim.confirmar() # Llama al método sobrecargado con IVA
        except Exception as e: # Captura cualquier excepción que pueda ocurrir durante la creación y confirmación de la reserva, lo que permite manejar de manera general cualquier error inesperado en este proceso y proporciona una oportunidad para registrar el error en el log, además de cumplir con los requisitos de la guía de la universidad para el manejo avanzado de excepciones.
            pass

        # 7. Reserva fallida (Servicio inexistente)
        try: # Intento de crear una reserva con un servicio nulo para demostrar el manejo de errores específicos relacionados con reservas, lo que permite mostrar cómo el sistema puede manejar situaciones en las que se intenta reservar un servicio que no existe o no se ha proporcionado, y proporciona una oportunidad para registrar este tipo de error de manera específica en el log, además de cumplir con los requisitos de la guía de la universidad para el manejo avanzado de excepciones.
            reserva_mala = Reserva(cli, None, 1)
            if not reserva_mala.servicio: raise ErrorReserva("Servicio nulo en reserva.")
        except ErrorReserva as e: # Captura de la excepción específica para reservas, lo que permite manejar de manera específica los errores relacionados con reservas y proporciona una oportunidad para registrar este tipo de error en el log, además de cumplir con los requisitos de la guía de la universidad para el manejo avanzado de excepciones.
            self.registrar_error_usuario("Simulación 7: Reserva con servicio nulo rechazada.")
            
        # 8 & 9. Encadenamiento de Excepciones (raise ... from ...)
        try: # Intento de crear una excepción encadenada para demostrar el manejo de errores específicos, lo que permite mostrar cómo el sistema puede manejar situaciones en las que un error de bajo nivel es convertido en un error más específico, y proporciona una oportunidad para registrar este tipo de error en el log, además de cumplir con los requisitos de la guía de la universidad para el manejo avanzado de excepciones.
            try: # Intento de generar un error base (ValueError) para luego encadenarlo a una excepción personalizada, lo que permite demostrar el uso de raise ... from ... para crear una cadena de excepciones que proporciona más contexto sobre el error original, y proporciona una oportunidad para registrar este tipo de error en el log, además de cumplir con los requisitos de la guía de la universidad para el manejo avanzado de excepciones.
                int("TextoInvalidoParaGenerarErrorBase")
            except ValueError as error_base:
                # Encadenamos la excepción base de Python a nuestra excepción personalizada
                raise ErrorOperacionCritica("Fallo grave en conversión de datos del sistema.") from error_base
        except ErrorOperacionCritica as e: # Captura de la excepción personalizada que encadena la excepción base, lo que permite manejar de manera específica los errores críticos en el sistema y proporciona una oportunidad para registrar este tipo de error en el log, además de cumplir con los requisitos de la guía de la universidad para el manejo avanzado de excepciones.
            self.registrar_error_usuario("Simulación 8 y 9: Encadenamiento de excepciones capturado.")
            logging.critical(f"Encadenamiento: {e.__cause__}")

        # 10. Operación final de limpieza
        logging.info("--- FIN SIMULACIÓN DE 10 OPERACIONES ---") # Registro de fin de la simulación en el log, lo que permite identificar claramente el final de la sección de pruebas y facilita la revisión de los resultados en el archivo de log para verificar el manejo avanzado de excepciones implementado en el sistema, además de cumplir con los requisitos de la guía de la universidad para el manejo avanzado de excepciones.


# ==========================================
# 4. INTERFAZ GRÁFICA (Dashboard Principal)
# ==========================================
class AppDashboardFJ: # Clase principal de la interfaz gráfica del sistema, que gestiona la ventana principal, el proceso de inicio de sesión y la construcción de la interfaz de usuario, lo que proporciona una experiencia visual para interactuar con el sistema y conecta la lógica del negocio con la presentación al usuario.
    def __init__(self, root, sistema): # El constructor de la clase AppDashboardFJ, que inicializa la ventana principal, configura su apariencia y llama al método para mostrar la pantalla de inicio de sesión, lo que establece la base de la interfaz gráfica y proporciona una experiencia visual para interactuar con el sistema desde el inicio.
        self.root = root                                    # Referencia a la ventana principal de Tkinter, lo que permite gestionar la ventana y sus componentes dentro de la clase AppDashboardFJ y facilita la construcción de la interfaz gráfica del sistema.
        self.sistema = sistema                              # Referencia al objeto del sistema (SistemaFJ), lo que permite acceder a la lógica del negocio y los datos del sistema desde la interfaz gráfica, facilitando la integración entre la presentación y la lógica del negocio en el diseño del sistema.
        self.root.title("FJ Technology - Sistema Integral") # Configuración del título de la ventana principal, lo que proporciona una identificación clara del sistema en la interfaz gráfica y mejora la experiencia del usuario al saber qué aplicación está utilizando.
        self.root.geometry("1200x750")                      # Configuración del tamaño de la ventana principal, lo que proporciona un espacio adecuado para mostrar la interfaz gráfica y sus componentes de manera organizada y visualmente atractiva, mejorando la experiencia del usuario al interactuar con el sistema.
        self.root.configure(bg="#0B1426")                 # Configuración del color de fondo de la ventana principal, lo que contribuye a la estética visual del sistema y proporciona una base para el diseño de la interfaz gráfica, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y atractivo.
        
        self.c_bg_main = "#0B1426"          # Definición de colores para la interfaz gráfica, lo que permite mantener una paleta de colores coherente y atractiva en el diseño de la interfaz, mejorando la experiencia del usuario al interactuar con un entorno visualmente agradable y profesional. 
        self.c_bg_panel = "#112240"         # Color de fondo para paneles y secciones dentro de la interfaz, lo que proporciona contraste con el fondo principal y ayuda a resaltar las áreas de contenido, mejorando la legibilidad y la organización visual de la interfaz gráfica del sistema.
        self.c_bg_sidebar = "#080F1E"       # Color de fondo para la barra lateral, lo que proporciona un contraste visual con el fondo principal y ayuda a diferenciar claramente la sección de navegación del resto del contenido, mejorando la experiencia del usuario al interactuar con la interfaz gráfica del sistema.
        self.c_accent_blue = "#0267C1"      # Color de acento azul para elementos destacados, lo que proporciona un contraste visual atractivo y ayuda a resaltar elementos importantes en la interfaz gráfica, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional.
        self.c_accent_green = "#00A896"     # Color de acento verde para elementos destacados, lo que proporciona un contraste visual atractivo y ayuda a resaltar elementos importantes en la interfaz gráfica, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional.
        self.c_text = "#CCD6F6"             # Color de texto principal para la interfaz gráfica, lo que proporciona una buena legibilidad y contraste con el fondo, mejorando la experiencia del usuario al interactuar con un entorno visualmente agradable y fácil de leer dentro del sistema.
        
        self.cliente_vinculado = None         # Atributo para almacenar el cliente actualmente vinculado a la sesión, lo que permite mantener un seguimiento del cliente que está interactuando con el sistema en la interfaz gráfica y facilita la gestión de operaciones relacionadas con ese cliente, como reservas o consultas, mejorando la experiencia del usuario al proporcionar una interacción personalizada dentro del sistema.  
        self.lista_reservas_actual = []       # Array de objetos Reserva para el "carrito"
        
        self._mostrar_login()                 # Llamada al método para mostrar la pantalla de inicio de sesión, lo que establece el primer punto de interacción del usuario con la interfaz gráfica y proporciona una experiencia visual para acceder al sistema de manera segura, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio.  

    def _mostrar_login(self):                 # Método para mostrar la pantalla de inicio de sesión, que construye un panel de login con campos para el usuario y la contraseña, y un botón para iniciar sesión, lo que proporciona una experiencia visual para acceder al sistema de manera segura y establece el primer punto de interacción del usuario con la interfaz gráfica, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio.
        self.frame_login = tk.Frame(self.root, bg=self.c_bg_main) # Creación de un marco para la pantalla de inicio de sesión, lo que permite organizar los elementos del login de manera estructurada y visualmente atractiva dentro de la interfaz gráfica, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio.
        self.frame_login.pack(fill="both", expand=True) # Configuración del marco de inicio de sesión para que ocupe toda la ventana, lo que proporciona un espacio adecuado para mostrar los elementos del login de manera organizada y visualmente atractiva, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio.
        
        panel_login = tk.Frame(self.frame_login, bg=self.c_bg_panel, padx=40, pady=40) # Creación de un panel dentro del marco de inicio de sesión para contener los elementos del login, lo que permite organizar los campos de usuario y contraseña, y el botón de inicio de sesión de manera estructurada y visualmente atractiva, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio.
        panel_login.place(relx=0.5, rely=0.5, anchor="center") # Posicionamiento del panel de inicio de sesión en el centro de la ventana, lo que proporciona un diseño equilibrado y visualmente atractivo para la pantalla de login, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio.
        
        tk.Label(panel_login, text="SISTEMA INTEGRAL FJ", font=("Arial", 13, "bold"), bg=self.c_bg_panel, fg=self.c_accent_blue).pack(pady=(0, 5)) # Etiqueta para el título del sistema en la pantalla de inicio de sesión, lo que proporciona una identificación clara del sistema y mejora la experiencia del usuario al saber qué aplicación está utilizando desde el inicio, además de contribuir a la estética visual de la interfaz gráfica.
        tk.Label(panel_login, text="Iniciar Sesión", font=("Arial", 18, "bold"), bg=self.c_bg_panel, fg="white").pack(pady=(0, 25)) # Etiqueta para el subtítulo de la pantalla de inicio de sesión, lo que proporciona una guía clara para el usuario sobre la acción que debe realizar y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio, además de contribuir a la estética visual de la interfaz gráfica.
        
        tk.Label(panel_login, text="Usuario:", bg=self.c_bg_panel, fg="#8892B0", font=("Arial", 11)).pack(anchor="w") # 
        self.ent_usuario = tk.Entry(panel_login, width=32, bg="#0B1426", fg="white", insertbackground="white", font=("Arial", 11)) # Campo de entrada para el usuario en la pantalla de inicio de sesión, lo que permite al usuario ingresar su nombre de usuario de manera segura y visualmente coherente con el diseño de la interfaz gráfica, mejorando la experiencia del usuario al interactuar con un entorno visualmente atractivo y profesional desde el inicio.
        self.ent_usuario.pack(pady=(5, 15)) # Configuración del campo de entrada para el usuario con un margen inferior, lo que proporciona un espacio adecuado entre los elementos del login y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio.
        
        tk.Label(panel_login, text="Contraseña:", bg=self.c_bg_panel, fg="#8892B0", font=("Arial", 11)).pack(anchor="w") # Etiqueta para el campo de contraseña en la pantalla de inicio de sesión, lo que proporciona una identificación clara del campo y mejora la experiencia del usuario al saber qué información debe ingresar.
        self.ent_password = tk.Entry(panel_login, width=32, bg="#0B1426", fg="white", insertbackground="white", show="*", font=("Arial", 11)) # 
        self.ent_password.pack(pady=(5, 25)) # Configuración del campo de entrada para la contraseña con un margen inferior, lo que proporciona un espacio adecuado entre los elementos del login y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio.
        
        btn_login = tk.Button(panel_login, text="INGRESAR", bg=self.c_accent_blue, fg="white", font=("Arial", 11, "bold"), # Botón para iniciar sesión en la pantalla de inicio de sesión, lo que permite al usuario acceder al sistema de manera segura y visualmente coherente con el diseño de la interfaz gráfica, mejorando la experiencia del usuario al interactuar con un entorno visualmente atractivo y profesional desde el inicio.
                              bd=0, width=22, command=self._verificar_login, cursor="hand2") # Configuración del botón de inicio de sesión con un diseño atractivo y una acción asociada para verificar las credenciales ingresadas, lo que mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio, además de proporcionar una interacción clara y directa para acceder al sistema.
        btn_login.pack(ipady=6) # Configuración del botón de inicio de sesión con un padding interno vertical, lo que proporciona un diseño más atractivo y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio.
        
        self.root.bind("<Return>", lambda event: self._verificar_login()) # Configuración para que la tecla Enter también active el inicio de sesión, lo que proporciona una experiencia de usuario más fluida y eficiente al permitir una interacción rápida con el sistema desde la pantalla de inicio de sesión, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio.

    def _verificar_login(self): # Método para verificar las credenciales ingresadas en la pantalla de inicio de sesión, que compara el usuario y la contraseña con valores predefinidos (en este caso, "admin" para ambos), y si son correctos, destruye el panel de login y construye la interfaz principal del sistema; si son incorrectos, registra un error de acceso y muestra un mensaje de error al usuario, lo que proporciona una experiencia visual para acceder al sistema de manera segura y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio.
        usuario = self.ent_usuario.get()
        password = self.ent_password.get()
        
        if usuario == "admin" and password == "admin": # Verificación de credenciales para el inicio de sesión, lo que permite controlar el acceso al sistema de manera segura y proporciona una experiencia visual para acceder al sistema desde la pantalla de inicio de sesión, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional desde el inicio.
            self.root.unbind("<Return>")
            self.frame_login.destroy()
            self._construir_interfaz()
        else:
            self.sistema.registrar_error_usuario(f"Intento de acceso fallido. Usuario digitado: '{usuario}'")
            messagebox.showerror("Error de acceso", "Usuario o contraseña incorrectos.")

    def _construir_interfaz(self): # Método para construir la interfaz principal del sistema después de un inicio de sesión exitoso, que crea una barra lateral con opciones de navegación y un área central para mostrar el contenido principal, lo que proporciona una experiencia visual organizada y coherente para interactuar con las diferentes funcionalidades del sistema, mejorando la experiencia del usuario al ofrecer una interfaz atractiva y fácil de usar para gestionar clientes, servicios y reservas dentro del sistema.
        # 1. SIDEBAR
        sidebar = tk.Frame(self.root, bg=self.c_bg_sidebar, width=220)
        sidebar.pack(side="left", fill="y")

        try: # Intento de cargar el logo de la empresa para mostrarlo en la barra lateral, lo que proporciona una experiencia visual más atractiva y profesional al incluir elementos gráficos relacionados con la identidad de la empresa en la interfaz gráfica del sistema.
            img_raw = Image.open("logo_fj_tech.png")
            img_res = img_raw.resize((160, 90), Image.LANCZOS)
            self.img_logo = ImageTk.PhotoImage(img_res)
            tk.Label(sidebar, image=self.img_logo, bg=self.c_bg_sidebar).pack(pady=20)
        except:
            try: # Intento de cargar un logo alternativo para mostrarlo en la barra lateral si el logo principal no se encuentra, lo que proporciona una experiencia visual más atractiva y profesional al incluir elementos gráficos relacionados con la identidad de la empresa en la interfaz gráfica del sistema, incluso si el logo principal no está disponible.
                img_raw = Image.open("logo_fj.png")
                img_res = img_raw.resize((160, 90), Image.LANCZOS)
                self.img_logo = ImageTk.PhotoImage(img_res)
                tk.Label(sidebar, image=self.img_logo, bg=self.c_bg_sidebar).pack(pady=20)
            except: # Si no se encuentra ningún logo, muestra el nombre de la empresa como texto en la barra lateral, lo que proporciona una experiencia visual coherente y profesional al incluir la identidad de la empresa en la interfaz gráfica del sistema, incluso si los elementos gráficos no están disponibles.
                tk.Label(sidebar, text="FJ TECHNOLOGY", fg=self.c_accent_blue, bg=self.c_bg_sidebar, font=("Arial", 14, "bold")).pack(pady=40)

        # Botones del menú
        for btn_txt in ["Inicio", "Clientes", "Servicios", "Reservas", "Reportes"]: # Iteración para crear los botones de navegación en la barra lateral, lo que proporciona una experiencia visual organizada y coherente para interactuar con las diferentes funcionalidades del sistema, mejorando la experiencia del usuario al ofrecer una interfaz atractiva y fácil de usar para gestionar clientes, servicios, reservas y reportes dentro del sistema.
            bg_c = self.c_bg_panel if btn_txt == "Inicio" else self.c_bg_sidebar
            cmd = None
            if btn_txt == "Clientes": cmd = self.abrir_lista_clientes
            elif btn_txt == "Servicios": cmd = self.abrir_config_servicios
            elif btn_txt == "Reportes": cmd = self.abrir_reporte_errores
                
            tk.Button(sidebar, text=f"  {btn_txt}", bg=bg_c, fg="white", font=("Arial", 11), # Creación de un botón para cada opción del menú en la barra lateral, lo que proporciona una experiencia visual organizada y coherente para interactuar con las diferentes funcionalidades del sistema, mejorando la experiencia del usuario al ofrecer una interfaz atractiva y fácil de usar para gestionar clientes, servicios, reservas y reportes dentro del sistema.
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
        
        self.campos_reg = {} # Diccionario para almacenar las referencias a los campos de entrada del formulario de registro, lo que permite acceder fácilmente a los valores ingresados por el usuario al momento de guardar un nuevo cliente, mejorando la eficiencia en la gestión de datos dentro del sistema y facilitando la integración entre la interfaz gráfica y la lógica del negocio para el proceso de registro de clientes.
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
        
        tk.Label(col_der, text="Vincular Cliente (Documento):", bg=self.c_bg_panel, fg="#8892B0").pack(anchor="w", padx=15) # Etiqueta para el campo de vinculación de cliente en la sección de servicios, lo que proporciona una guía clara para el usuario sobre la acción que debe realizar para vincular un cliente a la sesión actual, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema.
        frame_vinc = tk.Frame(col_der, bg=self.c_bg_panel)
        frame_vinc.pack(fill="x", padx=15)
        self.ent_vinc_doc = tk.Entry(frame_vinc, width=20, bg="#0B1426", fg="white")
        self.ent_vinc_doc.pack(side="left", pady=5)
        tk.Button(frame_vinc, text="Vincular", command=self.evento_vincular).pack(side="left", padx=10)
        
        self.lbl_vinc_nom = tk.Label(col_der, text="Esperando cliente...", fg=self.c_accent_green, bg=self.c_bg_panel, font=("Arial", 9, "italic")) # Etiqueta para mostrar el nombre del cliente vinculado en la sección de servicios, lo que proporciona una retroalimentación visual clara al usuario sobre el cliente que está actualmente vinculado a la sesión, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema.
        self.lbl_vinc_nom.pack(anchor="w", padx=15)

        tk.Label(col_der, text="Servicio:", bg=self.c_bg_panel, fg="#8892B0").pack(anchor="w", padx=15, pady=(15,0)) # Etiqueta para el campo de selección de servicio en la sección de servicios, lo que proporciona una guía clara para el usuario sobre la acción que debe realizar para seleccionar un servicio del catálogo, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema.
        
        # Mapea los nombres de los objetos Servicio al ComboBox
        nombres_servicios = [s.nombre for s in self.sistema._servicios_catalogo]
        self.cb_servs = ttk.Combobox(col_der, values=nombres_servicios, state="readonly", width=42)
        self.cb_servs.pack(padx=15, pady=5)

        tk.Button(col_der, text="➕ Agregar Servicio", bg=self.c_bg_sidebar, fg="white", command=self.evento_agregar_serv).pack(pady=10) # Botón para agregar un servicio seleccionado a la lista de servicios vinculados, lo que permite al usuario construir una reserva con múltiples servicios y proporciona una experiencia visual para gestionar los servicios asociados a la sesión actual, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema.

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

        # --- FOOTER INTERACTIVO --- # 
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
    def abrir_lista_clientes(self): # Método para abrir una ventana emergente que muestra la lista de clientes registrados en el sistema, lo que proporciona una experiencia visual para consultar la información de los clientes y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema.
        ventana = tk.Toplevel(self.root)
        ventana.title("Base de Datos de Clientes")
        ventana.geometry("600x400")
        ventana.configure(bg=self.c_bg_panel)
        ventana.transient(self.root)
        ventana.focus_set()
        
        tk.Label(ventana, text="LISTA DE CLIENTES REGISTRADOS", bg=self.c_bg_panel, fg="white", font=("Arial", 12, "bold")).pack(pady=10) # Etiqueta para el título de la ventana emergente de lista de clientes, lo que proporciona una identificación clara del contenido de la ventana y mejora la experiencia del usuario al saber qué información se está mostrando, además de contribuir a la estética visual de la interfaz gráfica.
        
        tabla = ttk.Treeview(ventana, columns=("Nombre", "Doc"), show="headings")
        tabla.heading("Nombre", text="Nombre del Cliente")
        tabla.heading("Doc", text="Número de Documento")
        tabla.pack(fill="both", expand=True, padx=20, pady=10)

        for c in self.sistema._clientes:
            tabla.insert("", tk.END, values=(c.nombre, c.num_doc))

    def abrir_config_servicios(self): # Método para abrir una ventana emergente que permite configurar los servicios disponibles en el sistema, lo que proporciona una experiencia visual para gestionar el catálogo de servicios y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de permitir la adición de nuevos servicios de manera dinámica.
        ventana = tk.Toplevel(self.root)
        ventana.title("Configuración de Servicios")
        ventana.geometry("400x300")
        ventana.configure(bg=self.c_bg_panel)
        ventana.transient(self.root)
        ventana.focus_set()

        tk.Label(ventana, text="CREAR NUEVA ASESORIA", bg=self.c_bg_panel, fg="white", font=("Arial", 11, "bold")).pack(pady=20) # Etiqueta para el título de la sección de creación de nuevos servicios en la ventana emergente de configuración de servicios, lo que proporciona una identificación clara del propósito de la sección y mejora la experiencia del usuario al saber qué acción se está realizando, además de contribuir a la estética visual de la interfaz gráfica.
        
        tk.Label(ventana, text="Nombre del Servicio:", bg=self.c_bg_panel, fg="white").pack() # Etiqueta para el campo de nombre del servicio en la sección de creación de nuevos servicios, lo que proporciona una guía clara para el usuario sobre la información que debe ingresar para crear un nuevo servicio, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema.
        e_nom = tk.Entry(ventana, width=30)
        e_nom.pack(pady=5)

        tk.Label(ventana, text="Costo ($):", bg=self.c_bg_panel, fg="white").pack() # Etiqueta para el campo de costo del servicio en la sección de creación de nuevos servicios, lo que proporciona una guía clara para el usuario sobre la información que debe ingresar para crear un nuevo servicio, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema.
        e_cos = tk.Entry(ventana, width=30)
        e_cos.pack(pady=5)

        def guardar_s(): # Función para guardar un nuevo servicio en el catálogo, que toma los valores ingresados para el nombre y el costo del servicio, valida la información y, si es correcta, crea un nuevo objeto de tipo AsesoriaEspecializada (por polimorfismo) y lo agrega al catálogo de servicios del sistema, actualizando el ComboBox de servicios disponibles; si la información es incorrecta, registra un error de usuario y muestra un mensaje de error, lo que proporciona una experiencia visual para gestionar el catálogo de servicios y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema.
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

        tk.Button(ventana, text="Añadir Servicio", bg=self.c_accent_green, fg="white", command=guardar_s).pack(pady=20) # Botón para guardar un nuevo servicio en la ventana emergente de configuración de servicios, lo que proporciona una experiencia visual para gestionar el catálogo de servicios y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de permitir la adición de nuevos servicios de manera dinámica.

    def abrir_reporte_errores(self): # Método para abrir una ventana emergente que muestra un reporte de errores operativos relacionados con las acciones del usuario, lo que proporciona una experiencia visual para consultar los errores registrados en el sistema y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer transparencia sobre las incidencias ocurridas durante la interacción con el sistema.
        ventana = tk.Toplevel(self.root)
        ventana.title("Auditoría - Reporte de Errores Operativos")
        ventana.geometry("650x400")
        ventana.configure(bg=self.c_bg_panel)
        ventana.transient(self.root)
        ventana.focus_set()

        tk.Label(ventana, text="🚨 REPORTE DE ERRORES DE USUARIO", bg=self.c_bg_panel, fg="white", font=("Arial", 12, "bold")).pack(pady=15)
        
        frame_tabla = tk.Frame(ventana, bg=self.c_bg_panel) # Creación de un marco para contener la tabla de errores en la ventana emergente de reporte de errores, lo que permite organizar los elementos de la tabla de manera estructurada y visualmente atractiva dentro de la interfaz gráfica, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema.
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrolly = ttk.Scrollbar(frame_tabla, orient="vertical") # Creación de un scrollbar vertical para la tabla de errores en la ventana emergente de reporte de errores, lo que proporciona una experiencia visual para navegar por la lista de errores registrados y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, especialmente cuando hay una gran cantidad de errores registrados.
        scrolly.pack(side="right", fill="y")
        
        tabla = ttk.Treeview(frame_tabla, columns=("Fecha", "Detalle"), show="headings", yscrollcommand=scrolly.set) # Creación de una tabla para mostrar los errores registrados en la ventana emergente de reporte de errores, lo que proporciona una experiencia visual organizada y coherente para consultar la información de los errores y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer transparencia sobre las incidencias ocurridas durante la interacción con el sistema.
        scrolly.config(command=tabla.yview)
        
        tabla.heading("Fecha", text="Fecha / Hora") # Configuración de la cabecera de la columna "Fecha" en la tabla de errores, lo que proporciona una experiencia visual clara para identificar la fecha y hora de cada error registrado.
        tabla.heading("Detalle", text="Descripción de la Incidencia / Error") # Configuración de la cabecera de la columna "Detalle" en la tabla de errores, lo que proporciona una experiencia visual clara para identificar la descripción de cada error registrado.
        tabla.column("Fecha", width=160, anchor="center") # Configuración de la columna "Fecha" en la tabla de errores, lo que proporciona una experiencia visual clara y organizada para mostrar la fecha y hora de cada error registrado, mejorando la legibilidad de la información presentada.
        tabla.column("Detalle", width=450, anchor="w") # Configuración de la columna "Detalle" en la tabla de errores, lo que proporciona una experiencia visual clara y organizada para mostrar la descripción de cada error registrado, mejorando la legibilidad de la información presentada.
        tabla.pack(side="left", fill="both", expand=True) # Configuración de la tabla de errores para que ocupe el espacio disponible en el marco, lo que proporciona una experiencia visual organizada y coherente para consultar la información de los errores registrados y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer transparencia sobre las incidencias ocurridas durante la interacción con el sistema.

        if not self.sistema._historial_errores_usuario: # Verificación de si no hay errores registrados en el sistema, lo que proporciona una experiencia visual clara para el usuario al mostrar un mensaje indicando que no se han detectado errores, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer transparencia sobre las incidencias ocurridas durante la interacción con el sistema.
            tabla.insert("", tk.END, values=("N/A", "No se han detectado errores. (Ignorar simulaciones internas)"))
        else:
            for error in self.sistema._historial_errores_usuario:
                tabla.insert("", tk.END, values=error)

    # ==========================================
    # LÓGICA DE PROCESOS (Con POO conectada)
    # ==========================================
    def evento_cerrar_sesion(self): # Método para manejar el evento de cerrar sesión, que muestra un mensaje de confirmación al usuario y, si confirma, destruye la ventana principal del sistema, lo que proporciona una experiencia visual para gestionar la sesión del usuario y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer una interacción clara para finalizar la sesión de manera segura.
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea salir del sistema?"):
            self.root.destroy()

    def evento_limpiar(self): # Método para manejar el evento de limpiar la sesión actual, que restablece todos los campos de entrada, desvincula al cliente actual, limpia la lista de reservas y actualiza la interfaz gráfica para reflejar el estado limpio, lo que proporciona una experiencia visual para gestionar la sesión del usuario y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer una interacción clara para reiniciar la sesión de manera segura.
        self.ent_busc_doc.delete(0, tk.END)
        for e in self.campos_reg.values(): e.delete(0, tk.END)
        self.ent_vinc_doc.delete(0, tk.END)
        self.lbl_vinc_nom.config(text="Esperando cliente...")
        self.cliente_vinculado = None
        self.lista_reservas_actual.clear()
        self.cb_servs.set('')
        self.list_items.delete(0, tk.END)
        self.lbl_total.config(text="TOTAL: $ 0")

    def evento_liquidar(self): # Método para manejar el evento de generar una liquidación, que verifica que un cliente esté vinculado y que haya servicios agregados, luego genera un resumen de la liquidación con los detalles del cliente y los servicios contratados, mostrando el resultado en un mensaje informativo; si no se cumplen las condiciones necesarias, registra un error de usuario y muestra un mensaje de advertencia, lo que proporciona una experiencia visual para gestionar la generación de liquidaciones y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer una interacción clara para generar liquidaciones de manera segura.
        if not self.cliente_vinculado:
            self.sistema.registrar_error_usuario("Intento de liquidación fallido: No se vinculó ningún cliente.")
            messagebox.showwarning("Atención", "Debe vincular a un cliente antes de liquidar.")
            return
            
        if not self.lista_reservas_actual: # Verificación de que la lista de reservas actual no esté vacía antes de generar la liquidación, lo que proporciona una experiencia visual clara para el usuario al mostrar un mensaje de advertencia si no se han agregado servicios a la reserva, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer una interacción clara para gestionar la generación de liquidaciones de manera segura.
            self.sistema.registrar_error_usuario("Intento de liquidación fallido: Lista de servicios vacía.")
            messagebox.showwarning("Atención", "Debe agregar al menos un servicio para liquidar.")
            return

        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M") # Obtención de la fecha y hora actual para incluirla en el resumen de la liquidación, lo que proporciona una experiencia visual clara para el usuario al mostrar cuándo se generó la liquidación, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer información relevante sobre el momento de la transacción.
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
            
        resumen += f"------------------------------------\n" # Línea divisoria antes del total, lo que proporciona una experiencia visual clara para separar los detalles de los servicios contratados del resumen final de la liquidación, mejorando la legibilidad y organización de la información presentada en el resumen de la liquidación, además de contribuir a la estética visual de la interfaz gráfica.
        resumen += f"   {self.lbl_total.cget('text')}\n"
        resumen += f"====================================\n" # Línea divisoria final del resumen de la liquidación, lo que proporciona una experiencia visual clara para cerrar el resumen de la liquidación, mejorando la legibilidad y organización de la información presentada en el resumen de la liquidación, además de contribuir a la estética visual de la interfaz gráfica.
        
        messagebox.showinfo("Liquidación Generada Correctamente", resumen)  # Muestra el resumen de la liquidación generada en un mensaje informativo, lo que proporciona una experiencia visual clara para el usuario al mostrar los detalles de la liquidación, mejorando la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer una interacción clara para gestionar la generación de liquidaciones de manera segura.

    def evento_consultar(self): # Método para manejar el evento de consultar un cliente por su número de documento...
        doc = self.ent_busc_doc.get().strip() # Obtención del número de documento ingresado en el campo de búsqueda, lo que proporciona una experiencia visual para gestionar la consulta de clientes y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer una interacción clara para consultar clientes de manera eficiente.
        cli = self.sistema.buscar_cliente(doc)
        if cli:
            self.campos_reg["Nombre completo"].delete(0, tk.END)
            self.campos_reg["Nombre completo"].insert(0, cli.nombre)
            self.campos_reg["Teléfono celular"].delete(0, tk.END)
            self.campos_reg["Teléfono celular"].insert(0, cli.telefono)
            
            self.campos_reg["Correo electrónico"].delete(0, tk.END)
            self.campos_reg["Correo electrónico"].insert(0, cli.correo)
                       
            self.campos_reg["No. de Documento"].delete(0, tk.END)
            self.campos_reg["No. de Documento"].insert(0, cli.num_doc)
            messagebox.showinfo("Consulta", "Cliente cargado en formulario.")
        else: 
            self.sistema.registrar_error_usuario(f"Consulta de documento inexistente: '{doc}'")
            messagebox.showwarning("Atención", "Cliente no registrado.")            

    def evento_guardar(self): # Método para manejar el evento de guardar un nuevo cliente, que toma los valores ingresados en los campos del formulario de registro, valida la información y, si es correcta, registra un nuevo cliente en el sistema; si la información es incorrecta o faltan campos obligatorios, registra un error de usuario y muestra un mensaje de error, lo que proporciona una experiencia visual para gestionar el registro de clientes y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer una interacción clara para registrar clientes de manera eficiente.
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

    def evento_vincular(self): # Método para manejar el evento de vincular un cliente, que toma el valor ingresado en el campo de vinculación, busca el cliente en el sistema y, si lo encuentra, lo vincula al formulario; si no lo encuentra, registra un error de usuario y muestra un mensaje de error, lo que proporciona una experiencia visual para gestionar la vinculación de clientes y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer una interacción clara para vincular clientes de manera eficiente.
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

    def evento_agregar_serv(self): # Método para manejar el evento de agregar un servicio a la reserva actual, que verifica que un cliente esté vinculado, toma el servicio seleccionado en el ComboBox, busca el objeto de servicio correspondiente en el catálogo, crea una nueva reserva conectando al cliente y al servicio, calcula el costo de la reserva y actualiza la lista de servicios agregados y el total; si no se cumple la condición de tener un cliente vinculado o si no se selecciona un servicio, registra un error de usuario y muestra un mensaje de advertencia, lo que proporciona una experiencia visual para gestionar la adición de servicios a la reserva y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer una interacción clara para agregar servicios de manera eficiente.
        if not self.cliente_vinculado:
            messagebox.showwarning("Atención", "Vincule un cliente primero.")
            return

        nombre_serv = self.cb_servs.get() # Obtención del nombre del servicio seleccionado en el ComboBox, lo que proporciona una experiencia visual para gestionar la selección de servicios y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema, además de ofrecer una interacción clara para seleccionar servicios de manera eficiente.
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
if __name__ == "__main__": # Punto de entrada del programa, que crea una instancia del sistema de gestión, inicializa la interfaz gráfica y comienza el bucle principal de la aplicación, lo que proporciona una experiencia visual para iniciar el sistema y mejora la experiencia del usuario al interactuar con un entorno visualmente coherente y profesional dentro del sistema.
    motor = SistemaFJ()
    root = tk.Tk()
    app = AppDashboardFJ(root, motor)
    root.mainloop()