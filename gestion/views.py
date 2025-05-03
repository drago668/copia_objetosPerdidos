from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomAuthenticationForm, UsuarioForm, objetoForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import objeto, SolicitudPrestamo,CustomUser
from django.contrib import messages
from django.db.models import Q
from django.db.models import Count


def listar_objetos(request):
    solictudesA=SolicitudPrestamo.objects.filter(solicitante=request.user)
    query = request.GET.get('q', '')  # Obtiene el parámetro 'q' de la URL
    if query:
        objetos = objeto.objects.filter(Q(nombre__icontains=query))\
            
    else:
          
        objetos = objeto.objects.exclude(propietario=request.user)

    return render(request, 'listar_objetos.html', {'objetos': objetos, 'query': query,'solicitudes':solictudesA})

@login_required
def listar_objetos_prpietario(request):
    query = request.GET.get('q', '')  # Obtiene el parámetro 'q' de la URL
    if query:
        objetos = objeto.objects.filter(Q(nombre__icontains=query))
    else:
        objetos = objeto.objects.filter(propietario=request.user)
    return render(request, 'listar_objetos_propietario.html', {'objetos': objetos, 'query': query})

@login_required
def publicar_objeto(request):
    if request.method == 'POST':
        form = objetoForm(request.POST, request.FILES)
        if form.is_valid():
            objeto = form.save(commit=False)
            objeto.propietario = request.user
            objeto.save()
            
            return redirect('listar_objetos')
    else:
        form = objetoForm()
    return render(request, 'objeto_perdido.html', {'form': form})




@login_required
def solicitar_prestamo(request, objeto_id):
    print("ingresooo", objeto_id)
    Objeto= get_object_or_404(objeto, id=objeto_id)
    if Objeto.propietario != request.user:
        SolicitudPrestamo.objects.create(
            objeto=Objeto,
            solicitante=request.user,
            propietario=Objeto.propietario,
            mensaje=request.POST.get("Mensaje_de_objeto")
        )
        messages.success(request, f"Solicitud enviada para el libro '{objeto.nombre}'.")
        return redirect('listar_objetos')
    else:
        messages.error(request, "No puedes solicitar tu propio libro.")
        return redirect('listar_objetos')


def index(request):
    return render(request, 'index.html')



    
def login_view(request):
    print("ingresooo")
    if request.method == 'POST':
        print("Se recibió una solicitud POST")
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("El formulario es valido")
            user = form.get_user()
            login(request, user)
            return redirect('inicio')  # O la página a la que quieras redirigir después de iniciar sesión
        else:
            print("El formulario es invalido")
        
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def registrar(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()  # Crea el usuario pero no lo guarda
            login(request, user)
            return redirect('inicio')
    else:
        form = UsuarioForm()
    return render(request, 'registro.html', {'form': form})


@login_required
def gestionar_solicitudes(request):
    solicitudes = SolicitudPrestamo.objects.filter(objeto__propietario=request.user, estado='pendiente')

    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        # Verifica si el ID está presente y es válido
        if not solicitud_id:
            return render(request, 'error.html', {'mensaje': 'ID de solicitud no proporcionado.'})

        # Busca la solicitud
        solicitud = SolicitudPrestamo.objects.filter(id=solicitud_id).first()

        # Si no existe, maneja el error
        if not solicitud:
            return render(request, 'error.html', {'mensaje': 'No se encontró la solicitud especificada.'})
        accion = request.POST.get('accion')
        solicitud = get_object_or_404(SolicitudPrestamo, id=solicitud_id, objeto__propietario=request.user)

        if accion == 'aceptar':
            mensaje_contacto = request.POST.get('mensaje_contacto')  # Capturar mensaje
            if not mensaje_contacto:
                    # Puedes redirigir con un mensaje de error si es necesario
                    messages.error(request, "El mensaje de contacto es obligatorio.")
                    return redirect('gestionar_solicitudes')
            solicitud.estado = 'aceptada'
            solicitud.mensaje_contacto = mensaje_contacto
            solicitud.objeto.disponible = False  # Marca el libro como no disponible
            solicitud.objeto.save()
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'
        solicitud.save()

    return render(request, 'gestionar_solicitudes.html', {'solicitudes': solicitudes})

@login_required
def solicitudes_aprobadas(request):
    solicitudes = SolicitudPrestamo.objects.filter(solicitante=request.user, estado='aceptada')
    return render(request, 'solicitudes_aprobadas.html', {'solicitudes': solicitudes})


