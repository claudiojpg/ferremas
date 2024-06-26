from django.db import models

class Producto(models.Model):
    id = models.AutoField(primary_key=True)  
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    cantidad = models.IntegerField(default=0)  

    def __str__(self):
        return self.nombre