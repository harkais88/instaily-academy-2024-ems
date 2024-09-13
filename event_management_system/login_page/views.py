from django.shortcuts import render,redirect
from django.http import Http404
from .models import User

def home(request):
    param = {}
    if "user" in request.session:
        param = {'current_user': request.session['user']}

    return render(request,'home.html',param)
    
def login(request):
    # If user is logged in already
    if 'user' in request.session:
        return redirect('home')
    
    # If no signup has been done till now (only for testing purpose)
    if not User.objects.exists():
        return redirect('signup')

    error = {}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Check If username and password exist in database   
        try:
            User.objects.get(username=username,password=password)
            request.session['user'] = username
            return redirect('home')
        except User.DoesNotExist:
            error = {'error': 'error'}
                
    return render(request,'login.html',error)

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).count() > 0:
            raise Http404("Username already exists, go back to home page!")
        else:
            User(username=username,password=password).save()
            return redirect('login')

    return render(request,'signup.html')

def logout(request):
    try:
        del request.session['user']
    except:
        pass
    return redirect('home')