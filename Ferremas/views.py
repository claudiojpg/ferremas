from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse  # Importar JsonResponse desde django.http
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
from django.conf import settings
from .models import Producto

def mostrar_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())
    cantidades = {int(k): v for k, v in carrito.items()}
    total = sum(producto.precio * cantidades[producto.id] for producto in productos)

    return render(request, 'website/carro.html', {
        'productos': productos,
        'cantidades': cantidades,
        'total': total,
    })

def add_to_cart(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id_str = str(producto_id)
    if producto_id_str in carrito:
        carrito[producto_id_str] += 1
    else:
        carrito[producto_id_str] = 1
    request.session['carrito'] = carrito
    cart_count = sum(carrito.values())
    return JsonResponse({'cart_count': cart_count})

def index(request):
    return render(request, 'website/index.html')

def mostrar_pagina_pago(request):
    return render(request, 'pagos/iniciar_pago.html')

def procesar_pago(request):
    if request.method == 'POST':
        try:
            carrito = request.session.get('carrito', {})
            if not carrito:
                return HttpResponse("El carrito está vacío.")
            
            total = sum(Producto.objects.get(id=int(prod_id)).precio * cantidad for prod_id, cantidad in carrito.items())
            
            buy_order = "ordenCompra123"
            session_id = "sesion123"
            amount = total  
            return_url = request.build_absolute_uri('/pagos/confirmar/')

            # Crear la transacción
            tx = Transaction(WebpayOptions(settings.TRANBANK_COMMERCE_CODE, settings.TRANBANK_API_KEY, IntegrationType.TEST))
            response = tx.create(buy_order, session_id, amount, return_url)
            if response:
                return redirect(response['url'] + "?token_ws=" + response['token'])
            else:
                return HttpResponse("No se recibió respuesta de Transbank.")
        except Producto.DoesNotExist:
            return HttpResponse("Producto no encontrado.")
        except Exception as e:
            return HttpResponse(f"Error interno: {str(e)}")
    return HttpResponse("Método no permitido", status=405)

def confirmar_pago(request):
    token_ws = request.GET.get('token_ws')
    if not token_ws:
        return HttpResponse("Token no proporcionado.")

    try:
        tx = Transaction(WebpayOptions(settings.TRANBANK_COMMERCE_CODE, settings.TRANBANK_API_KEY, IntegrationType.TEST))
        response = tx.commit(token_ws)
        if response:
            return HttpResponse(f"Transacción confirmada con éxito. Detalles: {response}")
        else:
            return HttpResponse("No se recibió respuesta de Transbank.")
    except Exception as e:
        return HttpResponse(f"Error interno: {str(e)}")