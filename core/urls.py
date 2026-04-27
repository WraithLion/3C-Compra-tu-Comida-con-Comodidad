"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name = "home"),
    path("registro/", views.register_view, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("pedidos/", views.lista_pedidos, name="lista_pedidos"),
    path("pedidos/crear/", views.crear_pedido,name='crear_pedido'),
    path("pedidos/<int:pedido_id>/",views.detalle_pedido, name="detalle_pedido"),
    path('pedidos/<int:pedido_id>/editar/', views.editar_pedido, name='editar_pedido'),
    path('pedidos/<int:pedido_id>/cancelar/', views.cancelar_pedido, name='cancelar_pedido'),
]
