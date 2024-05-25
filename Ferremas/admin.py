from django.contrib import admin
from .models import Producto

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio','cantidad')  

admin.site.register(Producto, ProductoAdmin)
