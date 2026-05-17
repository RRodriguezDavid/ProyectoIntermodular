from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile


def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:catalog')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Los administradores van directamente al panel de admin
            if user.is_staff:
                return redirect('admin:index')
            return redirect('store:catalog')
        else:
            messages.error(request, 'Usuario o contrasena incorrectos.')

    return render(request, 'users/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('store:catalog')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Las contrasenas no coinciden.')
            return render(request, 'users/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya existe.')
            return render(request, 'users/register.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        # El perfil se crea automáticamente vía la señal post_save en users/signals.py
        login(request, user)
        messages.success(request, f'Bienvenido, {username}.')
        return redirect('store:catalog')

    return render(request, 'users/register.html')


def logout_view(request):
    logout(request)
    return redirect('users:login')


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.telefono = request.POST.get('telefono', '')
        profile.direccion = request.POST.get('direccion', '')
        profile.ciudad = request.POST.get('ciudad', '')
        profile.codigo_postal = request.POST.get('codigo_postal', '')
        profile.save()
        messages.success(request, 'Perfil actualizado correctamente.')

    return render(request, 'users/profile.html', {'profile': profile})
