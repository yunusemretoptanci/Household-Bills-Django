from multiprocessing import context
from webbrowser import get
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from .models import Member, Inovoice
from django.db.models import Sum
from django.shortcuts import get_object_or_404

@login_required(login_url='/login')
def home(request):
    members=request.user.member_set.all()
    inovoices=request.user.inovoice_set.all().order_by('-created')
    total_inovoice_price=inovoices.aggregate(total_price=Sum('price'))['total_price']
    
    if request.method=='POST':
        if 'member' in request.POST:
            family_name=request.user
            inputname=request.POST.get('add_member_name')
            member=Member(family_name=family_name,name=inputname)
            if Member.objects.filter(family_name=family_name,name=inputname):
                messages.error(request, 'Please enter a valid name',extra_tags='add_member')
            else:   
                member.save()
                return redirect('home')
        elif 'inovoice' in request.POST:
            owner_name=request.POST.get('owner')
            owner_family_name=request.user
            owner_name=Member.objects.get(name=owner_name,family_name=owner_family_name)
            
            Inovoice.objects.create(
                family=request.user,
                owner=owner_name,
                description=request.POST.get('description'),
                price=request.POST.get('price')
            )
            return redirect('home')
            

    return render(request, 'base/home.html', {'members':members,'inovoices':inovoices,'total_inovoice_price':total_inovoice_price})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginRegisterPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        if 'login' in request.POST: 
            username=request.POST.get('username')
            password=request.POST.get('password')

            try:
                User.objects.get(username=username)
            except:
                messages.error(request, 'User does not exist',extra_tags='login')
            
            user= authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                
                return redirect('home')
            else:
                messages.error(request, 'Username or password is incorrect',extra_tags='login')
        elif 'register' in request.POST:
            username=request.POST.get('username')
            password=request.POST.get('password')
            password2=request.POST.get('password2')

            if password==password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists',extra_tags='register')
                else:
                    user=User.objects.create_user(username=username,password=password)
                    user.save()
                    messages.success(request, 'User created',extra_tags='register')
            else:
                messages.error(request, 'Passwords do not match',extra_tags='register')

    return render(request, 'base/login_register.html')

@login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login')
def deleteInovoice(request,pk):
    inovoice=Inovoice.objects.get(id=pk)
    inovoice.delete()
    return redirect('home')


    


    