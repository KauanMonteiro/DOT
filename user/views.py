from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.get_full_name() or user.username}!')
            return redirect('home')

        messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'pages/login.html')
