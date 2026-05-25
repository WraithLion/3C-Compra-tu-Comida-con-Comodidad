from django.urls import path
from . import views

urlpatterns = [

    path('',views.sitioPrincipal3C,name='sitioPrincipal_3C'),
    path('cliente/',views.sitioPrincipalCliente,name='sitioPrincipal_Cliente'),
    path('restaurante/',views.sitioPrincipalRestaurante,name='sitioPrincipal_Restaurante'),
    path('repartidor/',views.sitioPrincipalRepartidor,name='sitioPrincipal_Repartidor'),

    path('crearCuenta/tipo', views.crearCuenta, name='tipoCuenta'),
    path('crearCuenta/cliente', views.datosCliente, name='datosCliente'),
    path('crearCuenta/repartidor', views.datosRepartidor, name='datosRepartidor'),
    path('crearCuenta/restaurante', views.datosRestaurante, name='datosRestaurante'),
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

]
