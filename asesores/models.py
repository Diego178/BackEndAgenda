from django.db import models


class Asesor(models.Model):
    id_asesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    idioma = models.CharField(max_length=15)
    email = models.EmailField(max_length=45)
    password = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'asesor'

class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    nombrecurso = models.CharField(db_column='nombreCurso', max_length=20, blank=True, null=True)  # Field name made lowercase.
    idasesor = models.ForeignKey(Asesor, models.CASCADE, db_column='idAsesor', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'curso'

class Datosreunionvirtual(models.Model):
    id_datosreunion = models.AutoField(primary_key=True)
    url = models.CharField(db_column='URL', max_length=150, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=15, blank=True, null=True)
    id_reunion = models.CharField(max_length=20, blank=True, null=True)
    idasesor = models.ForeignKey(Asesor, models.CASCADE, db_column='idAsesor', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'datosreunionvirtual'
