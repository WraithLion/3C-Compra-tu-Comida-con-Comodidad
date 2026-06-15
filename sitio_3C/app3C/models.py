import os
import uuid
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

class Cuenta(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50)
    correo = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)
    teléfono = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre
        

class Cliente(models.Model):
    IDcuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='clientes', null=False, default=1)

    def __str__(self):
        return self.IDcuenta.__str__

class Restaurante(models.Model):
    IDcuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='restaurantes', null=False, default=1)
    direccion = models.CharField(max_length=200, default='')
    
    def __str__(self):
        # Muestra: "Nombre del Restaurante (Dirección)"
        return f"{self.IDcuenta.nombre} - {self.direccion}"

class Repartidor(models.Model):
    IDcuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='repartidores', null=False, default=1)
    CURP = models.CharField(max_length=18, default='000000000000000000')

    def __str__(self):
        return self.IDcuenta
                                                
# Asignar un id a las imagenes de los platillos
#

def obtener_nombre_unico(instance, filename):
    """
    Genera un nombre de archivo único usando UUID.
    Mantiene la extensión original del archivo.
    """
    # Extraer la extensión del archivo original
    ext = os.path.splitext(filename)
    # Generar un UUID único
    nuevo_nombre = f"{uuid.uuid4().hex}{ext}"
    # Retornar la ruta completa dentro de la carpeta 'platillos/'
    return os.path.join('platillos', nuevo_nombre)

                                                                        
class Platillo(models.Model):
    IDelemento = models.CharField(max_length=100,null=False)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='platillos', null=False, default=1)
    nombre = models.CharField(max_length=100,null=False)
    imagen = models.ImageField(upload_to=obtener_nombre_unico, null=True, blank=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombre

class Promociones(models.Model):

    IDelemento = models.CharField(max_length=25,null=False)

    # Relación correcta: Una promoción pertenece a un Platillo específico
    platillo = models.ForeignKey(
        Platillo,
        on_delete=models.CASCADE,
        related_name='promociones' # Esto te permitirá hacer: mi_platillo.promociones.all()
    )


    # Opciones para el campo 'tipo'
    TIPO_PROMOCION = [
        ('descuento', 'Descuento'),
        ('combo', 'Combo'),
    ]



    # Uso de choices para restringir los valores
    tipo = models.CharField(
        max_length=9,
        choices=TIPO_PROMOCION,
        default='descuento'
    )

    valor = models.CharField(
        max_length=20,
        null=False,
        help_text="Porcentaje (ej: 15) o promoción (ej: 2x1, 3x2)"
    )

    def __str__(self):
        if self.tipo == 'descuento':
            return f"{self.valor}% de descuento en {self.platillo.nombre}"
        else:
            return f"Combo {self.valor} en {self.platillo.nombre}"

    def obtener_imagen(self):
        return self.platillo.imagen

        
class Pedido(models.Model):
    IDpedido = models.CharField(max_length=100)
    userCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos', null=False, default=1)
    activo = models.BooleanField(default=False)
    repAsignado = models.ForeignKey(Repartidor, on_delete=models.SET_NULL, related_name='pedidos', null=True, blank=True)

    def __str__(self):
        return self.IDpedido

class Orden(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='ordenes', null=False, default=1)
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE, related_name='ordenes', null=False, default=1)
    copias = models.PositiveIntegerField()
        
class Tarjeta(models.Model):
    numero = models.CharField(max_length=16)
    usuario = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='tarjetas', null=False, default=1)
    titular = models.CharField(max_length=100)
    vencimiento = models.CharField(max_length=5)  # Formato MM/AA
    ccv = models.CharField(max_length=4)

    def __str__(self):
        return f"Tarjeta de {self.titular}"
        
class Vehiculo(models.Model):
    tipo = models.CharField(max_length=25)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=15)
    placa = models.CharField(max_length=7)
    propietario = models.ForeignKey(Repartidor, on_delete=models.CASCADE, related_name='vehiculos', null=False, default=1)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"
        
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    correo = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)
    teléfono = models.IntegerField()

    def __str__(self):
        return self.nombre
        





        


