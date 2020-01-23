from django.shortcuts import render
from myapp.forms import *
from django.core.mail import send_mail


from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
# Create your views here.
def index(request):
    if request.session.get('username'):
        user=request.session.get('username')
        return render(request,"home.html",context={"username":user})
    return render(request,"home.html")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def l(request):
    return HttpResponse("<h1>hai</h1>")

def register(request):
    registered=False
    if request.method=="POST" and request.FILES:
        userform=UserForm(request.POST)
        profileform=ProfileForm(request.POST,request.FILES)
        if userform.is_valid() and profileform.is_valid():
            user=userform.save(commit=False)
            user.set_password(userform.cleaned_data['password'])
            user.save()

            profile=profileform.save(commit=False)
            profile.user=user
            profile.save()
            send_mail(
                    'Registration Successful',
                    'Thanks For Registering Your Registration is Successful',
                    'akshay.python@gmail.com',
                    [user.email],
                    fail_silently=False,
                    )
            registered=True
    userform=UserForm()
    profileform=ProfileForm()
    d={'registered':registered,'userform':userform,'profileform':profileform}
    return render(request,'register.html',context=d)

def user_login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse("Not a Active User or Invalid username and password")
    return render(request,'user_login.html',context={})

@login_required
def user_profile(request):
    username=request.session['username']
    user=User.objects.get(username=username)
    print(user.password)
    profile=Profile.objects.get(user=user)
    data={'profile':profile}
    return render(request,'profile.html',context=data)

@login_required
def change_password(request):
    username=request.session["username"]
    user=User.objects.get(username=username)
    if request.method=="POST":
        password=request.POST["password"]
        user.set_password(password)
        user.save()
        HttpResponseRedirect(reverse('user_logout'))
    return render(request,'changepwd.html')

def reset_password(request):
    if request.method=="POST":
        username=request.POST['username']
        user=User.objects.get(username=username)
        if user:
            user.set_password("password")
            
            send_mail(
                    'New Password',
                    'Your Password reset successul your new password is \"password\"',
                    'akshay.python@gmail.com',
                    [user.email],
                    fail_silently=False,
                    )
            user.save()
        else:
            return HttpResponse("Invalid User")
    return render(request,'reset_pwd.html')        