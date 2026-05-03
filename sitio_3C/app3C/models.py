from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

class Cuenta(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50)
    correo = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)
    teléfono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)
    CURP = models.CharField(max_length=18)

    def __str__(self):
        return self.nombre
        

class Cliente(models.Model):
    cuenta = models.OneToOneField(Cuenta, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.nombre

class Restaurante(models.Model):
    cuenta = models.OneToOneField(Cuenta, on_delete=models.CASCADE,null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class Repartidor(models.Model):
    cuenta = models.OneToOneField(Cuenta, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.nombre   
                                                
                                                                        
class Platillo(models.Model):
    IDelemento = models.CharField(max_length=100,null=False)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='platillos',null=False)
    imagen = models.ImageField(upload_to='platillos/', null=False, blank=True)
    nombre = models.CharField(max_length=100,null=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

        
class Pedido(models.Model):
    IDpedido = models.CharField(max_length=100)
    userCliente = models.CharField(max_length=100)

    def __str__(self):
        return self.IDpedido
        
class Tarjeta(models.Model):
    numero = models.CharField(max_length=16)
    usuario = models.CharField(max_length=100)
    titular = models.CharField(max_length=100)
    vencimiento = models.CharField(max_length=5)  # Formato MM/AA
    ccv = models.CharField(max_length=4)

    def __str__(self):
        return f"Tarjeta de {self.titular}"
        
class Vehiculo(models.Model):
    tipo = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    color = models.CharField(max_length=30)
    placa = models.CharField(max_length=10)

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
        




        


