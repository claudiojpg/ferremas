from django.urls import include, path
from django.conf.urls.static import static

from miwebpay import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agregar/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carro/', views.mostrar_carrito, name='mostrar_carrito'),
    path('vaciar/', views.vaciar_carrito, name='vaciar_carrito'),  
    path('pagos/iniciar/', views.iniciar_pago, name='iniciar_pago'),
    path('pagos/confirmar/', views.confirmar_pago, name='confirmar_pago'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)