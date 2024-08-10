from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar/', views.registrar, name='registrar'),
    path('cerrar_sesion/', views.CerrarSesion, name='cerrar_sesion'),
    path('login/', views.iniciar_sesion, name='login'),
    path('tareas', views.tareas, name='tareas'),
    path('tareas/crear', views.agregar_tarea, name='add_tarea'),
    path('tareas/completar/<int:id_tarea>', views.completar_tarea, name='completar_tarea'),
    path('tareas/eliminar/<int:id_tarea>', views.eliminar_tarea, name='eliminar_tarea'),
    path('tareas/editar/<int:id_tarea>', views.editar_tarea, name='editar_tarea'),
]