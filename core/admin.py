from django.contrib import admin
from .models import Platillo, Pedido, DetallePedido, Pago

# Register your models here.

admin.site.register(Platillo)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Pago)
