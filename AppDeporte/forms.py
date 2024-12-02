from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    tipo_user = forms.CharField(initial='U', widget=forms.HiddenInput())  # Campo oculto

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


    comuna = forms.ChoiceField(choices=COMU_CHOICES, label="Comuna", widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'comuna', 'phone', 'password1', 'password2','tipo_user')
        labels = {
            'username': 'Nombre',
            'first_name': 'Apellido Paterno',
            'last_name': 'Apellido Materno',
            'email': 'Email',
            'date_of_birth': 'Fecha de nacimiento',
            'gender': 'Género',
            'comuna': 'Comuna',
            'phone': 'Teléfono',
        }

    # Puedes usar widgets personalizados si deseas modificar la apariencia de los campos
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre'
        self.fields['first_name'].label = 'Apellido Paterno'
        self.fields['last_name'].label = 'Apellido Materno'
        self.fields['email'].label = 'Email'
        self.fields['date_of_birth'].label = 'Fecha de nacimiento'
        self.fields['gender'].label = 'Género'
        self.fields['comuna'].label = 'Comuna'
        self.fields['phone'].label = 'Teléfono'

        # Establecer el widget de fecha para el campo date_of_birth
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={
            'type': 'date',  # Esto hará que aparezca un calendario en navegadores compatibles
            'class': 'form-control',  # Puedes agregar clases CSS para estilizar el campo

        })


        # Verificación de que el email no esté registrado ya
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return email
    


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
