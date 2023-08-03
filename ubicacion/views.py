from django.shortcuts import render, redirect

from .forms import FormularioContacto

from django.core.mail import EmailMessage

# Create your views here.

def ubicacion(request):
    formulario_contacto=FormularioContacto()

    # si se hace post le decimos que rescate la informaicon del formulario
    if request.method=="POST":
        formulario_contacto=FormularioContacto(data=request.POST)
        if formulario_contacto.is_valid():
            nombre=request.POST.get("nombre")
            email=request.POST.get("email")
            contenido=request.POST.get("contenido")

            email=EmailMessage("Mensaje de un usuario",
                               "Un usuario con el nombre de {} y la dirección de correo electrónico {}, ha enviado el siguiente mensaje:\n\n{}"
                               .format(nombre, email, contenido),"",["expendiomares21@gmail.com"],
                               reply_to=[email])
            try:
                email.send()

                return redirect("/ubicacion/?valido")
            except:
                return redirect("/ubicacion/?Nvalido")




    return render(request, "ubicacion/ubicacion.html", {'miformulario':formulario_contacto})

def conocenos(request):
    return render(request, "Conocenos/conocenos.html")