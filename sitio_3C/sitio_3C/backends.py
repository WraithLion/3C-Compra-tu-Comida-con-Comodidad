from django.contrib.auth.hashers import check_password
from .models import Cuenta

class CuentaBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            cuenta = Cuenta.objects.get(usuario=username)
            if cuenta.contraseña == password:  # Considera usar hash con check_password
                return cuenta
        except Cuenta.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Cuenta.objects.get(pk=user_id)
        except Cuenta.DoesNotExist:
            return None
