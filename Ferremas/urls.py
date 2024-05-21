from django.urls import path
from . import views

urlpatterns = [
    path('iniciar/', views.mostrar_pagina_pago, name='iniciar_pago'),
    path('procesar/', views.procesar_pago, name='procesar_pago'),
    path('confirmar/', views.confirmar_pago, name='confirmar_pago'),
    path('index/', views.index, name='index'),
    path('carro/', views.mostrar_carrito, name='carro'),
    path('carro/add/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
]
