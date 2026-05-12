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

def sitioPrincipalRepartidor(request):

    return render(request, 'repartidor/Pantalla_principal_repartidor.html', )

def sitioPrincipalRepartidor(request):

    return render(request, 'repartidor/Pantalla_principal_repartidor.html', )


