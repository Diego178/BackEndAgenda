from django.db import models

class Asesor(models.Model):
    id_asesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    idioma = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'asesor'

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    matricula = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'usuario'
