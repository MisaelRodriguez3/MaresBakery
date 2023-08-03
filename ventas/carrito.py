class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar_item(self, producto, cantidad):
        id = str(producto.IDproducto)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "producto_id": producto.IDproducto,
                "Nombre": producto.Nombre,
                "Acumulado": producto.Precio * cantidad,
                "Imagen": producto.Imagen,
                "Cantidad": cantidad,
            }
        else:
            self.carrito[id]["Cantidad"] += cantidad
            self.carrito[id]["Acumulado"] += producto.Precio * cantidad
        self.guardar_carrito()

    def aumentar(self, producto):
        id = str(producto.IDproducto)
        if id in self.carrito.keys():
            self.carrito[id]["Cantidad"] += 1
            self.carrito[id]["Acumulado"] += producto.Precio
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar_item(self, producto):
        id = str(producto.IDproducto)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        id = str(producto.IDproducto)
        if id in self.carrito.keys():
            self.carrito[id]["Cantidad"] -= 1
            self.carrito[id]["Acumulado"] -= producto.Precio
            if self.carrito[id]["Cantidad"] <= 0:
                self.eliminar_item(producto)
        self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def sincronizar_con_usuario(self, usuario):
        if usuario.is_authenticated:
            carrito_usuario = self.session.get("carrito_usuario", {})

            for producto_id, producto_info in self.carrito.items():
                carrito_usuario[producto_id] = producto_info
            self.session["carrito_usuario"] = carrito_usuario
            self.carrito = {}
            self.guardar_carrito()
