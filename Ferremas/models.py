from django.db import models

class Producto(models.Model):
    id = models.AutoField(primary_key=True)  # Definir explícitamente el campo id autoincrementable
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()

    def __str__(self):
        return self.nombre
