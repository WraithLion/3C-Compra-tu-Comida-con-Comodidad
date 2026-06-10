from django.urls import path
from . import views

urlpatterns = [

    path('',views.sitioPrincipal3C,name='sitioPrincipal_3C'),
    path('cliente/',views.sitioPrincipalCliente,name='sitioPrincipal_Cliente'),
    path('restaurante/',views.sitioPrincipalRestaurante,name='sitioPrincipal_Restaurante'),
    path('restaurante/promociones/',views.promocionesRestaurante,name="promocionesRestaurante"),
    path('repartidor/',views.sitioPrincipalRepartidor,name='sitioPrincipal_Repartidor'),
    path('crearCuenta/tipo', views.tipoCuenta, name='tipoCuenta'),
    path('crearCuenta/cliente', views.datosCliente, name='datosCliente'),
    path('crearCuenta/repartidor', views.datosRepartidor, name='datosRepartidor'),

    path('crearCuenta/restaurante', views.datosRestaurante, name='datosRestaurante'),

    # Rutas para Platillos
    path('restaurante/platillos/agregar/', views.agregar_platillo, name='agregar_platillo'),
    # Nota: Para modificar y eliminar, se hará uso del ID en la URL.
    # El frontend enviará POST a estas rutas con el ID.
    path('restaurante/platillos/<str:id_elemento>/modificar/', views.modificar_platillo, name='modificar_platillo'),
    path('restaurante/platillos/<str:id_elemento>/eliminar/', views.eliminar_platillo, name='eliminar_platillo'),

    # Rutas para Promociones

    path('restaurante/promociones/agregar/', views.agregar_promocion, name='agregar_promocion'),
    path('restaurante/promociones/<int:promo_id>/modificar/', views.modificar_promocion, name='modificar_promocion'),
    path('restaurante/promociones/eliminar/', views.eliminar_promocion, name='eliminar_promocion'),
# # #     Tarjetas

    path('crearCuenta/tarjeta', views.datosTarjeta, name='datosTarjeta'),
    path('crearCuenta/vehiculo', views.datosVehiculo, name='datosVehiculo'),

    path('carrito/', views.carrito, name='carrito'),
    path('pedido/direccion', views.direccionEntrega, name='direccionEntrega'),
    path('pedido/pago', views.metodoPago, name='metodoPago'),
    path('cliente/pedido', views.pedidoCliente, name='estadoPedidoCliente'),

    path('user/modificarCuenta', views.modificarCuenta, name='modificarCuenta'),
    path('user/eliminarCuenta', views.eliminarCuenta, name='eliminarCuenta'),

    path('repartidor/pendientes', views.pedidosPendientes, name='pedidosPendientes'),
    path('repartidor/pedido', views.pedidoRepartidor, name='pedidoRepartidor'),

    path('restaurante/ordenes', views.ordenes, name='ordenesPendientes'),

    path('cliente/carrito', views.carrito, name='carritoSinSesion')
]
