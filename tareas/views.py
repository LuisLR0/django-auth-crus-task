from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Tareas
from .forms import TareasForm


# Create your views here.

def home(request):
    return render(request, 'home.html')

def registrar(request):
    
    form = UserCreationForm()
    if request.method == 'POST':
        datos = request.POST
        if datos['password1'] == datos['password2']:
            
            try:
                user = User.objects.create_user(
                        username=datos['username'],
                        password=datos['password1']
                    )
                
                user.save()
                login(request, user)
                return redirect('home')
            except:
                return render(request, 'registrar.html', {
                    'form': form,
                    'aviso': 'Usuario ya existe!'
                })
            
        else:
            return render(request, 'registrar.html', {
                'form': form,
                'aviso': 'Las contraseñas no coinciden'
            })
    else:
        return render(request, 'registrar.html', {
            'form': form,
        })

def iniciar_sesion(request):
    
    
    
    if request.method == 'POST':
        
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                
                login(request, user)
                return redirect('home')
            
            else:
                return render(request, 'login.html', {
                    'form': form,
                    'aviso': 'Nombre de usuario o contraseña incorrectos.'
                })
                
        else:
            
            return render(request, 'login.html', {
                'form': form,
                'aviso': 'Nombre de usuario o contraseña incorrectos.'
            })
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form})

@login_required
def CerrarSesion(request):
    logout(request)
    return redirect('home')

@login_required
def agregar_tarea(request):
    if request.method == 'POST':
        
        form = TareasForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario = request.user
            tarea.save()
            
            return redirect('tareas')

    return render(request, 'add_tarea.html', {
        'form': TareasForm()
    })

@login_required
def tareas(request):
    
    tareas = Tareas.objects.filter(usuario=request.user)
    
    return render(request, 'tareas.html', {
        'tareas': tareas
    })

@login_required
def completar_tarea(request, id_tarea):
    
    tarea = get_object_or_404(Tareas, id=id_tarea, usuario=request.user)
    tarea.completado = not tarea.completado 
    tarea.finalizacion = timezone.now()
    tarea.save()
    
    return redirect('tareas')

@login_required
def eliminar_tarea(request, id_tarea):
    
    tarea = get_object_or_404(Tareas, id=id_tarea, usuario=request.user)
    tarea.delete()
    
    return redirect('tareas')

@login_required
def editar_tarea(request, id_tarea):

    tarea = get_object_or_404(Tareas, id=id_tarea, usuario=request.user, completado=False)
    
    if request.method == 'POST':
        
        try:
            tarea.titulo = request.POST.get('titulo')
            tarea.descripcion = request.POST.get('descripcion')
            tarea.important = request.POST.get('important') == 'on'
                
            tarea.save()
            
            return redirect('tareas')
        except ValueError as error:
            print(error)
            return render(request, 'edit_tarea.html', {
                'form': TareasForm(instance=tarea),
                'aviso': 'Ingresa bien los datos!'
             })
        
    return render(request, 'edit_tarea.html', {
        'form': TareasForm(instance=tarea)
    })