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

class Diahora(models.Model):
    id_diahora = models.AutoField(primary_key=True)
    dia = models.CharField(max_length=15, blank=True, null=True)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_termino = models.TimeField(blank=True, null=True)
    modalidad = models.CharField(max_length=15, blank=True, null=True)
    estado = models.CharField(max_length=15, blank=True, null=True)
    eslibre = models.CharField(db_column='esLibre', max_length=15, blank=True, null=True)  # Field name made lowercase.
    idasesor = models.ForeignKey(Asesor, models.CASCADE, db_column='idAsesor', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'diahora'

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    matricula = models.CharField(max_length=10)
    password = models.CharField(max_length=16)
    email = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'usuario'

class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    nombrecurso = models.CharField(db_column='nombreCurso', max_length=20, blank=True, null=True)  # Field name made lowercase.
    idasesor = models.ForeignKey(Asesor, models.CASCADE, db_column='idAsesor', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'curso'

        
class Asesoria(models.Model):
    id_asesoria = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10)
    tema = models.CharField(max_length=200)
    fecha = models.DateField()
    escancelada = models.CharField(db_column='esCancelada', max_length=15, blank=True, null=True) 
    idasesor = models.ForeignKey(Asesor, models.CASCADE, db_column='idAsesor', blank=True, null=True)  # Field name made lowercase.
    iddiahora = models.ForeignKey(Diahora, models.CASCADE, db_column='idDiaHora', blank=True, null=True)  # Field name made lowercase.
    idusuario = models.ForeignKey(Usuario, models.CASCADE, db_column='idUsuario', blank=True, null=True)  # Field name made lowercase.
    idcurso = models.ForeignKey(Curso, models.CASCADE, db_column='idCurso', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'asesoria'

class Datosreunionvirtual(models.Model):
    id_datosreunion = models.AutoField(primary_key=True)
    url = models.CharField(db_column='URL', max_length=150, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=15, blank=True, null=True)
    id_reunion = models.CharField(max_length=20, blank=True, null=True)
    idasesor = models.ForeignKey(Asesor, models.CASCADE, db_column='idAsesor', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'datosreunionvirtual'