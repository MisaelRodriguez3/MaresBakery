from email.mime.image import MIMEImage
from django.shortcuts import get_object_or_404, render, redirect
from panaderia import settings
from ventas.carrito import Carrito
from ventas.context_processor import total_carrito
from datetime import datetime
from django.utils import timezone
from .models import Clientes_facturas, Clientes_encargos, Productos, Facturas, Encargos, Info_facturas, Info_encargos
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.models import User
from panaderia.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import View
import json
from empleados.views import correo_compra_empleados, correo_encargo_empleados

# Create your views here.
def carrito(request):
    carrito = Carrito(request)
    productos_carrito = carrito.carrito.values()
    context = {
        "carrito": productos_carrito,
    }
    return render(request, "carrito/Carrito.html", context)


def agregar_producto(request, producto_id):
    if request.method == "POST":
        cantidad = request.POST.get("cantidad", 1)
        if cantidad.isdigit():
            cantidad = int(cantidad)
            carrito = Carrito(request)
            producto = Productos.objects.get(IDproducto=producto_id)
        else:
            cantidad = 1
            carrito = Carrito(request)
            producto = Productos.objects.get(IDproducto=producto_id)
        carrito.agregar_item(producto, cantidad)
    return JsonResponse({})


def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Productos.objects.get(IDproducto=producto_id)
    carrito.eliminar_item(producto)
    total = total_carrito(request)
    response_data = {
        'producto_id': producto_id,
        'new_quantity': 0,
        'total_carrito': total,
        'eliminar': True
    }
    return JsonResponse(response_data)


def aumentar(request, producto_id):
    carrito = Carrito(request)
    producto = Productos.objects.get(IDproducto=producto_id)
    carrito.aumentar(producto)
    updated_product_info = carrito.carrito.get(str(producto_id), {})
    total = total_carrito(request)
    response_data = {
        'producto_id': producto_id,
        'new_quantity': updated_product_info.get('Cantidad', 0),
        'total_carrito': total
    }
    return JsonResponse(response_data)


def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Productos.objects.get(IDproducto=producto_id)
    carrito.restar(producto)
    updated_product_info = carrito.carrito.get(str(producto_id), {})
    total = total_carrito(request)
    response_data = {
        'producto_id': producto_id,
        'new_quantity': updated_product_info.get('Cantidad', 0),
        'total_carrito': total
    }
    return JsonResponse(response_data)

def comprar(request):
    carrito = Carrito(request)
    if request.method == "POST":
        forma_de_pago = request.POST.get('pago')
        if "efectivo" in forma_de_pago:
            user_id = request.user.id
            total_carrito = sum(item['Acumulado'] for item in carrito.carrito.values())
            factura = Facturas()
            factura.IDcliente = User.objects.get(id=user_id)
            factura.Total_a_pagar = total_carrito
            factura.Fecha_pedido = timezone.localtime(timezone.now())
            factura.transaction_id = "Pago en efectivo"
            factura.save()

            #guardar datos en Clientes_facturas
            cliente_factura = Clientes_facturas()
            cliente_factura.IDcliente = User.objects.get(id=user_id)
            cliente_factura.IDfactura = factura
            cliente_factura.save()

            # Obtener el carrito de compras de la sesión
            for producto_info in carrito.carrito.values():
                producto_id = producto_info["producto_id"]
                cantidad = producto_info["Cantidad"]

                producto = get_object_or_404(Productos, IDproducto=producto_id)

                info_factura = Info_facturas()
                info_factura.IDfactura = factura
                info_factura.IDproducto = producto
                info_factura.cantidad = cantidad
                info_factura.save()
            metodo = "Efectivo"
            correo_compra_empleados(request, factura=factura.IDfactura, metodo=metodo)
            correo_compra_clientes(request, factura=factura.IDfactura, metodo=metodo)
            carrito.limpiar()
            return redirect('../carrito')
        elif "paypal" in forma_de_pago:
            return redirect('proceso')

def verificar_encargo(request):
    if not request.user.is_authenticated:
        return JsonResponse({'califica': False, 'redirect':'../../accounts/login'})
    else:
        carrito = Carrito(request)
        if sum(item['Cantidad'] for item in carrito.carrito.values()) <20:
            return JsonResponse({'califa': False})
        else:
            return JsonResponse({'califica': True})

def encargar(request):
    carrito = Carrito(request)
    if request.method == "POST":
        forma_de_pago = request.POST.get('pago_e')
        fecha = request.POST.get('fecha')
        if "efectivo" in forma_de_pago:
            user_id = request.user.id
            total_carrito = sum(item['Acumulado'] for item in carrito.carrito.values())

            encargo = Encargos()
            encargo.IDcliente = User.objects.get(id=user_id)
            encargo.Total = total_carrito
            encargo.Anticipo = 0
            encargo.Fecha_encargo =timezone.localtime(timezone.now())
            encargo.Fecha_entrega = fecha
            encargo.transaction_id = "Pago en efectivo"
            encargo.save()

            #guardar datos en Clientes_encargos
            cliente_encargo = Clientes_encargos()
            cliente_encargo.IDcliente = User.objects.get(id=user_id)
            cliente_encargo.IDencargo = encargo
            cliente_encargo.save()

            # Obtener el carrito de compras de la sesión
            for producto_info in carrito.carrito.values():
                producto_id = producto_info["producto_id"]
                cantidad = producto_info["Cantidad"]

                producto = get_object_or_404(Productos, IDproducto=producto_id)

                info_encargo = Info_encargos()
                info_encargo.IDencargo = encargo
                info_encargo.IDproducto = producto
                info_encargo.Cantidad = cantidad
                info_encargo.save()
            metodo = "Efectivo"
            correo_encargo_empleados(request, encargo=encargo.IDencargo, metodo=metodo, fecha=fecha)
            correo_encargo_clientes(request,encargo=encargo.IDencargo, metodo=metodo, fecha=fecha)
            carrito.limpiar()
            return redirect('../carrito')
        elif "paypal" in forma_de_pago:
            #cambiar el redirect si se hace otra vista
            return redirect('proceso_encargo', fecha=fecha)


def correo_compra_clientes(request, factura, metodo):
    # Obtener el objeto de la factura
    try:
        factura = Facturas.objects.get(pk=factura)
        info_facturas = Info_facturas.objects.filter(IDfactura=factura)
        total_compra = sum(item.IDproducto.Precio * item.cantidad for item in info_facturas)
        hora = factura.Fecha_pedido.strftime("%d/%m/%Y %H:%M:%S")
        for item in info_facturas:
            item.Subtotal = item.IDproducto.Precio * item.cantidad
        metodo = metodo
    except Facturas.DoesNotExist:
        return render(request, 'ruta_de_tu_app/error.html')
    
    mensaje_cliente = "Su compra ha sido procesada. Puede pasar a tienda y recogerlo."
    context = {
        'factura': factura,
        'info_facturas': info_facturas,
        'total_compra': total_compra,
        'hora': hora,
        'metodo': metodo,
        'subtotal': item.Subtotal,
        'mensaje': mensaje_cliente
    }
    # Renderizar la plantilla HTML con los datos
    html_content = render_to_string(
        'vista_mensaje/ticket_compra.html', context)

    # Crear una versión de texto plano del contenido HTML
    text_content = strip_tags(html_content)

    # Enviar el correo electrónico al cliente
    subject = "Se ha confirmado una compra"
    from_email = settings.EMAIL_HOST_USER
    to_email = [request.user.email]

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    img_path = 'ventas/static/img/log.png'
    with open(img_path, 'rb') as f:
        msg_img = MIMEImage(f.read())
        msg_img.add_header('Content-ID', '<imagen>')
        msg.attach(msg_img)
    msg.send()
    

def correo_encargo_clientes(request, encargo, metodo, fecha):
    try:
        encargo = Encargos.objects.get(pk=encargo)
        info_encargo = Info_encargos.objects.filter(IDencargo=encargo)
        total_compra = sum(item.IDproducto.Precio * item.Cantidad for item in info_encargo)
        anticipo = total_compra / 2
        hora = encargo.Fecha_encargo.strftime("%d/%m/%Y %H:%M:%S")
        for item in info_encargo:
            item.Subtotal = item.IDproducto.Precio * item.Cantidad
        metodo = metodo
    except Encargos.DoesNotExist:
        return render(request, 'ruta_de_tu_app/error.html')
    
    mensaje_cliente = "Su encargo ha sido procesado. Puede pasar a tienda y recogerlo el día acordado dentro del horario laboral."
    context = {
        'encargo': encargo,
        'info_encargo': info_encargo,
        'total_compra': total_compra,
        'hora': hora,
        'metodo': metodo,
        'subtotal': item.Subtotal,
        'mensaje': mensaje_cliente,
        'fecha': fecha,
        'anticipo': anticipo
    }
    # Renderizar la plantilla HTML con los datos
    html_content = render_to_string(
        'vista_mensaje/ticket_compra.html', context)

    # Crear una versión de texto plano del contenido HTML
    text_content = strip_tags(html_content)

    # Enviar el correo electrónico al cliente
    subject = "Se ha confirmado un Encargo"
    from_email = settings.EMAIL_HOST_USER
    to_email = [request.user.email]

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    img_path = 'ventas/static/img/log.png'
    with open(img_path, 'rb') as f:
        msg_img = MIMEImage(f.read())
        msg_img.add_header('Content-ID', '<imagen>')
        msg.attach(msg_img)
    msg.send()


def proceso(request):
    carrito = Carrito(request)
    total_carrito = sum(item['Acumulado'] for item in carrito.carrito.values())
    #total_carrito = (total * 1.0395) + 5.50

    context = {
        'total_carrito': str(total_carrito),  # Convertir a cadena (string)
    }
    return render(request, 'carrito/proceso.html', context) 

class GuardarDatosPagoView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            user_id = request.user.id

            # Datos del fetch
            data = json.loads(request.body)

            amount = data.get('amount')
            transaction_id = data.get('transactionId')

            #guardar datos en Facturas
            factura = Facturas()
            factura.IDcliente = User.objects.get(id=user_id)
            factura.Total_a_pagar = amount
            factura.transaction_id = transaction_id
            factura.Fecha_pedido = timezone.localtime(timezone.now())
            factura.save()

            #guardar datos en Clientes_facturas
            cliente_factura = Clientes_facturas()
            cliente_factura.IDcliente = User.objects.get(id=user_id)
            cliente_factura.IDfactura = factura
            cliente_factura.save()

            # Obtener el carrito de compras de la sesión
            carrito = Carrito(request)
            for producto_info in carrito.carrito.values():
                producto_id = producto_info["producto_id"]
                cantidad = producto_info["Cantidad"]

                producto = get_object_or_404(Productos, IDproducto=producto_id)

                info_factura = Info_facturas()
                info_factura.IDfactura = factura
                info_factura.IDproducto = producto
                info_factura.cantidad = cantidad
                info_factura.save()
 
            # Verificar en la consola
            print('Transaction ID:', transaction_id)
            print('User ID autenticado:', user_id)

            
            carrito.limpiar()
            # Devolver una respuesta JSON con la clave "success" que indica que el procesamiento fue exitoso
            return JsonResponse({'success': True})
        else:
            # Devolver una respuesta JSON con la clave "success" en falso ya que el usuario no está autenticado
            return JsonResponse({'success': False, 'message': 'Usuario no autenticado'})


def proceso_encargo(request, fecha):
    carrito = Carrito(request)
    total_carrito = sum(item['Acumulado'] for item in carrito.carrito.values())
    fecha_actual = fecha

    context = {
        'total_carrito': str(total_carrito),
        'fecha': str(fecha_actual) # Convertir a cadena (string)
    }
    return render(request, 'carrito/proceso_encargo.html', context)


class GuardarDatosEncargoView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            user_id = request.user.id

            carrito = Carrito(request)

            # Datos del fetch
            data = json.loads(request.body)

            amount = data.get('amount')
            transaction_id = data.get('transactionId')
            totalAnticipo = data.get('totalAnticipo')
            fecha = data.get('fecha')
            fecha_formateada = datetime.strptime(fecha, "%Y-%m-%d")

            encargo = Encargos()
            encargo.IDcliente = User.objects.get(id=user_id)
            encargo.Fecha_entrega = fecha_formateada
            encargo.Anticipo = totalAnticipo
            encargo.Total = amount
            encargo.transaction_id=transaction_id
            encargo.Fecha_encargo =timezone.localtime(timezone.now())
            encargo.save()

            #guardar datos en Clientes_encargo
            cliente_encargo = Clientes_encargos()
            cliente_encargo.IDcliente = User.objects.get(id=user_id)
            cliente_encargo.IDencargo = encargo
            cliente_encargo.save()


            
            for producto_info in carrito.carrito.values():
                producto_id = producto_info["producto_id"]
                cantidad = producto_info["Cantidad"]

                producto = get_object_or_404(Productos, IDproducto=producto_id)

                info_encargo = Info_encargos()
                info_encargo.IDencargo = encargo
                info_encargo.IDproducto = producto
                info_encargo.Cantidad = cantidad
                info_encargo.save()
           
            carrito.limpiar()
            # Devolver una respuesta JSON con la clave "success" que indica que el procesamiento fue exitoso
            return JsonResponse({'success': True})
        else:
            # Devolver una respuesta JSON con la clave "success" en falso ya que el usuario no está autenticado
            return JsonResponse({'success': False, 'message': 'Usuario no autenticado'})
