from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Cuenta, Repartidor, Platillo, Pedido, Tarjeta, Vehiculo


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
    return render(request, 'crearCuenta/datosCliente.html')

def datosRepartidor(request):
    return render(request, 'crearCuenta/datosRepartidor.html')

def datosRestaurante(request):
    return render(request, 'crearCuenta/datosRestaurante.html')

def datosTarjeta(request):
    return render(request, 'crearCuenta/datosTarjeta.html')

def datosVehiculo(request):
    return render(request, 'crearCuenta/datosVehiculo.html')

# --- Vista para agregar un elemento al carrito de un cliente
def copiasCarrito(request):
    return render(request, 'cliente/copiasCarrito.html')

# --- Vistas para que un cliente pueda hacer y ver un pedido
def carrito(request):
    return render(request, 'cliente/carrito.html')

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
