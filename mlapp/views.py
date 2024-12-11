from django.shortcuts import render, redirect
from .forms import InputForm, LoginForm, SignUpForm
import joblib
import numpy as np
from .models import Customer
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate


loaded_model = joblib.load('model/ml_model.pkl')

@login_required
def index(request):
    return render(request, 'mlapp/index.html')

# def input_form(request):
#     form = InputForm()
#     return render(request, 'mlapp/input_form.html', {'form':form})
@login_required
def input_form(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('result')
    else:
        form = InputForm()
        return render(request, 'mlapp/input_form.html', {'form':form})
    
@login_required
def result(request):
    data = Customer.objects.order_by('id').reverse().values_list('limited_balance', 'education', 'marriage', 'age')
    x = np.array([data[0]])
    y = loaded_model.predict(x)
    y_proba = loaded_model.predict_proba(x)
    y_proba = y_proba*100
    y, y_proba = y[0], y_proba[0]

    customer = Customer.objects.order_by('id').reverse()[0]
    customer.proba = y_proba[y]
    customer.result = y
    customer.save()

    return render(request, 'mlapp/result.html', {'y':y, 'y_proba':round(y_proba[y], 2)})

@login_required
def history(request):
    if request.method == 'POST':
        d_id = request.POST
        d_customer = Customer.objects.filter(id=d_id['d_id'])
        d_customer.delete()

    customers = Customer.objects.all()
    return render(request, 'mlapp/history.html', {'customers':customers})

class Login(LoginView):
    form_class = LoginForm
    template_name = 'mlapp/login.html'

class Logout(LogoutView):
    template_name = 'mlapp/base.html'

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            new_user = authenticate(username=username, password=password)
            if new_user is not None:
                login(request, new_user)
                return redirect('index')
    else:
        form = SignUpForm()
        return render(request, 'mlapp/signup.html', {'form':form})
    