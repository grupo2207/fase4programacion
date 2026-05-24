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