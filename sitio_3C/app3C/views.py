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

# Verificacion de tipo de usuario
#

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['nombre']
#         password = request.POST['contraseña']
#         backend = CuentaBackend()
#         user = backend.authenticate(request, username=username, password=password)
#         if user is not None:
#             auth_login(request, user, backend='app3C.backends.CuentaBackend')
#             # Redirige al parámetro 'next' si existe, si no, a una URL por defecto
#             next_url = request.POST.get('next') or request.GET.get('next') or '/cargarContenido/'
#             return JsonResponse({'success': True, 'redirect': next_url})
#         else:
#             return JsonResponse({'success': False, 'error': 'Credenciales inválidas'})
#     # Para solicitudes GET, podrías devolver el formulario, pero para fetch, un JSON con error también sirve
#     return JsonResponse({'success': False, 'error': 'Método no permitido'})
#
#
# def cargarContenido(request):
#     cuenta = request.user.cuenta  # Asume que estás usando Cuenta como modelo principal
#
#     if hasattr(cuenta, 'cliente'):
#         return redirect('pantalla_principal_cliente')
#     elif hasattr(cuenta, 'restaurante'):
#         return redirect('pantalla_principal_restaurante')
#     elif hasattr(cuenta, 'repartidor'):
#         return redirect('pantalla_principal_repartidor')
#     else:
#         # Si no tiene rol, muestra el formulario principal con un mensaje
#         return render(request, 'index.html', {
#             'error': 'Datos incorrectos, inténtalo de nuevo'
#         })
#
#
# # --- VISTAS PARA CUENTAS ---
#
# def pantalla_principal_cliente(request):
#
#     return render(request, 'cliente/Pantalla_principal_cliente.html', {})
#
# def pantalla_principal_restaurante(request):
#
#     return render(request, 'restaurante/Pantalla_principal_restaurante.html', {})
#
# def pantalla_principal_repartidor(request):
#
#     return render(request, 'repartidor/Pantalla_principal_repartidor.html', {})
#
# def cuenta_list(request):
#     items = Cuenta.objects.all()
#     return render(request, 'cuenta/cuenta_list.html', {'items': items})
#
# def cuenta_create(request):
#     if request.method == 'POST':
#         form = CuentaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('cuenta_list')
#     else:
#         form = CuentaForm()
#     return render(request, 'cuenta/cuenta_form.html', {'form': form, 'action': 'Crear Cuenta'})
#
# def cuenta_update(request, pk):
#     item = get_object_or_404(Cuenta, pk=pk)
#     if request.method == 'POST':
#         form = CuentaForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('cuenta_list')
#     else:
#         form = CuentaForm(instance=item)
#     return render(request, 'cuenta/cuenta_form.html', {'form': form, 'action': 'Actualizar Cuenta'})
#
# def cuenta_delete(request, pk):
#     item = get_object_or_404(Cuenta, pk=pk)
#     if request.method == 'POST':
#         item.delete()
#         return redirect('cuenta_list')
#     return render(request, 'cuenta/cuenta_confirm_delete.html', {'item': item})
#
# # --- VISTAS PARA REPARTIDOR ---
# def repartidor_list(request):
#     items = Repartidor.objects.all()
#     return render(request, 'repartidor/repartidor_list.html', {'items': items})
#
# def repartidor_create(request):
#     if request.method == 'POST':
#         form = RepartidorForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('repartidor_list')
#     else:
#         form = RepartidorForm()
#     return render(request, 'repartidor/repartidor_form.html', {'form': form, 'action': 'Crear Repartidor'})
#
# def repartidor_update(request, pk):
#     item = get_object_or_404(Repartidor, pk=pk)
#     if request.method == 'POST':
#         form = RepartidorForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('repartidor_list')
#     else:
#         form = RepartidorForm(instance=item)
#     return render(request, 'repartidor/repartidor_form.html', {'form': form, 'action': 'Actualizar Repartidor'})
#
# def repartidor_delete(request, pk):
#     item = get_object_or_404(Repartidor, pk=pk)
#     if request.method == 'POST':
#         item.delete()
#         return redirect('repartidor_list')
#     return render(request, 'repartidor/repartidor_confirm_delete.html', {'item': item})
#
# # --- VISTAS PARA PLATILLO ---
# def platillo_list(request):
#     items = Platillo.objects.all()
#     return render(request, 'platillo/platillo_list.html', {'items': items})
#
# def platillo_create(request):
#     if request.method == 'POST':
#         form = PlatilloForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('platillo_list')
#     else:
#         form = PlatilloForm()
#     return render(request, 'platillo/platillo_form.html', {'form': form, 'action': 'Crear Platillo'})
#
# def platillo_update(request, pk):
#     item = get_object_or_404(Platillo, pk=pk)
#     if request.method == 'POST':
#         form = PlatilloForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('platillo_list')
#     else:
#         form = PlatilloForm(instance=item)
#     return render(request, 'platillo/platillo_form.html', {'form': form, 'action': 'Actualizar Platillo'})
#
# def platillo_delete(request, pk):
#     item = get_object_or_404(Platillo, pk=pk)
#     if request.method == 'POST':
#         item.delete()
#         return redirect('platillo_list')
#     return render(request, 'platillo/platillo_confirm_delete.html', {'item': item})
#
# # --- VISTAS PARA PEDIDO ---
# def pedido_list(request):
#     items = Pedido.objects.all()
#     return render(request, 'pedido/pedido_list.html', {'items': items})
#
# def pedido_create(request):
#     if request.method == 'POST':
#         form = PedidoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('pedido_list')
#     else:
#         form = PedidoForm()
#     return render(request, 'pedido/pedido_form.html', {'form': form, 'action': 'Crear Pedido'})
#
# def pedido_update(request, pk):
#     item = get_object_or_404(Pedido, pk=pk)
#     if request.method == 'POST':
#         form = PedidoForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('pedido_list')
#     else:
#         form = PedidoForm(instance=item)
#     return render(request, 'pedido/pedido_form.html', {'form': form, 'action': 'Actualizar Pedido'})
#
# def pedido_delete(request, pk):
#     item = get_object_or_404(Pedido, pk=pk)
#     if request.method == 'POST':
#         item.delete()
#         return redirect('pedido_list')
#     return render(request, 'pedido/pedido_confirm_delete.html', {'item': item})
#
# # --- VISTAS PARA TARJETA ---
# def tarjeta_list(request):
#     items = Tarjeta.objects.all()
#     return render(request, 'tarjeta/tarjeta_list.html', {'items': items})
#
# def tarjeta_create(request):
#     if request.method == 'POST':
#         form = TarjetaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('tarjeta_list')
#     else:
#         form = TarjetaForm()
#     return render(request, 'tarjeta/tarjeta_form.html', {'form': form, 'action': 'Crear Tarjeta'})
#
# def tarjeta_update(request, pk):
#     item = get_object_or_404(Tarjeta, pk=pk)
#     if request.method == 'POST':
#         form = TarjetaForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('tarjeta_list')
#     else:
#         form = TarjetaForm(instance=item)
#     return render(request, 'tarjeta/tarjeta_form.html', {'form': form, 'action': 'Actualizar Tarjeta'})
#
# def tarjeta_delete(request, pk):
#     item = get_object_or_404(Tarjeta, pk=pk)
#     if request.method == 'POST':
#         item.delete()
#         return redirect('tarjeta_list')
#     return render(request, 'tarjeta/tarjeta_confirm_delete.html', {'item': item})
#
# # --- VISTAS PARA VEHICULO ---
# def vehiculo_list(request):
#     items = Vehiculo.objects.all()
#     return render(request, 'vehiculo/vehiculo_list.html', {'items': items})
#
# def vehiculo_create(request):
#     if request.method == 'POST':
#         form = VehiculoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('vehiculo_list')
#     else:
#         form = VehiculoForm()
#     return render(request, 'vehiculo/vehiculo_form.html', {'form': form, 'action': 'Crear Vehículo'})
#
# def vehiculo_update(request, pk):
#     item = get_object_or_404(Vehiculo, pk=pk)
#     if request.method == 'POST':
#         form = VehiculoForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('vehiculo_list')
#     else:
#         form = VehiculoForm(instance=item)
#     return render(request, 'vehiculo/vehiculo_form.html', {'form': form, 'action': 'Actualizar Vehículo'})
#
# def vehiculo_delete(request, pk):
#     item = get_object_or_404(Vehiculo, pk=pk)
#     if request.method == 'POST':
#         item.delete()
#         return redirect('vehiculo_list')
#     return render(request, 'vehiculo/vehiculo_confirm_delete.html', {'item': item})
#
# # --- VISTAS PARA USUARIO ---
# def usuario_list(request):
#     items = Usuario.objects.all()
#     return render(request, 'usuario/usuario_list.html', {'items': items})
#
# def usuario_create(request):
#     if request.method == 'POST':
#         form = UsuarioForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('usuario_list')
#     else:
#         form = UsuarioForm()
#     return render(request, 'usuario/usuario_form.html', {'form': form, 'action': 'Crear Usuario'})
#
# def usuario_update(request, pk):
#     item = get_object_or_404(Usuario, pk=pk)
#     if request.method == 'POST':
#         form = UsuarioForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('usuario_list')
#     else:
#         form = UsuarioForm(instance=item)
#     return render(request, 'usuario/usuario_form.html', {'form': form, 'action': 'Actualizar Usuario'})
#
# def usuario_delete(request, pk):
#     item = get_object_or_404(Usuario, pk=pk)
#     if request.method == 'POST':
#         item.delete()
#         return redirect('usuario_list')
#     return render(request, 'usuario/usuario_confirm_delete.html', {'item': item})
