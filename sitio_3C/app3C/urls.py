from django.urls import path
from . import views

urlpatterns = [

    path('',views.sitioPrincipal3C,name='sitioPrincipal_3C'),
    path('cliente/',views.sitioPrincipalCliente,name='sitioPrincipal_Cliente'),
    path('restaurante/',views.sitioPrincipalRestaurante,name='sitioPrincipal_Restaurante'),
    path('repartidor/',views.sitioPrincipalRepartidor,name='sitioPrincipal_Repartidor'),
    
    
]
