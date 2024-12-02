from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

# modelo personalizado de ususario.

class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True
    )

    # Agregar campos de género y teléfono
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    # Agregar campos de comuna
    COMU_CHOICES = [
        ('Cerro Navia', 'Cerro Navia'),
        ('Conchali', 'Conchali'),
        ('El Bosque', 'El Bosque'),
        ('Estación Central', 'Estación Central'),
        ('Huechuraba', 'Huechuraba'),
        ('Independencia', 'Independencia'),
        ('La Cisterna', 'La Cisterna'),
        ('La Florida', 'La Florida'),
        ('La Granja', 'La Granja'),
        ('La Pintana', 'La Pintana'),
        ('La Reina', 'La Reina'),
        ('Las Condes', 'Las Condes'),
        ('Lo Barnechea', 'Lo Barnechea'),
        ('Lo Espejo', 'Lo Espejo'),
        ('Macul', 'Macul'),
        ('Maipú', 'Maipú'),
        ('Ñuñoa', 'Ñuñoa'),
        ('Pedro Aguirre Cerda', 'Pedro Aguirre Cerda'),
        ('Peñalolén', 'Peñalolén'),
        ('Providencia', 'Providencia'),
        ('Puente Alto', 'Puente Alto'),
        ('Quilicura', 'Quilicura'),
        ('Recoleta', 'Recoleta'),
        ('Renca', 'Renca'),
        ('San Bernardo', 'San Bernardo'),
        ('San Joaquín', 'San Joaquín'),
        ('San Miguel', 'San Miguel'),
        ('San Ramón', 'San Ramón'),
        ('Santiago Centro', 'Santiago Centro'),
        ('Vitacura', 'Vitacura'),

    ]

    # Agregar campos de deporte
    DEPO_CHOICES = [
        ('Baby fútbol', 'Baby fútbol'),
        ('Baloncesto', 'Baloncesto'),
        ('Atletismo', 'Atletismo'),
        ('Voleibol', 'Voleibol'),
        ('Ping-pong', 'Ping-pong'),
        ('Taekwondo', 'Taekwondo'),
        ('Jiu-Jitsu Brasileño', 'Jiu-Jitsu Brasileño'),
        ('Gimnasia', 'Gimnasia'),

    ]

    # Agregar campos de tipo de usuario
    TIPO_CHOICES = [
        ('E', 'Entrenador'),
        ('U', 'Usuario'),

    ]
    
    gender = models.CharField(
        _('gender'),
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,  # Opcional, permite que quede vacío
        null=True
    )

    comuna = models.CharField(
        _('comuna'),
        max_length=25,
        choices=COMU_CHOICES,
        blank=True,  # Opcional, permite que quede vacío
        null=True
    )
    
    phone = models.CharField(
        _('phone'),
        max_length=15,
        blank=True,  # Opcional, permite que quede vacío
        null=True
    )

    date_of_birth = models.DateField(
        _('date of birth'),
        blank=False,  # Requerido en formularios
        null=False,    # No puede ser nulo en la base de datos
        default=timezone.now
    )

    deporte = models.CharField(
        _('deporte'),
        max_length=25,
        choices=DEPO_CHOICES,
        blank=True,  # Opcional, permite que quede vacío
        null=True
    )

    tipo_user = models.CharField(
        _('tipo_user'),
        max_length=1,
        choices=TIPO_CHOICES,
        blank=True,  # Opcional, permite que quede vacío
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


# Modelo Actividad
class Actividad(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    entrenador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'tipo_user': 'entrenador'})
    fecha = models.DateField()
    fecha_fin = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    cupos = models.IntegerField()

    def __str__(self):
        return self.nombre


# Modelo Reserva
class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas')
    actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE)
    fecha_reserva = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.actividad.nombre}"


# Modelo Comentario
class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comentarios')
    actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE, related_name='comentarios')
    contenido = models.TextField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.nombre} en {self.actividad.nombre}"
    

# Modelo Asistencia
class Asistencia(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='asistencias')
    actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE, related_name='asistencias')
    fecha_asistencia = models.DateField(auto_now_add=True)
    presente = models.BooleanField(default=False)

    def __str__(self):
        return f"Asistencia de {self.usuario.nombre} a {self.actividad.nombre}"
