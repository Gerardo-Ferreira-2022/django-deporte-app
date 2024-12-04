from django.shortcuts import render, redirect
from AppDeporte.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.views import View
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Actividad
from datetime import timedelta

# Create your views here.

# Vista home.
def home(request):
    return render(request, 'home.html')


# Vista dashboard.
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# Vista registro.
class RegisterView(View):
    template_name = 'register.html'  # Tu plantilla HTML para el formulario

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Usuario registrado exitosamente. ¡Ahora puedes iniciar sesión!")
                return redirect('login')  # Cambia 'login' por el nombre de tu vista de inicio de sesión
            else:
                messages.error(request, "Por favor, corrige los errores en el formulario.")
        except Exception as e:
            # Captura cualquier error inesperado
            messages.error(request, f"Ha ocurrido un error inesperado: {str(e)}")
        return render(request, self.template_name, {'form': form})
    


def login_view(request):
    if request.method == 'POST':
        print("Método POST recibido")  # Verificar si entra al POST
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(f"Usuario autenticado: {user.username}")
            return redirect('dashboard')
        else:

            return render(request, 'login.html', {
                'error_message': 'Usuario o contraseña incorrectos.'
            })
    else:

        return render(request, 'login.html')


def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige al login o a la página de inicio


# Vista actividad.
@login_required
def actividad(request):
    actividades = Actividad.objects.all()
    
    # Formatear las fechas para FullCalendar
    actividades_formateadas = []
    for actividad in actividades:
        # Asegurarse de que la fecha es de tipo datetime y agregar la hora si no existe
        start_datetime = timezone.make_aware(
            timezone.datetime.combine(actividad.fecha, timezone.datetime.min.time())
        ).strftime('%Y-%m-%dT%H:%M')  # Formato para FullCalendar
        end_datetime = timezone.make_aware(
            timezone.datetime.combine(actividad.fecha_fin, timezone.datetime.min.time())
        ).strftime('%Y-%m-%dT%H:%M')
        
        actividades_formateadas.append({
            'nombre': actividad.nombre,
            'start': start_datetime,
            'end': end_datetime
        })
    
    return render(request, 'actividad.html', {
        'actividades': actividades_formateadas
    })


# Vista usuarios.
@login_required
def usuarios(request):
    usuarios = User.objects.all()

    # Conteos
    total_usuarios = usuarios.count()-1
    total_entrenadores = usuarios.filter(tipo_user='E').count()  # Asumiendo 'E' para Entrenador
    total_usuarios_generales = usuarios.filter(tipo_user='U').count()  # Asumiendo 'U' para Usuario

    # Cálculo de porcentajes
    porcentaje_entrenadores = (total_entrenadores / total_usuarios) * 100 if total_usuarios > 0 else 0
    porcentaje_usuarios = (total_usuarios_generales / total_usuarios) * 100 if total_usuarios > 0 else 0

    # Pasar todo al contexto
    context = {
        'usuarios': usuarios,
        'porcentaje_entrenadores': round(porcentaje_entrenadores, 1),
        'porcentaje_usuarios': round(porcentaje_usuarios, 1),
    }
    return render(request, 'usuarios.html', context)


# actualizar usuario
@login_required
def actualizar_usuario(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        tipo_user = request.POST.get('tipo_user')
        deporte = request.POST.get('deporte')
        is_active = request.POST.get('is_active') == 'True'

        # Obtener el usuario y actualizar los campos
        user = get_object_or_404(User, id=user_id)
        user.tipo_user = tipo_user
        user.deporte = deporte
        user.is_active = is_active
        user.save()

        # Agregar un mensaje de éxito
        messages.success(request, 'Usuario actualizado correctamente')

        # Redirigir a la página de usuarios
        return redirect('usuarios')  # Redirigir a la lista de usuarios

    else:
        return redirect('usuarios')  # Si no es un POST, redirigir a la vista de usuarios
    

#eliminar usuario
@login_required
def eliminar_usuario(request, user_id):
    # Verificar si el usuario existe
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        try:
            # Eliminar al usuario
            user.delete()
            messages.success(request, 'Usuario eliminado correctamente.')
            return redirect('usuarios')  # Redirigir a la lista de usuarios o donde sea necesario
        except:
            messages.error(request, 'Ocurrió un error al eliminar el usuario.')
            return redirect('usuarios')  # Redirigir en caso de error
        


#insertar actividad
@login_required
def crear_actividad(request):
    if request.method == 'POST':
        try:
            # Recibir los datos del formulario
            activity_name = request.POST.get('actividad_nombre')
            description = request.POST.get('descripcion')
            start_date = request.POST.get('fecha_inicio')
            end_date = request.POST.get('fecha_fin')
            day_of_week = int(request.POST.get('dia'))  # Día de la semana (1=lunes, 7=domingo)
            start_time = request.POST.get('hora_inicio')
            end_time = request.POST.get('hora_fin')
            capacity = int(request.POST.get('capacidad'))

            # Verificación de los datos recibidos
            if not activity_name or not description or not start_date or not start_time or not end_time or not capacity:
                messages.error(request, 'Todos los campos son obligatorios.')
                return redirect('crear_actividad')  # Redirige de vuelta al formulario

            # Obtener el deporte del usuario (entrenador actual)
            deporte_usuario = request.user.deporte
            entrenador = request.user  # El usuario actual será el entrenador

            # Convertir las fechas y horas
            try:
                start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
                start_time = timezone.datetime.strptime(start_time, '%H:%M').time()
                end_time = timezone.datetime.strptime(end_time, '%H:%M').time()
            except Exception as e:
                messages.error(request, f'Error al convertir las fechas y horas: {e}')
                return redirect('crear_actividad')

            # Calcular las fechas que caen en el día seleccionado dentro del rango
            fechas = []
            current_date = start_date
            while current_date <= end_date:
                if current_date.weekday() == day_of_week - 1:  # weekday() devuelve 0=lunes, 6=domingo
                    fechas.append(current_date)
                current_date += timedelta(days=1)

            # Crear las actividades para cada fecha calculada
            for fecha in fechas:
                actividad = Actividad(
                    nombre=activity_name,
                    descripcion=description,
                    entrenador=entrenador,
                    fecha=fecha,
                    fecha_fin=fecha,
                    hora_inicio=start_time,
                    hora_fin=end_time,
                    cupos=capacity
                )
                try:
                    actividad.save()
                except Exception as e:
                    messages.error(request, f'Error al guardar la actividad: {e}')
                    return redirect('crear_actividad')

            # Mensaje de éxito
            messages.success(request, 'Actividad creada con éxito')
            return redirect('actividad')  # Redirige después de crear la actividad

        except Exception as e:
            messages.error(request, f'Error al crear actividad: {str(e)}')
            return redirect('actividad')

    # Si no es un POST, solo renderizar el formulario
    return render(request, 'actividad.html')


# vista asistencia
@login_required
def asistencia(request):
    return render(request, 'asistencia.html')


# vista foro
@login_required
def foro(request):
    return render(request, 'foro.html')


# vista agendar
@login_required
def agendar(request):
    return render(request, 'agendar.html')


