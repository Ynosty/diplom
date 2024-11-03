from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import pandas as pd
import numpy as np
from .models import *
from home.models import Car
from django.views.generic.edit import CreateView
model = None
df = pd.read_csv('Cleaned_Car_data.csv')

def seller(request):
    return render(request, 'seller/index.html')

def loginpage(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.error(request, 'User not found.')
                return redirect('/sell/login/')

            user_obj = authenticate(username=username, password=password)
            if user_obj:
                login(request, user_obj)
                return redirect('/sell/')
            else:
                messages.error(request, 'Wrong Password.')
                return redirect('/sell/login/')

        except Exception as e:
            messages.error(request, 'Something went wrong.')
            return redirect('/register/')
    
    return render(request, 'seller/login.html')

def registerpage(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')

            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, 'User already exists. Try to forget your password.')
                return redirect('/sell/register/')

            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, 'Account created. Please login.')

            return redirect('/sell/login/')

        except Exception as e:
            messages.error(request, 'Something went wrong.')
            return redirect('/sell/register/')

    return render(request, 'seller/register.html')


def sell(request):
    companies = sorted(df['company'].unique())
    car_models = sorted(df['name'].unique())
    companies.insert(0, 'Select Company')
    car_models.insert(0, 'Select Company')
    
    return render(request, 'seller/sell.html', {'companies': companies, 'car_models': car_models})


def result(request):
    if request.method == 'GET':
        try:
            name = request.GET['name']
            company = request.GET['company']
            year = request.GET['year']
            kms_driven = request.GET['kms_driven']
            fuel_type = request.GET['fuel_type']

            result = model.predict(pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                                                data=np.array([name, company, year, kms_driven, fuel_type]).reshape(1, 5)))
            result = int(result)
            print(result)

            return render(request, 'seller/result.html', {'result': result})
        except Exception as e:
            messages.error(request, 'Something went wrong.')
            return redirect('/sell/')

def car(request):
     if request.method == 'POST':
         category = request.POST.get('category')
         car_name = request.POST.get('car_name')
         desc = request.POST.get('desc')
         price = request.POST.get('price')
         color = request.POST.get('color')
         images = request.FILES.get('images')
         images2 = request.FILES.get('images2')
         images3 = request.FILES.get('images3')
         images4 = request.FILES.get('images4')
         images5 = request.FILES.get('images5')
         car = Car(category=category, car_name=car_name, desc=desc, price=price, color=color, images=images, images2=images2, images3=images3, images4=images4, images5=images5)
         car.save()
     return render(request, 'seller/car.html')

def sell2(request):
    if request.method == 'POST':
        carname = request.POST.get('carname')
        model = request.POST.get('model')
        original_price = request.POST.get('original_price')
        km_driven = request.POST.get('km_driven')
        year_of_purchase = request.POST.get('year_of_purchase')

        # Create a new Car instance and set the form data
        car = Car()
        car.car_name = carname
        # Set the other fields accordingly
        car.save()

        return redirect('sell')
    else:
        return render(request, 'seller/sell1.html')

def result2(request):
    return render(request, 'seller/result2.html')

class CarCreateView(CreateView):
    model = Car
    template_name = "seller/car.html"
    fields = "__all__"
