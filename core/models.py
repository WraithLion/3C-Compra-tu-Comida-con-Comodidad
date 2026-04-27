from django.db import models
from django.conf import settings

# Create your models here.


# Modelo para el platillo
class Platillo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
# Modelo para el pedido
class Pedido(models.Model):
    ESTADOS_PEDIDO=[
        ('pendiente','Pendiente'),
        ('pagado','Pagado'),
        ('preparado','Preparado'),
        ('en_camino','En camino'),
        ('entregado','Entregado'),
        ('cancelado','Cancelado'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pedidos'
    )
    fecha_creacion = models.DateTimeField(auto_now_add= True)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def puede_modificarse(self):
        if self.estado == 'pendiente':
            return True
        return False
    
    def puede_cancelarse(self):
        if self.estado == 'pendiente':
            return True
        return False

    def __str__(self):
        return f'Pedido #{self.id} - {self.usuario.username}'
    
# Modelo para el Detalle del Pedido
class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    platillo = models.ForeignKey(
        Platillo,
        on_delete=models.CASCADE,
        related_name='detalles_pedido'
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('pedido','platillo')

    def __str__(self):
        return f'{self.cantidad} x {self.platillo.nombre} en pedido #{self.pedido.id}'
    
# Modelo para el  Pago
class Pago(models.Model):
    METODOS_PAGO = [
        ('tarjeta', 'Tarjeta'),
        ('efectivo', 'Efectivo'),
        ('paypal', 'PayPal'),
        ('mercadopago', 'Mercado Pago'),
    ]

    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='pago'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='pendiente')
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pago del pedido #{self.pedido.id}'