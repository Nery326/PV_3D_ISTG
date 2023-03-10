from django.db import models

# Create your models here.
class eliminacion_compras(models.Model):
    id = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)
    id_compras = models.ForeignKey(compras, on_delete=models.CASCADE)
    motivo_eliminacion = models.CharField(max_length=500)
    fecha_eliminacion = models.TimeField()
    estado = models.IntegerField()

    class Meta: db_table = 'eliminacion_compra'

class eliminacion_ventas(models.Model):
    id = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)
    id_ventas = models.ForeignKey(ventas, on_delete=models.CASCADE)
    motivo_eliminacion = models.CharField(max_length=500)
    fecha_eliminacion = models.TimeField()
    estado = models.IntegerField()

    class Meta: db_table = 'eliminacion_ventas'