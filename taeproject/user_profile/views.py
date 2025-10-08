from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Имэйл эсвэл нууц үг буруу байна.')
    return render(request, 'user_profile/login.html')



from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        if password1 != password2:
            messages.error(request, 'Нууц үг таарахгүй байна.')
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Нэвтрэх нэр аль хэдийн бүртгэлтэй байна.')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Имэйл аль хэдийн бүртгэлтэй байна.')
        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password1,
                phone=phone,
                address=address
            )
            auth_login(request, user)
            return redirect('dashboard')
    return render(request, 'user_profile/register.html')


from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'user_profile/dashboard.html')


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')