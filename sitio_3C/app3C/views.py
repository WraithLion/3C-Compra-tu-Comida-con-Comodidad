from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Cuenta, Cliente, Repartidor, Restaurante, Platillo, Promociones, Pedido, Orden, Tarjeta, Vehiculo


# --- VISTAS PARA CUENTA ---
def sitioPrincipal3C(request):
    
    return render(request, 'sitio_principal_3C.html', )

def sitioPrincipalCliente(request):

    return render(request, 'cliente/Pantalla_principal_cliente.html', )

def sitioPrincipalRestaurante(request):

    return render(request, 'restaurante/Pantalla_principal_restaurante.html', )

def promocionesRestaurante(request):

    return render(request, 'restaurante/Pantalla_promociones_restaurante.html',)

def sitioPrincipalRepartidor(request):

    return render(request, 'repartidor/Pantalla_principal_repartidor.html', )

def sitioPrincipalRepartidor(request):

    return render(request, 'repartidor/Pantalla_principal_repartidor.html', )


# --- Vistas para la creación de una cuenta
def tipoCuenta(request):
    return render(request, 'crearCuenta/tipoCuenta.html')

def datosCliente(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        us = request.POST.get('us')
        cor = request.POST.get('cor')
        tel = request.POST.get('tel')
        con = request.POST.get('con')

        cuenta = Cuenta.objects.create(
            nombre = nom,
            usuario = us,
            correo = cor,
            teléfono = tel,
            contraseña = con
        )
        Cliente.objects.create(IDcuenta = cuenta)
        messages.success(request, "Cuenta creada con éxito. Inicie sesión para empezar a usar la aplicación")
        return redirect('sitioPrincipal_3C')
    return render(request, 'crearCuenta/datosCliente.html')

def datosRepartidor(request):
    if request.method == 'POST':
        cuenta = Cuenta.objects.create(
            nombre = request.POST.get('nom'),
            usuario = request.POST.get('us'),
            correo = request.POST.get('cor'),
            teléfono = request.POST.get('tel'),
            contraseña = request.POST.get('con')
        )
        Repartidor.objects.create(
            IDcuenta = cuenta,
            CURP = request.POST.get('cur')
        )
        request.session['username'] = cuenta.usuario
        return redirect('datosVehiculo')
    return render(request, 'crearCuenta/datosRepartidor.html')

def datosRestaurante(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        dir = request.POST.get('dir')
        us = request.POST.get('us')
        cor = request.POST.get('cor')
        tel = request.POST.get('tel')
        con = request.POST.get('con')

        cuenta = Cuenta.objects.create(
            nombre = nom,
            usuario = us,
            correo = cor,
            teléfono = tel,
            contraseña = con
        )
        Restaurante.objects.create(
            IDcuenta = cuenta,
            direccion = dir
        )
        request.session['username'] = us
        return redirect('datosTarjeta')
    return render(request, 'crearCuenta/datosRestaurante.html')

def datosTarjeta(request):
    username = request.session.get('username')
    if request.method == 'POST':
        num = request.POST.get('num')
        tit = request.POST.get('tit')
        mmaa = request.POST.get('mmaa')
        cc = request.POST.get('cc')
    
        Tarjeta.objects.create(
            numero = num,
            usuario = get_object_or_404(Cuenta, usuario = username),
            titular = tit,
            vencimiento = mmaa,
            ccv = cc
        )
        messages.success(request, "Cuenta creada con éxito. Inicie sesión para empezar a usar la aplicación")
        return redirect('sitioPrincipal_3C')
    return render(request, 'crearCuenta/datosTarjeta.html')

def datosVehiculo(request):
    username = request.session.get('username')
    if request.method == 'POST':
        cuenta = get_object_or_404(Cuenta, usuario = username)
        Vehiculo.objects.create(
            tipo = request.POST.get('tipoVehiculo'),
            modelo = request.POST.get('mod'),
            color = request.POST.get('col'),
            placa = request.POST.get('pla'),
            propietario = get_object_or_404(Repartidor, IDcuenta = cuenta)
        )
        return redirect('datosTarjeta')
    return render(request, 'crearCuenta/datosVehiculo.html')

# --- Vista para agregar un elemento al carrito de un cliente
def copiasCarrito(request):
    IDplatillo = request.session.get('IDpla')
    platillo = get_object_or_404(Platillo, IDelemento = IDplatillo)
    return render(request, 'cliente/copiasCarrito.html', {'platillo' : platillo})

# --- Vistas para que un cliente pueda hacer y ver un pedido
def carrito(request):
    usuario = request.user
    if usuario.is_authenticated:
        pedidos = Pedido.objects.filter(userCliente=usuario)
        ordenes = Orden.objects.filter(pedido_in=pedidos).select_related('platillo')
        return render(request, 'cliente/carrito.html', {'ordenes': ordenes})
    else:
        return render(request, 'error/loginError.html')

def metodoPago(request):
    return render(request, 'cliente/metodoPago.html')

def direccionEntrega(request):
    return render(request, 'cliente/direccionEntrega.html')

def pedidoCliente(request):
    return render(request, 'cliente/estadoPedido.html')

# --- Vista para que un repartidor pueda aceptar y actualizar un pedido
def pedidosPendientes(request):
    return render(request, 'repartidor/pedidosPendientes.html')

def pedidoRepartidor(request):
    return render(request, 'repartidor/estadoPedido.html')

# --- Vista para que un restaurante pueda ver sus órdenes pendientes
def ordenes(request):
    return render(request, 'restaurante/ordenes.html')

# --- Vistas para el manejo de la cuenta por un usuario
def opcionesCuenta(request):
    return render(request, 'cuenta/opcionesCuenta.html')

def modificarCuenta(request):
    return render(request, 'cuenta/modificarCuenta.html')

def eliminarCuenta(request):
    return render(request, 'cuenta/eliminarCuenta.html')
