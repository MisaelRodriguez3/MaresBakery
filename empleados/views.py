from django.shortcuts import render
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from panaderia import settings
from .models import Empleados
from ventas.models import Facturas, Encargos, Info_facturas, Info_encargos
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.

def lista_empleados(request):
    empleado = Empleados.objects.all()  
    return render(request, '.html', {'empleado': empleado})

def correo_compra_empleados(request, factura, metodo):
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
    
    mensaje_empleado = 'Se ha realizado una nueva compra por parte de {} {}.'.format(request.user.username, request.user.last_name)
    context = {
        'factura': factura,
        'info_facturas': info_facturas,
        'total_compra': total_compra,
        'hora': hora,
        'metodo': metodo,
        'subtotal': item.Subtotal,
        'mensaje': mensaje_empleado
    }
    # Renderizar la plantilla HTML con los datos
    html_content = render_to_string(
        'vista_mensaje/ticket_compra.html', context)

    # Crear una versión de texto plano del contenido HTML
    text_content = strip_tags(html_content)

    # Enviar el correo electrónico a los empleados
    subject = 'Nueva compra realizada'
    from_email = settings.EMAIL_HOST_USER
    empleados = Empleados.objects.all()
    to_email = [empleado.Correo for empleado in empleados]

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    img_path = 'ventas/static/img/log.png'
    with open(img_path, 'rb') as f:
        msg_img = MIMEImage(f.read())
        msg_img.add_header('Content-ID', '<imagen>')
        msg.attach(msg_img)
    msg.send()
    

def correo_encargo_empleados(request, encargo, metodo, fecha):
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
    
    mensaje_empleado = 'Se ha realizado un nuevo encargo por parte de {} {}.'.format(request.user.username, request.user.last_name)
    context = {
        'encargo': encargo,
        'info_encargo': info_encargo,
        'total_compra': total_compra,
        'hora': hora,
        'metodo': metodo,
        'subtotal': item.Subtotal,
        'mensaje': mensaje_empleado,
        'fecha': fecha,
        'anticipo': anticipo
    }
    # Renderizar la plantilla HTML con los datos
    html_content = render_to_string(
        'vista_mensaje/ticket_compra.html', context)

    # Crear una versión de texto plano del contenido HTML
    text_content = strip_tags(html_content)

    # Enviar el correo electrónico a los empleados
    subject = 'Nuevo encargo realizado'
    from_email = settings.EMAIL_HOST_USER
    empleados = Empleados.objects.all()
    to_email = [empleado.Correo for empleado in empleados]

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    img_path = 'ventas/static/img/log.png'
    with open(img_path, 'rb') as f:
        msg_img = MIMEImage(f.read())
        msg_img.add_header('Content-ID', '<imagen>')
        msg.attach(msg_img)
    msg.send()
