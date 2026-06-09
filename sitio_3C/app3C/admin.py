from django.contrib import admin
from .models import Cuenta, Cliente, Repartidor, Restaurante, Platillo, Pedido, Orden, Tarjeta, Vehiculo, Promociones
# Register your models here.
# Registro básico
admin.site.register(Restaurante)
admin.site.register(Platillo)
admin.site.register(Promociones)
