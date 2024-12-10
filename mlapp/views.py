from django.shortcuts import render, redirect
from .forms import InputForm
import joblib
import numpy as np
from .models import Customer


loaded_model = joblib.load('model/ml_model.pkl')

def index(request):
    return render(request, 'mlapp/index.html')

# def input_form(request):
#     form = InputForm()
#     return render(request, 'mlapp/input_form.html', {'form':form})
def input_form(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('result')
    else:
        form = InputForm()
        return render(request, 'mlapp/input_form.html', {'form':form})
    
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
