from django.urls import path
from . import views

urlpatterns = [

    path('',views.sitioPrincipal3C,name='sitioPrincipal_3C'),
    # Cuenta
    path('cuenta/', views.cuenta_list, name='cuenta_list'),
    path('cuenta/crear/', views.cuenta_create, name='cuenta_create'),
    path('cuenta/<int:pk>/editar/', views.cuenta_update, name='cuenta_update'),
    path('cuenta/<int:pk>/eliminar/', views.cuenta_delete, name='cuenta_delete'),

    # Repartidor
    path('repartidor/', views.repartidor_list, name='repartidor_list'),
    path('repartidor/crear/', views.repartidor_create, name='repartidor_create'),
    path('repartidor/<int:pk>/editar/', views.repartidor_update, name='repartidor_update'),
    path('repartidor/<int:pk>/eliminar/', views.repartidor_delete, name='repartidor_delete'),

    # Platillo
    path('platillo/', views.platillo_list, name='platillo_list'),
    path('platillo/crear/', views.platillo_create, name='platillo_create'),
    path('platillo/<int:pk>/editar/', views.platillo_update, name='platillo_update'),
    path('platillo/<int:pk>/eliminar/', views.platillo_delete, name='platillo_delete'),

    # Pedido
    path('pedido/', views.pedido_list, name='pedido_list'),
    path('pedido/crear/', views.pedido_create, name='pedido_create'),
    path('pedido/<int:pk>/editar/', views.pedido_update, name='pedido_update'),
    path('pedido/<int:pk>/eliminar/', views.pedido_delete, name='pedido_delete'),

    # Tarjeta
    path('tarjeta/', views.tarjeta_list, name='tarjeta_list'),
    path('tarjeta/crear/', views.tarjeta_create, name='tarjeta_create'),
    path('tarjeta/<int:pk>/editar/', views.tarjeta_update, name='tarjeta_update'),
    path('tarjeta/<int:pk>/eliminar/', views.tarjeta_delete, name='tarjeta_delete'),

    # Vehiculo
    path('vehiculo/', views.vehiculo_list, name='vehiculo_list'),
    path('vehiculo/crear/', views.vehiculo_create, name='vehiculo_create'),
    path('vehiculo/<int:pk>/editar/', views.vehiculo_update, name='vehiculo_update'),
    path('vehiculo/<int:pk>/eliminar/', views.vehiculo_delete, name='vehiculo_delete'),

    # Usuario
    path('usuario/', views.usuario_list, name='usuario_list'),
    path('usuario/crear/', views.usuario_create, name='usuario_create'),
    path('usuario/<int:pk>/editar/', views.usuario_update, name='usuario_update'),
    path('usuario/<int:pk>/eliminar/', views.usuario_delete, name='usuario_delete'),
]
