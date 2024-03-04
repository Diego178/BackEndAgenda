from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    matricula = models.CharField(max_length=10)
    password = models.CharField(max_length=16)
    email = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'usuario'