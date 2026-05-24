import tkinter as tk # Importamos tkinter para la interfaz gráfica
from tkinter import ttk, messagebox, simpledialog # ttk para combobox, messagebox para diálogos, simpledialog para pedir cantidad

# ==========================================
# BASE
# ==========================================
class TechProduct: # Clase base para productos tecnológicos
    def __init__(self, reference, brand, price, description, warranty, stock=0): # Inicializamos con referencia, marca, precio, descripción, garantía y stock
        self.reference = reference # Tipo o referencia del producto (ej: "Laptop Corporativa", "Router Layer 3", etc.)
        self.brand = brand # Marca del producto (ej: "Lenovo", "Cisco", etc.)
        self.price = float(price) # Precio del producto, convertido a float
        self.description = description # Descripción del producto
        self.warranty = warranty # Garantía del producto (ej: "3 años", "N/A", etc.)
        self.stock = stock # Cantidad en stock del producto

    def calculate_discount(self, d=0): # Calcula el precio con descuento, d es el porcentaje de descuento   
        return self.price * (1 - d/100) #   Retorna el precio con descuento aplicado (ej: si d=10, retorna el 90% del precio original)

# ==========================================
# PRODUCTOS
# ==========================================
class Laptop(TechProduct): # Clase para laptops, hereda de TechProduct
    def __init__(self, tipo, brand, price, desc, warranty, stock): # Inicializa con tipo (Corporativa o Consumo), marca, precio, descripción, garantía y stock
        super().__init__(tipo, brand, price, desc, warranty, stock) # Llama al constructor de la clase base para inicializar los atributos comunes

    def get_details(self): # Retorna una cadena con los detalles de la laptop para mostrar en la interfaz
        return f"[Laptop] {self.brand} ({self.reference}) - ${self.price} | Stock: {self.stock}" # Ejemplo: "[Laptop] Lenovo (Corporativa) - $1200 | Stock: 5"

class NetworkEquipment(TechProduct): # Clase para equipos de red, hereda de TechProduct
    def __init__(self, tipo, brand, clase, poe, ports, price, desc, stock): # Inicializa con tipo (Router o Switch), marca, clase (Layer 1, 2 o 3), si tiene PoE, cantidad de puertos, precio, descripción y stock
        super().__init__(tipo, brand, price, desc, "N/A", stock) # Llama al constructor de la clase base para inicializar los atributos comunes, con garantía "N/A" ya que no aplica para equipos de red
        self.clase = clase # Clase del equipo de red (ej: "Layer 3")
        self.poe = poe # Si tiene PoE (Power over Ethernet), "Sí" o "No"
        self.ports = ports # Cantidad de puertos del equipo de red (ej: "24")

    def get_details(self): # Retorna una cadena con los detalles del equipo de red para mostrar en la interfaz
        return f"[Network] {self.brand} {self.reference} - {self.clase} - {self.ports}p | Stock: {self.stock}" # Ejemplo: "[Network] Cisco Router - Layer 3 - 24p | Stock: 3"

class Accessory(TechProduct): # Clase para accesorios, hereda de TechProduct
    def __init__(self, tipo, brand, desc, price, stock): # Inicializa con tipo (Mouse, Keyboard o Combo), marca, descripción, precio y stock
        super().__init__(tipo, brand, price, desc, "N/A", stock) # Llama al constructor de la clase base para inicializar los atributos comunes, con garantía "N/A" ya que no aplica para accesorios

    def get_details(self): # Retorna una cadena con los detalles del accesorio para mostrar en la interfaz
        return f"[Accessory] {self.brand} {self.reference} | Stock: {self.stock}" # Ejemplo: "[Accessory] Logitech Mouse | Stock: 10"

# ==========================================
# CARRITO
# ==========================================
class Cart: # Clase para el carrito de compras, que maneja los productos seleccionados por el cliente
    def __init__(self): # Inicializa el carrito con una lista vacía de items
        self.items = [] # Cada item es un diccionario con la clave "p" para el producto y "q" para la cantidad (ej: {"p": laptop1, "q": 2})  

    def add(self, p, qty): # Agrega un producto al carrito con la cantidad especificada, si hay suficiente stock
        if p.stock >= qty: # Verifica si el stock del producto es suficiente para la cantidad solicitada
            self.items.append({"p": p, "q": qty}) # Agrega un nuevo item al carrito con el producto y la cantidad
            p.stock -= qty # Reduce el stock del producto en la cantidad agregada al carrito
        else:
            raise ValueError # Si no hay suficiente stock, lanza una excepción para indicar el error

    def total(self, discount=0): # Calcula el total del carrito aplicando un descuento opcional, que es un porcentaje (ej: 10 para 10% de descuento)
        return sum(i["p"].calculate_discount(discount)*i["q"] for i in self.items) # Retorna la suma del precio con descuento de cada producto multiplicado por su cantidad en el carrito

    def details(self): # Retorna una lista de cadenas con los detalles de cada item en el carrito para mostrar en la factura
        return [f"{i['p'].brand} {i['p'].reference} x{i['q']} - ${i['p'].price*i['q']}" for i in self.items] # Ejemplo: ["Lenovo Corporativa x2 - $2400", "Cisco Router x1 - $500"]

    def clear(self): # Limpia el carrito, vaciando la lista de items
        self.items.clear() # Elimina todos los items del carrito, dejándolo vacío para una nueva compra

# ==========================================
# INVENTARIO
# ==========================================
class InventoryWindow: # Clase para la ventana de inventario, que permite agregar nuevos productos a la tienda
    def __init__(self, root, app): # Inicializa la ventana de inventario con una referencia a la aplicación principal para agregar productos a la lista
        self.app = app # Guarda la referencia a la aplicación principal para poder llamar al método add_product cuando se guarde un nuevo producto
        self.win = tk.Toplevel(root) # Crea una nueva ventana secundaria (Toplevel) para el inventario, con el root como padre
        self.win.title("Agregar Producto") # Establece el título de la ventana de inventario
        self.win.geometry("400x500") # Establece el tamaño de la ventana de inventario

        tk.Label(self.win, text="Tipo Producto").pack() # Agrega una etiqueta para indicar que se debe seleccionar el tipo de producto
        self.type_cb = ttk.Combobox(self.win, values=("Laptop","Network Equipment","Accessory")) # Agrega un Combobox para seleccionar el tipo de producto, con las opciones "Laptop", "Network Equipment" y "Accessory"
        self.type_cb.pack() # Empaqueta el Combobox en la ventana de inventario
        self.type_cb.bind("<<ComboboxSelected>>", self.update_form) # Vincula el evento de selección del Combobox a la función update_form, que actualizará el formulario de acuerdo al tipo de producto seleccionado

        self.form = tk.Frame(self.win) # Crea un Frame para contener los campos del formulario, que se actualizarán dinámicamente según el tipo de producto seleccionado
        self.form.pack(pady=10) # Empaqueta el Frame del formulario con un margen vertical de 10 píxeles

        tk.Button(self.win, text="Guardar", bg="green", fg="white", command=self.save).pack(pady=10) # Agrega un botón para guardar el nuevo producto, que llamará a la función save cuando se haga clic, con un margen vertical de 10 píxeles

    def clear_form(self): # Función para limpiar el formulario, eliminando todos los widgets hijos del Frame del formulario
        for w in self.form.winfo_children(): # Itera sobre todos los widgets hijos del Frame del formulario
            w.destroy() # Elimina cada widget hijo, dejando el Frame vacío para agregar los nuevos campos según el tipo de producto seleccionado

    def update_form(self, e): # Función para actualizar el formulario según el tipo de producto seleccionado en el Combobox, recibe un evento (e) que no se utiliza en esta función
        self.clear_form() # Limpia el formulario antes de agregar los nuevos campos correspondientes al tipo de producto seleccionado
        t = self.type_cb.get() # Obtiene el tipo de producto seleccionado en el Combobox, que puede ser "Laptop", "Network Equipment" o "Accessory"

        if t == "Laptop": # Si el tipo de producto es "Laptop", agrega los campos específicos para laptops al formulario
            self.tipo = self.field("Tipo", ("Corporativa","Consumo")) # Agrega un campo de selección para el tipo de laptop, con las opciones "Corporativa" y "Consumo"
            self.brand = self.field("Marca", ("Lenovo","HP","Asus")) # Agrega un campo de selección para la marca de la laptop, con las opciones "Lenovo", "HP" y "Asus"
            self.desc = self.entry("Descripción") # Agrega un campo de entrada para la descripción de la laptop, que es un texto libre
            self.price = self.entry("Precio") # Agrega un campo de entrada para el precio de la laptop, que debe ser un número
            self.warranty = self.field("Garantía", ("1 año","18 meses","3 años corp","3 años onsite")) # Agrega un campo de selección para la garantía de la laptop, con las opciones "1 año", "18 meses", "3 años corp" y "3 años onsite"
            self.stock = self.entry("Stock") # Agrega un campo de entrada para el stock de la laptop, que debe ser un número entero

        elif t == "Network Equipment": # Si el tipo de producto es "Network Equipment", agrega los campos específicos para equipos de red al formulario
            self.tipo = self.field("Tipo", ("Router","Switch")) # Agrega un campo de selección para el tipo de equipo de red, con las opciones "Router" y "Switch"
            self.brand = self.field("Marca", ("HP","Cisco","Mercury","TP-Link")) # Agrega un campo de selección para la marca del equipo de red, con las opciones "HP", "Cisco", "Mercury" y "TP-Link"
            self.clase = self.field("Clase", ("Router modem","Layer 1","Layer 2","Layer 3")) # Agrega un campo de selección para la clase del equipo de red, con las opciones "Router modem", "Layer 1", "Layer 2" y "Layer 3"
            self.poe = self.field("PPoE", ("Sí","No")) # Agrega un campo de selección para indicar si el equipo de red tiene PoE (Power over Ethernet), con las opciones "Sí" y "No"
            self.ports = self.field("Puertos", ("5","8","24","48")) # Agrega un campo de selección para la cantidad de puertos del equipo de red, con las opciones "5", "8", "24" y "48"
            self.desc = self.entry("Descripción") # Agrega un campo de entrada para la descripción del equipo de red, que es un texto libre
            self.price = self.entry("Precio") # Agrega un campo de entrada para el precio del equipo de red, que debe ser un número
            self.stock = self.entry("Stock") # Agrega un campo de entrada para el stock del equipo de red, que debe ser un número entero

        else: # Si el tipo de producto es "Accessory", agrega los campos específicos para accesorios al formulario
            self.tipo = self.field("Tipo", ("Mouse","Keyboard","Combo")) # Agrega un campo de selección para el tipo de accesorio, con las opciones "Mouse", "Keyboard" y "Combo"
            self.brand = self.field("Marca", ("Logitech","Genius","Trust")) # Agrega un campo de selección para la marca del accesorio, con las opciones "Logitech", "Genius" y "Trust"
            self.desc = self.entry("Descripción") # Agrega un campo de entrada para la descripción del accesorio, que es un texto libre
            self.price = self.entry("Precio") # Agrega un campo de entrada para el precio del accesorio, que debe ser un número
            self.stock = self.entry("Stock") # Agrega un campo de entrada para el stock del accesorio, que debe ser un número entero

    def field(self, label, values): # Función para agregar un campo de selección (Combobox) al formulario, recibe una etiqueta (label) y una lista de valores (values) para el Combobox
        tk.Label(self.form, text=label).pack() # Agrega una etiqueta para el campo de selección, con el texto proporcionado en label
        cb = ttk.Combobox(self.form, values=values) # Crea un Combobox con las opciones proporcionadas en values, que es una lista de cadenas
        cb.pack() # Empaqueta el Combobox en el formulario
        return cb # Retorna el Combobox creado para que pueda ser accedido posteriormente para obtener el valor seleccionado

    def entry(self, label): # Función para agregar un campo de entrada (Entry) al formulario, recibe una etiqueta (label) para el campo
        tk.Label(self.form, text=label).pack() # Agrega una etiqueta para el campo de entrada, con el texto proporcionado en label
        e = tk.Entry(self.form) # Crea un campo de entrada (Entry) para que el usuario pueda escribir texto o números
        e.pack() # Empaqueta el campo de entrada en el formulario
        return e # Retorna el campo de entrada creado para que pueda ser accedido posteriormente para obtener el texto ingresado

    def save(self): # Función para guardar el nuevo producto creado en el formulario, que se llama cuando se hace clic en el botón "Guardar"
        try: # Intenta crear un nuevo producto según el tipo seleccionado y los datos ingresados en el formulario, y agregarlo a la aplicación principal
            t = self.type_cb.get() # Obtiene el tipo de producto seleccionado en el Combobox para determinar qué clase de producto crear (Laptop, NetworkEquipment o Accessory)

            if t == "Laptop": # Si el tipo de producto es "Laptop", crea una instancia de la clase Laptop con los datos ingresados en el formulario
                p = Laptop(self.tipo.get(), self.brand.get(), float(self.price.get()), # Convierte el precio a float, ya que el campo de entrada devuelve un string
                           self.desc.get(), self.warranty.get(), int(self.stock.get())) # Convierte el stock a entero, ya que el campo de entrada devuelve un string

            elif t == "Network Equipment": # Si el tipo de producto es "Network Equipment", crea una instancia de la clase NetworkEquipment con los datos ingresados en el formulario
                p = NetworkEquipment(self.tipo.get(), self.brand.get(), # Obtiene el tipo y la marca seleccionados en los Combobox correspondientes
                                     self.clase.get(), self.poe.get(), # Obtiene la clase y si tiene PoE seleccionados en los Combobox correspondientes
                                     self.ports.get(), float(self.price.get()), # Convierte el precio a float, ya que el campo de entrada devuelve un string
                                     self.desc.get(), int(self.stock.get())) # Convierte el stock a entero, ya que el campo de entrada devuelve un string
            else:
                p = Accessory(self.tipo.get(), self.brand.get(), # Obtiene el tipo y la marca seleccionados en los Combobox correspondientes
                              self.desc.get(), float(self.price.get()), # Convierte el precio a float, ya que el campo de entrada devuelve un string
                              int(self.stock.get())) # Convierte el stock a entero, ya que el campo de entrada devuelve un string

            self.app.add_product(p) # Llama al método add_product de la aplicación principal para agregar el nuevo producto creado a la lista de productos disponibles
            self.win.destroy() # Cierra la ventana de inventario después de guardar el nuevo producto
        except:
            messagebox.showerror("Error", "Datos inválidos") # Si ocurre un error al crear el producto (por ejemplo, si el precio o el stock no son números válidos), muestra un mensaje de error indicando que los datos son inválidos

# ==========================================
# APP
# ==========================================
class App: # Clase principal de la aplicación, que maneja la interfaz de la tienda, el carrito y la interacción con el usuario
    def __init__(self, root): # Inicializa la aplicación con la ventana principal (root) y configura la interfaz, el carrito y la lista de productos
        self.root = root # Guarda la referencia a la ventana principal para poder configurar su título, tamaño y agregar widgets
        self.root.title("Tech Store Pro") # Establece el título de la ventana principal de la aplicación
        self.root.geometry("950x550") # Establece el tamaño de la ventana principal de la aplicación

        self.cart = Cart() # Crea una instancia del carrito de compras para manejar los productos seleccionados por el cliente
        self.products = [] # Inicializa la lista de productos disponibles en la tienda, que se llenará con instancias de Laptop, NetworkEquipment y Accessory

        tk.Button(root, text="+ Agregar Producto", bg="orange", # Agrega un botón en la parte superior de la ventana principal para abrir la ventana de inventario y agregar nuevos productos, con un fondo naranja para destacarlo
                  command=lambda: InventoryWindow(root,self)).pack(pady=5) # El comando del botón crea una nueva instancia de InventoryWindow, pasando la ventana principal y la referencia a la aplicación para que pueda agregar productos a la lista

        main = tk.Frame(root) # Crea un Frame principal para contener las secciones de productos y carrito, que se dividirá en dos columnas (izquierda para productos y derecha para cliente y carrito)
        main.pack(fill=tk.BOTH, expand=True) # Empaqueta el Frame principal para que ocupe todo el espacio disponible en la ventana principal, permitiendo que se ajuste al tamaño de la ventana

        # IZQUIERDA PRODUCTOS
        self.left = tk.LabelFrame(main, text="Productos") # Crea un LabelFrame en la parte izquierda del Frame principal para mostrar la lista de productos disponibles, con el título "Productos"
        self.left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10) # Empaqueta el LabelFrame de productos en el lado izquierdo del Frame principal, permitiendo que ocupe todo el espacio disponible y agregando un margen horizontal de 10 píxeles

        # DERECHA
        self.right = tk.Frame(main) # Crea un Frame en la parte derecha del Frame principal para mostrar los datos del cliente y el carrito de compras
        self.right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10) # Empaqueta el Frame de la derecha en el lado derecho del Frame principal, permitiendo que ocupe todo el espacio disponible y agregando un margen horizontal de 10 píxeles

        # CLIENTE
        cliente_frame = tk.LabelFrame(self.right, text="Datos del Cliente") # Crea un LabelFrame dentro del Frame de la derecha para mostrar los campos de datos del cliente, con el título "Datos del Cliente"
        cliente_frame.pack(fill=tk.X) # Empaqueta el LabelFrame de datos del cliente para que ocupe todo el ancho disponible en el Frame de la derecha, pero no se expanda verticalmente

        tk.Label(cliente_frame, text="Nombre Completo").pack() # Agrega una etiqueta para el campo de nombre completo del cliente dentro del LabelFrame de datos del cliente
        self.name = tk.Entry(cliente_frame) # Agrega un campo de entrada para el nombre completo del cliente dentro del LabelFrame de datos del cliente, donde el usuario puede escribir su nombre
        self.name.pack() # Empaqueta el campo de entrada del nombre completo para que se muestre debajo de la etiqueta correspondiente

        tk.Label(cliente_frame, text="Cédula").pack() # Agrega una etiqueta para el campo de cédula del cliente dentro del LabelFrame de datos del cliente
        self.id = tk.Entry(cliente_frame) # Agrega un campo de entrada para la cédula del cliente dentro del LabelFrame de datos del cliente, donde el usuario puede escribir su cédula
        self.id.pack() # Empaqueta el campo de entrada de la cédula para que se muestre debajo de la etiqueta correspondiente

        tk.Label(cliente_frame, text="Teléfono").pack() # Agrega una etiqueta para el campo de teléfono del cliente dentro del LabelFrame de datos del cliente
        self.phone = tk.Entry(cliente_frame) # Agrega un campo de entrada para el teléfono del cliente dentro del LabelFrame de datos del cliente, donde el usuario puede escribir su número de teléfono
        self.phone.pack() # Empaqueta el campo de entrada del teléfono para que se muestre debajo de la etiqueta correspondiente

        # CARRITO
        cart_frame = tk.LabelFrame(self.right, text="Carrito") # Crea un LabelFrame dentro del Frame de la derecha para mostrar el carrito de compras, con el título "Carrito"
        cart_frame.pack(fill=tk.BOTH, expand=True) # Empaqueta el LabelFrame del carrito para que ocupe todo el espacio disponible en el Frame de la derecha, permitiendo que se expanda tanto horizontal como verticalmente

        self.cart_box = tk.Listbox(cart_frame) # Agrega un Listbox dentro del LabelFrame del carrito para mostrar los productos que el cliente ha agregado al carrito de compras, donde cada línea representará un producto con su cantidad y precio
        self.cart_box.pack(fill=tk.BOTH, expand=True) # Empaqueta el Listbox del carrito para que ocupe todo el espacio disponible dentro del LabelFrame del carrito, permitiendo que se expanda tanto horizontal como verticalmente

        tk.Label(cart_frame, text="Descuento (%)").pack() # Agrega una etiqueta para el campo de descuento dentro del LabelFrame del carrito, indicando que se debe ingresar un porcentaje de descuento
        self.discount = tk.Entry(cart_frame) # Agrega un campo de entrada para el descuento dentro del LabelFrame del carrito, donde el usuario puede escribir un porcentaje de descuento que se aplicará al total del carrito
        self.discount.insert(0,"0") # Inserta un valor predeterminado de "0" en el campo de descuento para indicar que no hay descuento aplicado inicialmente
        self.discount.pack() # Empaqueta el campo de entrada del descuento para que se muestre debajo de la etiqueta correspondiente

        self.total = tk.Label(cart_frame, text="Total: 0", fg="blue", font=("Arial",12,"bold")) # Crea una etiqueta para mostrar el total del carrito, con el texto "Total: 0", color azul y fuente en negrita
        self.total.pack() # Empaqueta la etiqueta del total para que se muestre debajo del campo de entrada del descuento

        tk.Button(cart_frame, text="Checkout", bg="green", fg="white", 
                  command=self.checkout).pack(pady=5) # Agrega un botón para realizar el checkout del carrito, que llamará a la función checkout cuando se haga clic, con un fondo verde para destacarlo y un margen vertical de 5 píxeles

        self.load() # Llama al método load para cargar algunos productos de ejemplo en la lista de productos disponibles al iniciar la aplicación, lo que permitirá probar la funcionalidad de agregar productos al carrito y realizar el checkout con productos predefinidos

    def load(self): # Método para cargar algunos productos de ejemplo en la lista de productos disponibles al iniciar la aplicación, creando instancias de Laptop y NetworkEquipment con datos predefinidos y agregándolos a la lista de productos mediante el método add_product
        self.add_product(Laptop("Corporativa","Lenovo",1200,"","3 años",5)) # Agrega un producto de ejemplo a la lista de productos disponibles, que es una laptop corporativa de la marca Lenovo, con un precio de 1200, sin descripción, garantía de 3 años y stock de 5 unidades
        self.add_product(NetworkEquipment("Router","Cisco","Layer 3","Sí","24",500,"",3)) # Agrega un producto de ejemplo a la lista de productos disponibles, que es un equipo de red tipo router de la marca Cisco, clase Layer 3, con PoE, 24 puertos, precio de 500, sin descripción y stock de 3 unidades

    def add_product(self,p): # Método para agregar un producto a la lista de productos disponibles
        self.products.append(p) # 
        self.refresh()

    def refresh(self): # Método para actualizar la sección de productos en la interfaz, limpiando los widgets actuales y creando nuevos botones para cada producto en la lista de productos disponibles, donde cada botón mostrará los detalles del producto y permitirá agregarlo al carrito al hacer clic
        for w in self.left.winfo_children(): # 
            w.destroy()

        for p in self.products: # Itera sobre cada producto en la lista de productos disponibles y crea un botón para cada uno, mostrando sus detalles y vinculando el comando para agregarlo al carrito cuando se haga clic
            tk.Button(self.left, text=p.get_details(), # Crea un botón para cada producto, utilizando el método get_details de cada producto para mostrar su información en el texto del botón
                      command=lambda prod=p:self.add_cart(prod)).pack(fill=tk.X,pady=2) # Vincula el comando del botón a una función lambda que llama al método add_cart con el producto correspondiente (prod=p) para agregarlo al carrito cuando se haga clic, y empaca el botón para que ocupe todo el ancho disponible y tenga un margen vertical de 2 píxeles entre cada botón

    def add_cart(self,p): # Método para agregar un producto al carrito de compras, que se llama cuando se hace clic en el botón de un producto en la sección de productos disponibles, y solicita al usuario la cantidad a agregar mediante un diálogo, verificando el stock disponible antes de agregarlo al carrito
        q = simpledialog.askinteger("Cantidad",f"Stock: {p.stock}") # Muestra un diálogo para solicitar al usuario la cantidad del producto que desea agregar al carrito, mostrando el stock disponible del producto en el mensaje del diálogo, y devuelve la cantidad ingresada como un número entero (o None si el usuario cancela el diálogo)
        if q:
            try:
                self.cart.add(p,q)
                self.update_cart()
                self.refresh()
            except:
                messagebox.showerror("Error","Sin stock")

    def update_cart(self): # Método para actualizar la sección del carrito en la interfaz, limpiando el Listbox del carrito y llenándolo con los detalles de cada producto agregado al carrito, y calculando el total del carrito aplicando el descuento ingresado por el usuario
        self.cart_box.delete(0,tk.END) # Limpia el Listbox del carrito para eliminar los productos anteriores y mostrar solo los productos actualmente en el carrito después de agregar o eliminar productos
        for d in self.cart.details(): # 
            self.cart_box.insert(tk.END,d) # Inserta cada detalle de producto en el Listbox del carrito, donde cada línea representará un producto con su cantidad y precio, utilizando el método details del carrito para obtener la lista de detalles de los productos agregados

        d = float(self.discount.get() or 0) # Obtiene el valor del descuento ingresado por el usuario en el campo de entrada del descuento, convirtiéndolo a float para poder aplicarlo al cálculo del total, y si el campo está vacío, utiliza 0 como valor predeterminado para indicar que no hay descuento aplicado
        total = self.cart.total(d) # Calcula el total del carrito aplicando el descuento ingresado por el usuario, utilizando el método total del carrito que recibe el porcentaje de descuento para calcular el precio con descuento de cada producto y sumarlos
        self.total.config(text=f"Total: {total:.2f}") # Actualiza el texto de la etiqueta del total para mostrar el nuevo total calculado del carrito, formateado con dos decimales para mostrar el precio correctamente

    def checkout(self): # Método para realizar el checkout del carrito de compras, que se llama cuando se hace clic en el botón "Checkout", y verifica que se hayan ingresado los datos del cliente antes de generar una factura con los detalles de la compra, aplicando el descuento ingresado y mostrando el total final, y luego limpia el carrito y actualiza la interfaz para una nueva compra
        if not self.name.get() or not self.id.get():
            messagebox.showwarning("Error","Ingrese datos del cliente")
            return

        d = float(self.discount.get() or 0) # Obtiene el valor del descuento ingresado por el usuario en el campo de entrada del descuento, convirtiéndolo a float para poder aplicarlo al cálculo del total, y si el campo está vacío, utiliza 0 como valor predeterminado para indicar que no hay descuento aplicado
        total = self.cart.total(d)

        factura = f"CLIENTE: {self.name.get()}\n" # Crea una cadena para la factura que incluirá los datos del cliente, los productos comprados, el descuento aplicado y el total final, comenzando con el nombre del cliente obtenido del campo de entrada del nombre
        factura += f"CÉDULA: {self.id.get()}\n" # Agrega la cédula del cliente a la factura, obtenida del campo de entrada de la cédula
        factura += f"TELÉFONO: {self.phone.get()}\n\n" # Agrega el teléfono del cliente a la factura, obtenido del campo de entrada del teléfono, y luego agrega una línea en blanco para separar los datos del cliente de los detalles de los productos comprados

        factura += "PRODUCTOS:\n" # Agrega un encabezado para la sección de productos en la factura, indicando que a continuación se mostrarán los productos comprados por el cliente
        for item in self.cart.details():
            factura += item + "\n"

        factura += f"\nDESCUENTO: {d}%" # Agrega el descuento aplicado a la factura, mostrando el porcentaje de descuento ingresado por el usuario
        factura += f"\nTOTAL: ${total:.2f}"

        messagebox.showinfo("Factura", factura) # Muestra un mensaje con la factura generada, utilizando un cuadro de diálogo de información para mostrar los detalles de la compra al cliente después de realizar el checkout

        self.cart.clear() # Limpia el carrito después de realizar el checkout, eliminando todos los productos agregados para preparar el carrito para una nueva compra
        self.update_cart() # Actualiza la sección del carrito en la interfaz para reflejar que el carrito está vacío después de realizar el checkout, mostrando un total de 0 y sin productos listados, listo para una nueva compra
        self.refresh() # Actualiza la sección de productos en la interfaz para reflejar los cambios en el stock de los productos después de realizar el checkout, ya que al agregar productos al carrito se reduce el stock disponible, y después del checkout se deben actualizar los botones de los productos para mostrar el nuevo stock disponible

# ==============================================================================================================================================================================================================================================
# LOGIN - MODULO DE LOGIN SIMPLIFICADO PARA ACCEDER A LA APLICACIÓN, CON USUARIO Y CONTRASEÑA PREDEFINIDOS (admin/admin), Y SI LAS CREDENCIALES SON CORRECTAS, SE INICIA LA APLICACIÓN PRINCIPAL, DE LO CONTRARIO SE MUESTRA UN MENSAJE DE ERROR
# ==============================================================================================================================================================================================================================================
def start(): # Función para iniciar la aplicación, mostrando una ventana de login simplificada que solicita un usuario y contraseña, y si las credenciales son correctas (admin/admin), se cierra la ventana de login y se inicia la aplicación principal, de lo contrario se muestra un mensaje de error indicando que las credenciales son incorrectas
    root = tk.Tk() # Crea una nueva ventana principal para el login, que se mostrará al iniciar la aplicación y solicitará las credenciales de acceso al usuario
    root.title("Login") # Establece el título de la ventana de login para indicar que es la pantalla de inicio de sesión
    root.geometry("300x200") # Establece el tamaño de la ventana de login

    tk.Label(root,text="Usuario").pack() # Agrega una etiqueta para el campo de usuario en la ventana de login, indicando que se debe ingresar el nombre de usuario para acceder a la aplicación
    u = tk.Entry(root) # Agrega un campo de entrada para el usuario en la ventana de login, donde el usuario puede escribir su nombre de usuario para acceder a la aplicación
    u.pack() # Empaqueta el campo de entrada del usuario para que se muestre debajo de la etiqueta correspondiente en la ventana de login

    tk.Label(root,text="Contraseña").pack() # Agrega una etiqueta para el campo de contraseña en la ventana de login, indicando que se debe ingresar la contraseña para acceder a la aplicación
    p = tk.Entry(root,show="*") # Agrega un campo de entrada para la contraseña en la ventana de login, donde el usuario puede escribir su contraseña para acceder a la aplicación, y utiliza el parámetro show="*" para ocultar los caracteres ingresados y mostrar asteriscos en su lugar por seguridad
    p.pack() # Empaqueta el campo de entrada de la contraseña para que se muestre debajo de la etiqueta correspondiente en la ventana de login

    def login(): # Función para verificar las credenciales ingresadas por el usuario en la ventana de login, que se llama cuando se hace clic en el botón "Login", y compara el usuario y contraseña ingresados con los valores predefinidos (admin/admin), y si son correctos, cierra la ventana de login y llama a la función main para iniciar la aplicación principal, de lo contrario muestra un mensaje de error indicando que las credenciales son incorrectas
        if u.get()=="admin" and p.get()=="admin": # Verifica si el usuario ingresado es "admin" y la contraseña ingresada es "admin", que son las credenciales predefinidas para acceder a la aplicación
            root.destroy() # Si las credenciales son correctas, cierra la ventana de login para que no quede abierta en segundo plano después de iniciar la aplicación principal
            main() # Llama a la función main para iniciar la aplicación principal después de cerrar la ventana de login, lo que permitirá al usuario acceder a la tienda y realizar compras después de iniciar sesión correctamente
        else:
            messagebox.showerror("Error","Credenciales incorrectas") # Si las credenciales ingresadas no son correctas, muestra un mensaje de error utilizando un cuadro de diálogo de error para indicar al usuario que las credenciales son incorrectas y que debe intentar nuevamente

    tk.Button(root,text="Login",command=login).pack() # Agrega un botón para realizar el login en la ventana de login, que llamará a la función login cuando se haga clic, con el texto "Login" para indicar su función al usuario
    root.mainloop()

def main(): # Función para iniciar la aplicación principal después de un login exitoso, que crea una nueva ventana principal y una instancia de la clase App para configurar la interfaz de la tienda y mostrar los productos disponibles, el carrito y los datos del cliente, permitiendo al usuario interactuar con la tienda después de iniciar sesión correctamente
    root = tk.Tk() # Crea una nueva ventana principal para la aplicación después de un login exitoso, que se mostrará al usuario para interactuar con la tienda y realizar compras después de iniciar sesión correctamente
    App(root) # Crea una instancia de la clase App, pasando la ventana principal como argumento para configurar la interfaz de la tienda, mostrar los productos disponibles, el carrito y los datos del cliente, y permitir al usuario interactuar con la tienda después de iniciar sesión correctamente
    root.mainloop() # Inicia el bucle principal de la ventana para mostrar la interfaz de la tienda y permitir al usuario interactuar con ella después de iniciar sesión correctamente

start() # Llama a la función start para iniciar la aplicación, mostrando la ventana de login para que el usuario ingrese sus credenciales y luego acceder a la tienda después de un login exitoso