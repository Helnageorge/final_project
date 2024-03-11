from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from .models import Registration
from .forms import EditProfileForm
from django.contrib.auth.hashers import check_password


def register(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        c_password = request.POST.get('cpassword')

        if password == c_password:
            if User.objects.filter(username=u_name).exists():
                messages.info(request, "Username already exists")
                return redirect('register_app:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect('register_app:register')
            else:
                user = User.objects.create_user(username=u_name, first_name=f_name, last_name=l_name, email=email, password=password)
                Registration.objects.create(username=user, fname=f_name, lname=l_name, email=email)
                messages.success(request, "Registration successful. Please log in.")
                return redirect('register_app:login')
        else:
            messages.error(request, "Password mismatch")
            return redirect('register_app:register')
    return render(request, 'register.html')

def view_profile(request, username):

    profile = Registration.objects.get(username__username=username)

    return render(request, 'profile.html', {'profile': profile})

def edit_profile(request):
    try:
        profile = request.user.registration
    except Registration.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('register_app:view_profile', username=request.user.username)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if password and not check_password(password, request.user.password):
                messages.error(request, "Incorrect password. Profile not updated.")
                return render(request, 'edit_profile.html', {'form': form})
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('register_app:view_profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})



def logout(request):
    auth.logout(request)
    return redirect("/")



def login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.info(request, 'successfully logged in')
            return redirect('/')

        else:
            messages.error(request,'Please enter a registered user id and password')
            return redirect('register_app:login')
    return render(request,'login.html')
