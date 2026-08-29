from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm
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

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect(reverse('home'))


def register_view(request):
    form = UserRegisterForm(request.POST or None,)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('user:login')
        else:
            messages.error(
                request,
                'Erro ao cadastrar o usuário. Verifique os campos informados.'
            )

    return render(
        request,
        'pages/form.html',
        {'form': form}
    )