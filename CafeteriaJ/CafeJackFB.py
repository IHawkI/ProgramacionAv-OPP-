import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
class Producto: 
    def __init__(self, nombre, precio, stock, ingredientes):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.ingredientes = ingredientes

class Bebida(Producto):
    lista_bebidas = []
    def __init__(self, nombre, precio, stock, ingredientes):
        super().__init__(nombre, precio, stock, ingredientes)
        Bebida.lista_bebidas.append(self)

class Postre(Producto):
    lista_postres = []
    def __init__(self, nombre, precio, stock, ingredientes):
        super().__init__(nombre, precio, stock, ingredientes)
        Postre.lista_postres.append(self)

empleados = {
    "1234": {"nombre": "Juan Pérez", "contraseña": "admin123"},
    "5678": {"nombre": "Ana López", "contraseña": "CI4"},
    "9101": {"nombre": "Carlos Díaz", "contraseña": "13789"},
    "1121": {"nombre": "Elena Gómez", "contraseña": "clave321"},
    "3141": {"nombre": "David Ruiz", "contraseña": "Blabla654"}
}

ingredientes_stock = {
    "leche": 10,
    "azúcar": 10,
    "café": 10,
    "chocolate": 10,
    "harina": 10,
    "huevo": 10,
    "hielo": 10,
    "limón": 10,
}
pedidoact = []

def actualizar_pedido():
    texto_pedido = "Pedido:\n"
    total = 0
    for item in pedidoact:
        texto_pedido += f"- {item['producto'].nombre} ({item['personalizacion']}) - ${item['producto'].precio}\n"
        total += item['producto'].precio
    texto_pedido += f"\nTotal: ${total}"
    pedido_var.set(texto_pedido)

def agregar_producto(tipo):
    seleccion = listbox_bebidas.curselection() if tipo == "bebida" else listbox_postres.curselection()
    lista = Bebida.lista_bebidas if tipo == "bebida" else Postre.lista_postres
    if seleccion:
        producto = lista[seleccion[0]]
        if producto.stock <= 0:
            messagebox.showerror("Agotado", f"{producto.nombre} está agotado.")
            return
        tamaño = var_tamaño.get()
        leche = var_leche.get()
        azúcar = var_azúcar.get()
        personalizacion = f"{tamaño}, {leche}, {azúcar}"
        for ing in producto.ingredientes:
            if ingredientes_stock.get(ing, 0) <= 0:
                messagebox.showerror("Sin stock", f"No hay suficiente {ing} para preparar {producto.nombre}.")
                return
        for ing in producto.ingredientes:
            ingredientes_stock[ing] -= 1
        producto.stock -= 1
        pedidoact.append({"producto": producto, "personalizacion": personalizacion})
        actualizar_pedido()

def eliminar_item():
    if pedidoact:
        item = pedidoact.pop()
        item["producto"].stock += 1
        for ing in item["producto"].ingredientes:
            ingredientes_stock[ing] += 1
        actualizar_pedido()
def realizar_pedido():
    if pedidoact:
        mesa = entry_mesa.get()
        if mesa:
            pedido_data = {
                "mesa": mesa,
                "pedido": [{"producto": item["producto"].nombre, "personalizacion": item["personalizacion"]} for item in pedidoact]
            }
            with open("pedidos.json", "a") as f:
                json.dump(pedido_data, f, indent=4)
                f.write("\n") 
            messagebox.showinfo("Pedido realizado", f"¡Gracias por su pedido! Pedido guardado en mesa {mesa}.")
            pedidoact.clear()
            actualizar_pedido()
        else:
            messagebox.showerror("Error", "Debe ingresar un número de mesa.")
    else:
        messagebox.showerror("Error", "No hay productos en el pedido.")


def actualizar_stock():
    seleccion = listbox_stock.curselection()
    if seleccion:
        producto = lista_stock[seleccion[0]]
        try:
            cantidad = int(entry_stock.get())
            producto.stock += cantidad
            messagebox.showinfo("Actualizado", f"{producto.nombre} ahora tiene {producto.stock} unidades.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido.")

def admin():
    adminwindow = tk.Toplevel()
    adminwindow.title("Panel de administrador")
    adminwindow.geometry("300x400")
    tk.Label(adminwindow, text="Actualizar Stock").pack()
    global listbox_stock, entry_stock, lista_stock
    lista_stock = Bebida.lista_bebidas + Postre.lista_postres
    listbox_stock = tk.Listbox(adminwindow)
    for producto in lista_stock:
        listbox_stock.insert(tk.END, f"{producto.nombre} - Stock: {producto.stock}")
    listbox_stock.pack()
    entry_stock = tk.Entry(adminwindow)
    entry_stock.pack()
    tk.Button(adminwindow, text="Actualizar", command=actualizar_stock).pack()

def iniciar_empleado():
    def verificar_credenciales():
        id_ingresado = entry_id.get()
        pass_ingresado = entry_pass.get()
        if id_ingresado in empleados and empleados[id_ingresado]["contraseña"] == pass_ingresado:
            login_window.destroy()
            messagebox.showinfo("Bienvenido", f"Hola {empleados[id_ingresado]['nombre']}")
            admin()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
    login_window = tk.Toplevel()
    login_window.title("Login Empleado")
    tk.Label(login_window, text="ID de Empleado:").pack()
    entry_id = tk.Entry(login_window)
    entry_id.pack()
    tk.Label(login_window, text="Contraseña:").pack()
    entry_pass = tk.Entry(login_window, show="*")
    entry_pass.pack()
    tk.Button(login_window, text="Ingresar", command=verificar_credenciales).pack()

def iniciar_cliente():
    ventana_inicio.destroy()
    cafeteria()

def cafeteria():
    global pedido_var, listbox_bebidas, listbox_postres, var_tamaño, var_leche, var_azúcar,entry_mesa
    root = tk.Tk()
    root.title("Cafetería Jackbuck")
    root.geometry("450x700")
    imagen = Image.open("C:/Users/axlal/Downloads/jackbucks.jpg")
    imagen = imagen.resize((450, 700))
    fondo = ImageTk.PhotoImage(imagen)
    label_fondo = tk.Label(root, image=fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.image = fondo
    tk.Label(root, text="Cafetería Jackbuck", font=("Arial", 18, "bold")).pack()
    tk.Label(root, text="Número de Mesa:").pack()
    entry_mesa = tk.Entry(root)
    entry_mesa.pack()
    tk.Label(root, text="Bebidas:").pack()
    listbox_bebidas = tk.Listbox(root)
    for bebida in Bebida.lista_bebidas:
        listbox_bebidas.insert(tk.END, f"{bebida.nombre} - ${bebida.precio}")
    listbox_bebidas.pack()
    tk.Button(root, text="Agregar Bebida", command=lambda: agregar_producto("bebida")).pack()
    tk.Label(root, text="Postres:").pack()
    listbox_postres = tk.Listbox(root)
    for postre in Postre.lista_postres:
        listbox_postres.insert(tk.END, f"{postre.nombre} - ${postre.precio}")
    listbox_postres.pack()
    tk.Button(root, text="Agregar Postre", command=lambda: agregar_producto("postre")).pack()
    tk.Label(root, text="Tamaño:").pack()
    var_tamaño = tk.StringVar(value="Mediano")
    tk.OptionMenu(root, var_tamaño, "Chico", "Mediano", "Grande").pack()
    tk.Label(root, text="Tipo de leche:").pack()
    var_leche = tk.StringVar(value="Normal")
    tk.OptionMenu(root, var_leche, "Normal", "Deslactosada", "Avena").pack()
    tk.Label(root, text="Azúcar:").pack()
    var_azúcar = tk.StringVar(value="Normal")
    tk.OptionMenu(root, var_azúcar, "Sin azúcar", "Normal", "Extra azúcar").pack()
    pedido_var = tk.StringVar()
    pedido_var.set("Pedido")
    tk.Label(root, textvariable=pedido_var, justify="left").pack()
    tk.Button(root, text="Eliminar Último Ítem", command=eliminar_item).pack()
    tk.Button(root, text="Realizar Pedido", command=realizar_pedido).pack()
    root.mainloop()

Bebida("Café Latte", 45, 5, ["leche", "café", "azúcar"])
Bebida("Capuchino", 50, 3, ["leche", "café", "chocolate"])
Bebida("Mocha Frío", 55, 4, ["leche", "café", "chocolate", "hielo"])
Postre("Brownie", 35, 4, ["chocolate", "harina", "huevo"])
Postre("Galleta", 25, 6, ["harina", "azúcar"])
Postre("Tarta de Limón", 40, 3, ["limón", "harina", "azúcar", "huevo"])

ventana_inicio = tk.Tk()
ventana_inicio.title("Bienvenido")
ventana_inicio.geometry("300x200")
imagen = Image.open("C:/Users/axlal/Downloads/jackbucks.jpg")
imagen = imagen.resize((300, 200))
fondo = ImageTk.PhotoImage(imagen)
label_fondo = tk.Label(ventana_inicio, image=fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
label_fondo.image = fondo
tk.Label(ventana_inicio, text="Seleccione su rol").pack(pady=10)
tk.Button(ventana_inicio, text="Cliente", command=iniciar_cliente).pack(pady=5)
tk.Button(ventana_inicio, text="Empleado", command=iniciar_empleado).pack(pady=5)
ventana_inicio.mainloop()
