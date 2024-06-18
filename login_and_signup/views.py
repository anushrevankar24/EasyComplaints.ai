from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render ,redirect
from login_and_signup.models import CustomUser
from Dashboard.views import *

def home_page(request):
    return render(request, 'home.html')

def logout_page(request):
      logout(request);
      return render(request, 'home.html')
  
def citizen_registration(request):
    if request.method == 'POST':
        role='citizen'
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email') 
        phone_number=request.POST.get('phone_number')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request,"Confirm password is not same as password")
            return redirect('citizen_registration')
        existing_user = CustomUser.objects.filter(email=email).exists()
        if existing_user:
            messages.error(request, "A user with this email already exists !!!")
            return redirect('citizen_registration')
        
        user = CustomUser.objects.create_user(
             first_name=first_name,
               last_name=last_name,
              username=email,
               email=email,
               password=password,
               phone_number=phone_number,
                role=role
            )
        # user.set_password(password)
        user.save()
        messages.success(request,"Your Account has been Successfully created !!!")
        return redirect('user_login')
    return render(request, 'citizen_registration.html')

def user_login(request):
    if request.method =='POST':
        email=request.POST.get('email')  
        password=request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
               login(request, user);
               return redirect('dashboard')
        else :
             messages.error(request,"Credentials did not match")
             return redirect('user_login')
    return render(request, 'login.html')