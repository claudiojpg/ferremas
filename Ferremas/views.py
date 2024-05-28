from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse  
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
from django.conf import settings
from django.urls import reverse
from .models import Producto
import hashlib

def index(request):
    productos = Producto.objects.all()  
    carrito = request.session.get('carrito', {})
    total_productos = sum(carrito.values())
    mensaje = request.session.pop('mensaje', None)
        
 
    return render(request, 'website/index.html', {
        'productos': productos,
        'total_productos': total_productos,
        'mensaje': mensaje,
    })

def agregar_al_carrito(request):
    if request.method == "POST":
        producto_id = request.POST.get('producto_id')
        carrito = request.session.get('carrito', {})
        total_productos = sum(carrito.values())

        if total_productos < 10:
            if producto_id in carrito:
                carrito[producto_id] += 1
            else:
                carrito[producto_id] = 1
            request.session['carrito'] = carrito
        else:
            request.session['mensaje'] = "No puedes añadir más de 10 productos en una sola compra."

    return redirect('index')

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

def iniciar_pago(request):
    if request.method == "POST":
        carrito = request.session.get('carrito', {})
        productos = Producto.objects.filter(id__in=carrito.keys())
        cantidades = {int(k): v for k, v in carrito.items()}
        total = sum(producto.precio * cantidades[producto.id] for producto in productos)
        
        if total > 0:
            session_key = request.session.session_key
            buy_order = hashlib.md5(session_key.encode()).hexdigest()[:26]
            session_id = f"sesion_{session_key}"
            amount = total
            return_url = request.build_absolute_uri(reverse('confirmar_pago'))

            tx = Transaction(WebpayOptions(settings.TRANBANK_COMMERCE_CODE, settings.TRANBANK_API_KEY, IntegrationType.TEST))
            try:
                response = tx.create(buy_order, session_id, amount, return_url)
                if response:
                    return redirect(response['url'] + "?token_ws=" + response['token'])
                else:
                    return HttpResponse("No se recibió respuesta de Transbank.")
            except Exception as e:
                return HttpResponse(f"Error interno: {str(e)}")
        else:
            return HttpResponse("El carrito está vacío.")
    else:
        return HttpResponse("Método no permitido.", status=405)

def confirmar_pago(request):
    token_ws = request.GET.get('token_ws')
    if not token_ws:
        return HttpResponse("Token no proporcionado.")

    try:
        tx = Transaction(WebpayOptions(settings.TRANBANK_COMMERCE_CODE, settings.TRANBANK_API_KEY, IntegrationType.TEST))
        response = tx.commit(token_ws)
        if response and response['status'] == 'AUTHORIZED':
            
            carrito = request.session.get('carrito', {})
            productos = Producto.objects.filter(id__in=carrito.keys())
            for producto in productos:
                producto.cantidad -= carrito[str(producto.id)]
                producto.save()
            
         
            del request.session['carrito']

            return render(request, 'website/confirmacion_pago.html', {'response': response})
        else:
            return HttpResponse("No se recibió respuesta de Transbank.")
    except Exception as e:
        return HttpResponse(f"Error interno: {str(e)}")

def vaciar_carrito(request):
    if 'carrito' in request.session:
        del request.session['carrito']
    return redirect('mostrar_carrito')
