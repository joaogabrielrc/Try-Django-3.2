from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout


def register_view(request):
  form = UserCreationForm(request.POST or None)
  if form.is_valid():
    user_object = form.save()
    return redirect('/login')

  context = {
    'form': form
  }

  return render(request, 'accounts/register.html', context)


def login_view(request):
  data = request.POST or None
  form = AuthenticationForm(request, data=data)
  context = {
    'form': form
  }
  
  if request.method == 'POST': 
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('/')    

  return render(request, 'accounts/login.html', context)
  

def login_view_old(request):
  context = {}
  
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('/')
    else:
      context = {'error': 'Invalid credencials'}    

  return render(request, 'accounts/login.html', context)


def logout_view(request):
  if request.method == 'POST':
    logout(request)
    return redirect('/login/')

  return render(request, 'accounts/logout.html')  
