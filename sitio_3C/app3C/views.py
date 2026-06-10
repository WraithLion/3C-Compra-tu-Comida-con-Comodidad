from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.http import JsonResponse
from decimal import Decimal
import json
import uuid
from django.contrib.auth.decorators import login_required
from .models import Cuenta, Cliente, Repartidor, Restaurante, Platillo, Promociones, Pedido, Orden, Tarjeta, Vehiculo


# --- VISTAS PARA CUENTA ---
def sitioPrincipal3C(request):
    
    return render(request, 'sitio_principal_3C.html', )

def sitioPrincipalCliente(request):

    return render(request, 'cliente/Pantalla_principal_cliente.html', )

# SITIO PARA SESION COMO RESTAURANTE

def sitioPrincipalRestaurante(request):
    restaurante = get_restaurante_actual(request)

    if not restaurante:
        # Si no hay restaurante logueado, redirige al login o inicio
        return redirect('sitioPrincipal_3C')

    # Obtener todos los platillos de este restaurante
    platillos = Platillo.objects.filter(restaurante=restaurante)

    # Pasar los platillos al template
    return render(request, 'restaurante/Pantalla_principal_restaurante.html', {
        'platillos': platillos
    })
#
#
# CONTROLADORES PARA CREAR, MODIFICAR Y ELIMINAR PLATILLO
## --- Vistas para Platillos ---
#

# CONTROLADOR CREAR PLATILLO
def agregar_platillo(request):
    restaurante = get_restaurante_actual(request)
    if not restaurante:
        # Opción A: Redirigir (si el usuario no está logueado)
        return redirect('sitioPrincipal_3C')
        # Opción B: Retornar JSON de error (si prefieres manejarlo en JS)
        # return JsonResponse({'error': 'No identificado'}, status=403)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        imagen = request.FILES.get('imagen')

        # Validación de duplicado
        if Platillo.objects.filter(restaurante=restaurante, nombre=nombre).exists():
            # Si usas fetch, devuelve JSON
            return JsonResponse({'error': 'Este platillo ya existe.'}, status=400)

        # Generar ID único
        nuevo_id = f"PLT-{uuid.uuid4().hex[:8].upper()}"

        try:
            Platillo.objects.create(
                IDelemento=nuevo_id,
                restaurante=restaurante,
                nombre=nombre,
                precio=precio,
                imagen=imagen
            )
            # Éxito: El frontend recargará la página
            return JsonResponse({'success': True,'message':'Se ha creado el platillo con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return redirect('sitioPrincipal_Restaurante')

# CONTROLADOR MODIFICAR PLATILLO

def modificar_platillo(request, id_elemento):
    restaurante = get_restaurante_actual(request)
    if not restaurante:
        return redirect('sitioPrincipal_3C')

    try:
        platillo = Platillo.objects.get(IDelemento=id_elemento, restaurante=restaurante)
    except Platillo.DoesNotExist:
        return JsonResponse({'error': 'Platillo no encontrado.'}, status=404)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        imagen = request.FILES.get('imagen')

        # Validar duplicado (excluyendo el actual)
        if Platillo.objects.filter(restaurante=restaurante, nombre=nombre).exclude(IDelemento=id_elemento).exists():
            return JsonResponse({'error': 'Ya existe otro platillo con ese nombre.'}, status=400)

        platillo.nombre = nombre
        platillo.precio = precio
        if imagen:
            platillo.imagen = imagen
        platillo.save()
        return JsonResponse({'success': True,'message':'Se han aplicado los cambios con éxito'})

    return redirect('sitioPrincipal_Restaurante')

# CONTROLADOR ELIMINAR PLATILLO


def eliminar_platillo(request, id_elemento):
    restaurante = get_restaurante_actual(request)
    if not restaurante:
        return redirect('sitioPrincipal_3C')

    try:
        platillo = Platillo.objects.get(IDelemento=id_elemento, restaurante=restaurante)

        #  Borra el archivo físico de la imagen si existe
        if platillo.imagen:
            # save=False evita que Django intente hacer un .save() automático
            # en un objeto que estamos a punto de destruir
            platillo.imagen.delete(save=False)

        # Ahora sí, borramos el registro de la base de datos
        platillo.delete()

        return JsonResponse({'success': True, 'message': 'El platillo se ha quitado del menú'})
    except Platillo.DoesNotExist:
        return JsonResponse({'error': 'Platillo no encontrado.'}, status=404)


# # # # SITIO PROMOCIONES COMO RESTAURANTE
# # # #
# # # #

def promocionesRestaurante(request):
    restaurante = get_restaurante_actual(request)
    if not restaurante:
        return redirect('sitioPrincipal_3C')

    promociones_raw = Promociones.objects.filter(platillo__restaurante=restaurante)

    # Le agregamos de forma dinámica el precio calculado a cada objeto promoción
    for promo in promociones_raw:
        if promo.tipo == 'descuento':
            try:
                porcentaje = int(str(promo.valor).replace('%', '').strip())

                # CORRECCIÓN: Convertimos la operación matemática a Decimal
                factor_descuento = Decimal(1 - (porcentaje / 100))
                descuento = promo.platillo.precio * factor_descuento

                promo.precio_descuento = round(descuento, 2)
            except ValueError:
                promo.precio_descuento = promo.platillo.precio
        else:
            promo.precio_descuento = None

    # El resto de tu lógica de exclusión de platillos se queda exactamente IGUAL...
    promociones_existentes = promociones_raw
    platillos_con_promo = promociones_existentes.values_list('platillo_id', flat=True)
    platillos_disponibles = Platillo.objects.filter(restaurante=restaurante).exclude(id__in=platillos_con_promo)

    context = {
        'promociones_existentes': promociones_existentes,
        'platillos_disponibles': platillos_disponibles
    }
    return render(request, 'restaurante/Pantalla_promociones_restaurante.html', context)

# # # # VER PROMOCIONES DEL RESTAURANTE
# # # #
# # # #
def vista_promociones(request):
    restaurante = get_restaurante_actual(request)
    if not restaurante:
        return redirect('sitioPrincipal_3C')

    promociones_existentes = Promociones.objects.filter(platillo__restaurante=restaurante)

    # 1. Traemos TODOS los platillos de la base de datos sin filtrar por restaurante
    # para comprobar si es un problema de asignación de ID de restaurante.
    platillos_disponibles = Platillo.objects.all()

    context = {
        'promociones_existentes': promociones_existentes,
        'platillos_disponibles': platillos_disponibles
    }
    return render(request, 'promocionesRestaurante.html', context)

# # # # # # # CONTROLADORES PARA CREAR, MODIFICAR Y ELIMINAR PROMOCIONES # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# CONTROLADOR CREAR PROMOCIÓN

def agregar_promocion(request):
    # 1. Recuperamos el restaurante activo de la sesión
    restaurante = get_restaurante_actual(request)
    if not restaurante:
        return JsonResponse({'success': False, 'error': 'No se detectó una sesión activa de restaurante.'}, status=403)

    if request.method == 'POST':
        try:
            # 2. Parseamos los datos que envió el Fetch desde JS
            data = json.loads(request.body)
            platillo_id = data.get('platillo_id') # Este es el ID que viene de la tarjeta
            tipo = data.get('tipo')              # 'combo' o 'descuento'
            valor = data.get('valor')             # '2x1', '10%', etc.

            # Validación de seguridad básica
            if not platillo_id or not tipo or not valor:
                return JsonResponse({'success': False, 'error': 'Faltan campos obligatorios en la petición.'}, status=400)

            # 3. Intentamos buscar el platillo usando tu campo personalizado 'IDelemento'
            try:
                platillo = Platillo.objects.get(IDelemento=platillo_id, restaurante=restaurante)
            except Platillo.DoesNotExist:
                # Plan B: Si por alguna razón tu JS leyó el ID automático numérico, buscamos por id
                try:
                    platillo = Platillo.objects.get(id=platillo_id, restaurante=restaurante)
                except (Platillo.DoesNotExist, ValueError):
                    return JsonResponse({
                        'success': False,
                        'error': f'No se encontró el platillo con ID "{platillo_id}" para este restaurante.'
                    }, status=404)

            # 4. Creamos el registro en la tabla de Promociones
            # NOTA: Revisa que los nombres de los campos (platillo, tipo, valor) coincidan con tu modelo Promociones
            nueva_promo = Promociones.objects.create(
                platillo=platillo,
                tipo=tipo,
                valor=valor
            )

            # 5. Si todo salió bien, respondemos con JSON puro
            return JsonResponse({
                'success': True,
                'message': f'La promoción se ha creado con éxito'
            })

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'El cuerpo de la petición no es un JSON válido.'}, status=400)
        except Exception as e:
            # ¡EL SALVAVIDAS!: Si Python falla por cualquier otra cosa (ej. error de tipado en la BD),
            # te mandará el mensaje exacto al frontend en vez de tirar un Error 500 oculto.
            return JsonResponse({'success': False, 'error': f'Error interno en el servidor: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

# CONTROLADOR MODIFICAR PROMOCIÓN
def modificar_promocion(request, promo_id):
    """
    Vista para modificar una promoción existente.
    Recibe el ID desde la URL y los datos (tipo, valor) desde el JSON.
    """
    restaurante = get_restaurante_actual(request)
    if not restaurante:
        return JsonResponse({'success': False, 'error': 'No autorizado.'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tipo = data.get('tipo')
            valor = data.get('valor')

            if not tipo or not valor:
                return JsonResponse({'success': False, 'error': 'Faltan campos tipo o valor.'}, status=400)

            # Buscamos la promoción usando el ID de la URL y validamos propiedad
            try:
                promocion = Promociones.objects.get(id=promo_id, platillo__restaurante=restaurante)
            except Promociones.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Promoción no encontrada.'}, status=404)

            # Actualizamos
            promocion.tipo = tipo
            promocion.valor = valor
            promocion.save()

            return JsonResponse({
                'success': True,
                'message': 'Promoción modificada correctamente.'
            })

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error interno: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)


# # # # # # ELIMINAR PROMOCIÓN
# # # # # #
# # # # # #

# Asegúrate de tener importado json y JsonResponse
def eliminar_promocion(request):
    restaurante = get_restaurante_actual(request)
    if not restaurante:
        return JsonResponse({'success': False, 'error': 'No autorizado.'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Recibimos el ID de la promoción que pusiste en el data-promo-id del HTML
            promo_id = data.get('promo_id')

            if not promo_id:
                return JsonResponse({'success': False, 'error': 'No se proporcionó el ID de la promoción.'}, status=400)

            # Buscamos la promoción asegurándonos de que el platillo pertenezca a este restaurante
            try:
                # Asegúrate de que la búsqueda sea id=promo_id
                promocion = Promociones.objects.get(id=promo_id, platillo__restaurante=restaurante)
                promocion.delete() # ¡La borramos de la BD!

                return JsonResponse({'success': True, 'message': 'La promoción se ha eliminado'})
            except Promociones.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'La promoción no existe o no tienes permiso para borrarla.'}, status=404)

        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error interno: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

# --- Helper para obtener el Restaurante actual ---
def get_restaurante_actual(request):
    """Recupera el objeto Restaurante basado en el usuario de la sesión."""
    username = request.session.get('username')
    if not username:
        return None
    # Busca la cuenta con ese usuario y luego el restaurante asociado
    try:
        cuenta = Cuenta.objects.get(usuario=username)
        return Restaurante.objects.get(IDcuenta=cuenta)
    except (Cuenta.DoesNotExist, Restaurante.DoesNotExist):
        return None

# # # INICIAR SESIÓN

def validar_login(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        contrasena = request.POST.get('contrasena')
        user = authenticate(request, username=nombre, password=contrasena)
        if user is not None and hasattr(user, 'restaurante'): # Asegúrate que el usuario sea un Restaurante
            # login(request, user) # Opcional: si usas sesión
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Credenciales inválidas o no es un restaurante.'}, status=401)
    return JsonResponse({'error': 'Método no permitido'}, status=405)



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
