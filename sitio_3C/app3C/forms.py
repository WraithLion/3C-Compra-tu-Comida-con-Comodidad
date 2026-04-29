from django import forms
from .models import Cuenta, Repartidor, Platillo, Pedido, Tarjeta, Vehiculo, Usuario

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = '__all__'

class RepartidorForm(forms.ModelForm):
    class Meta:
        model = Repartidor
        fields = '__all__'

class PlatilloForm(forms.ModelForm):
    class Meta:
        model = Platillo
        fields = '__all__'

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = '__all__'

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
