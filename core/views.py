from decimal import Decimal
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido, Platillo, DetallePedido, Pago

# Create your views here.
def home(request):
    return render(request, "home.html")

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by("-fecha_creacion")
    context = {"pedidos":pedidos}
    return render(request, "core/lista_pedidos.html", context)

@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    context = {"pedido":pedido}
    return render(request, "core/detalle_pedido.html",context)

@login_required
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id = pedido_id, usuario = request.user)

    if not pedido.puede_modificarse():
        messages.error(request, 'Este pedido ya no se puede modificar.')
        return redirect("detalle_pedido", pedido_id = pedido.id)
    
    platillos = Platillo.objects.filter(disponible = True).order_by("nombre")

    cantidades_actuales = {}
    for detalle in pedido.detalles.all():
        cantidades_actuales[detalle.platillo.id] = detalle.cantidad

    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')

        if not metodo_pago:
            messages.error(request, 'debes seleccionar un metodo de pago.')
            context = {
                'pedido': pedido,
                'platillos': platillos,
                'cantidades_actuales': cantidades_actuales,
            }
            return render(request, "core/editar_pedido.html", context)
        
        detalle_temp = []
        total = Decimal('0.00')

        for platillo in platillos:
            cantidad_str = request.POST.get(f'cantidad_{platillo.id}','0')

            try:
                cantidad = int(cantidad_str)
            except ValueError:
                cantidad = 0
            
            if cantidad > 0:
                precio_unitario = platillo.precio
                subtotal = precio_unitario * cantidad

                detalle_temp.append({
                    'platillo': platillo,
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'subtotal': subtotal
                })

                total += subtotal
        
        if not detalle_temp:
            messages.error(request,'El pedido debe tener al menos un platillo')
            context = {
                'pedido': pedido,
                'platillos': platillos,
                'cantidades_actuales': cantidades_actuales,
            }
            return render(request, "core/editar_pedido.html", context)
        
        with transaction.atomic():
            pedido.detalles.all().delete()

            for detalle in detalle_temp:
                DetallePedido.objects.create(
                    pedido = pedido,
                    platillo = detalle['platillo'],
                    cantidad = detalle['cantidad'],
                    precio_unitario = detalle['precio_unitario'],
                    subtotal = detalle['subtotal']
                )
            pedido.total = total
            pedido.save(update_fields=['total'])

            pedido.pago.metodo_pago = metodo_pago
            pedido.pago.monto = total
            pedido.pago.save(update_fields = ['metodo_pago', 'monto'])

        messages.success(request, 'Pedido actualizado correctamente.')
        return redirect('detalle_pedido', pedido_id = pedido.id)
    context = {
                'pedido': pedido,
                'platillos': platillos,
                'cantidades_actuales': cantidades_actuales,
            }
    return render(request, 'core/editar_pedido.html', context)

@login_required
def crear_pedido(request):
    platillos = Platillo.objects.filter(disponible=True).order_by('nombre')

    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')
        detalles_temp = []
        total = Decimal('0.00')

        if not metodo_pago:
            messages.error(request, 'Debes seleccionar un método de pago.')
            return render(request, 'core/crear_pedido.html', {'platillos': platillos})

        for platillo in platillos:
            cantidad_str = request.POST.get(f'cantidad_{platillo.id}', '0')

            try:
                cantidad = int(cantidad_str)
            except ValueError:
                cantidad = 0

            if cantidad > 0:
                precio_unitario = platillo.precio
                subtotal = precio_unitario * cantidad

                detalles_temp.append({
                    'platillo': platillo,
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'subtotal': subtotal,
                })

                total += subtotal

        if not detalles_temp:
            messages.error(request, 'Debes seleccionar al menos un platillo con cantidad mayor a 0.')
            return render(request, 'core/crear_pedido.html', {'platillos': platillos})

        with transaction.atomic():
            pedido = Pedido.objects.create(
                usuario=request.user,
                estado='pendiente',
                total=total
            )

            for detalle in detalles_temp:
                DetallePedido.objects.create(
                    pedido=pedido,
                    platillo=detalle['platillo'],
                    cantidad=detalle['cantidad'],
                    precio_unitario=detalle['precio_unitario'],
                    subtotal=detalle['subtotal']
                )

            Pago.objects.create(
                pedido=pedido,
                monto=total,
                metodo_pago=metodo_pago,
                estado_pago='pendiente'
            )

        messages.success(request, 'Pedido creado correctamente.')
        return redirect('detalle_pedido', pedido_id=pedido.id)

    return render(request, 'core/crear_pedido.html', {'platillos': platillos})

@login_required
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)

    if request.method == 'POST':
        if not pedido.puede_cancelarse():
            messages.error(request, 'Este pedido ya no se puede cancelar.')
            return redirect('detalle_pedido', pedido_id=pedido.id)

        pedido.estado = 'cancelado'
        pedido.save(update_fields=['estado'])

        messages.success(request, 'El pedido ha sido cancelado correctamente.')
        return redirect('lista_pedidos')

    return render(request, 'core/cancelar_pedido.html', {'pedido': pedido})