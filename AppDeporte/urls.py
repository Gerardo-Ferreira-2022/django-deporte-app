from django.urls import path
from .views import home, dashboard, actividad, usuarios, actualizar_usuario, eliminar_usuario, crear_actividad, foro, asistencia, agendar
from .views import RegisterView
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('actividad/', actividad, name='actividad'),
    path('crear_actividad/', crear_actividad, name='crear_actividad'),  # Nueva URL para crear actividad
    path('usuarios/', usuarios, name='usuarios'),
    path('usuarios/actualizar/', actualizar_usuario, name='actualizar_usuario'),
    path('eliminar_usuario/<user_id>/', eliminar_usuario, name='eliminar_usuario'),
    path('asistencia/', asistencia, name='asistencia'),
    path('foro/', foro, name='foro'),
    path('agendar/', agendar, name='agendar'),
    

]