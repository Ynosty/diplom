from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login , logout, authenticate
from django.http import JsonResponse
import json
from django.db.models import Q
import datetime
from .forms import CarForm, RatingForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Car, Cart, CartItems, CarRating

from django.contrib.auth.decorators import login_required


def home(request):
    car = Car.objects.all()
    paginator = Paginator(car, 3)
    

    page_number = request.GET.get('page')
    car = paginator.get_page(page_number)
    context  = {'car':car}

    return render(request, 'home/index.html', context)

def buyer(request):
    car = Car.objects.all()
    paginator = Paginator(car, 3)
    

    page_number = request.GET.get('page')
    car = paginator.get_page(page_number)
    context  = {'car':car}

    return render(request, 'home/buyer.html', context)

def login_page(request):
    if request.method=='POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')

            user_obj = User.objects.filter(username = username)
            if not user_obj.exists():
                messages.error(request, 'User not found.')
                return redirect('/buyer/login/')

            
            
            if user_obj  := authenticate(username = username, password=password):
                login(request, user_obj)
                return redirect('/buyer')

            messages.error(request, 'Wrong Password.')

            return redirect('/login/')

        except Exception as e:
            messages.error(request, 'something went wrong')

            return redirect('/register/')
    return render(request, 'home/login.html')

def register_page(request):
    if request.method =='POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')

            user_obj = User.objects.filter(username = username)
            if user_obj.exists():
                messages.error(request, 'User already exist try to forget Password.')
                return redirect('/buyer/register/')

            user_obj = User.objects.create(username = username)
            user_obj.set_password(password)
            user_obj.save()

            messages.error(request, 'Account Created Login Plz.')

            return redirect('/buyer/login/')

        except Exception as e:
            messages.error(request, 'something went wrong')

            return redirect('/buyer/register/')

    return render(request, 'home/register.html')

def add_cart(request, car_uid):
    user = request.user

    car_obj = Car.objects.get(uid=car_uid)
    cart, _ = Cart.objects.get_or_create(user= user, is_paid=False)

    cart_items = CartItems.objects.create(
                cart = cart,
                car = car_obj
    )
    return redirect('/buyer/')


def save_rating(request, detail_page_uid):
    car = Car.objects.get(uid=detail_page_uid) # Получение объекта автомобиля

    if request.method == 'POST':
        form = RatingForm(request.POST) # Инициализация формы рейтинга с данными из запроса
        if form.is_valid():
            fuel_economy_rating = form.cleaned_data['fuel_economy_rating'] # Получение данных рейтинга
            repair_cost_rating = form.cleaned_data['repair_cost_rating']
            off_road_performance_rating = form.cleaned_data['off_road_performance_rating']
            
            # Получение всех рейтингов автомобиля
            ratings = car.car_ratings.all()
            
            # Вычисление среднего значения рейтингов
            total_ratings = ratings.count() + 1
            fuel_economy_sum = sum([rating.fuel_economy_rating for rating in ratings]) + int(fuel_economy_rating)
            repair_cost_sum = sum([rating.repair_cost_rating for rating in ratings]) + int(repair_cost_rating)
            off_road_performance_sum = sum([rating.off_road_performance_rating for rating in ratings]) + int(off_road_performance_rating)
            
            # Вычисление нового общего рейтинга автомобиля
            fuel_economy_avg = fuel_economy_sum / total_ratings
            repair_cost_avg = repair_cost_sum / total_ratings
            off_road_performance_avg = off_road_performance_sum / total_ratings
            
            # Создание и сохранение объекта CarRating
            car_rating = CarRating.objects.create(
                car=car,
                fuel_economy_rating=fuel_economy_rating,
                repair_cost_rating=repair_cost_rating,
                off_road_performance_rating=off_road_performance_rating
            )
            
            # Обновление общих рейтингов автомобиля
            car.fuel_economy_rating = fuel_economy_avg
            car.repair_cost_rating = repair_cost_avg
            car.off_road_performance_rating = off_road_performance_avg
            car.save()

            return redirect('detail', detail_page_uid=detail_page_uid) # Перенаправление на страницу деталей после сохранения рейтинга
    else:
        form = RatingForm() # Создание пустой формы рейтинга

    context = {
        'form': form,
        'car': car,
    }

    return render(request, 'home/detail.html', context)
@login_required
def cart(request):
    carts = Cart.objects.filter(is_paid=False, user=request.user)
    context = {'carts': carts}
    return render(request, 'home/cart.html', context)

def remove_cart_items(request, cart_item_uid):
    try:
        CartItems.objects.get(uid=cart_item_uid).delete()
        return redirect('/cart/')
    except Exception as e:
        print(e)

def detail_page(request, detail_page_uid):
    car = get_object_or_404(Car, uid=detail_page_uid)
    cars = Car.objects.all()
    user = request.user

    ratings = car.car_ratings.all()
    first_rating = car.car_ratings.first()
    overall_rating = first_rating.overall_rating if first_rating else 0

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            fuel_economy_rating = form.cleaned_data['fuel_economy_rating']
            repair_cost_rating = form.cleaned_data['repair_cost_rating']
            off_road_performance_rating = form.cleaned_data['off_road_performance_rating']

            car_rating = CarRating.objects.create(
                car=car,
                fuel_economy_rating=fuel_economy_rating,
                repair_cost_rating=repair_cost_rating,
                off_road_performance_rating=off_road_performance_rating
            )
            overall_rating = car_rating.overall_rating

            # Обновите оценку рейтинга автомобиля
            car.fuel_economy_rating = overall_rating
            car.save()

            # Перенаправьте пользователя на страницу с подробностями автомобиля
            return redirect('detail_page', detail_page_uid=detail_page_uid)
    else:
        form = RatingForm()
    
    context = {
        'detail_page_uid': detail_page_uid,
        'car': car,
        'cars': cars,
        'overall_rating': overall_rating,
        'car_uid': detail_page_uid,
        'form': form,
        'phone_number': car.phone_number
    }
    return render(request, 'home/detail.html', context)
def ride(request):
    car = Car.objects.all()
    paginator = Paginator(car, 9)
    category = request.GET.get('category')
    fuel_economy_rating = request.GET.get('fuel_economy_rating')
    repair_cost_rating = request.GET.get('repair_cost_rating')
    off_road_performance_rating = request.GET.get('off_road_performance_rating')
    car_name_query = request.GET.get('car_name')

    cars = Car.objects.all()

    if category:
        cars = cars.filter(category__name=category)

    if fuel_economy_rating:
        cars = cars.filter(car_ratings__fuel_economy_rating=int(fuel_economy_rating))

    if repair_cost_rating:
        cars = cars.filter(car_ratings__repair_cost_rating=int(repair_cost_rating))

    if off_road_performance_rating:
        cars = cars.filter(car_ratings__off_road_performance_rating=int(off_road_performance_rating))

    if car_name_query:
        cars = cars.filter(Q(car_name__icontains=car_name_query) | Q(carmodel__car_name__icontains=car_name_query))

    paginator = Paginator(cars, 9)
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)

    context = {
        'car': car,
        'cars': cars,
        'category': category,
        'fuel_economy_rating': fuel_economy_rating,
        'repair_cost_rating': repair_cost_rating,
        'off_road_performance_rating': off_road_performance_rating,
        'car_name_query': car_name_query
    }
    return render(request, 'home/ride.html', context)


def checkout(request):
    checkout = Cart.objects.filter(is_paid=True, user= request.user)
    context = {'orders':checkout}
    return render(request, 'home/checkout.html', context)


def checkout(request):
    checkout = Cart.objects.get(is_paid=False, user= request.user)
   
    context = {'cars':checkout}
    return render(request, 'home/checkout.html', context)


    
    # data = json.loads(request.body)

    # if request.user.is_authenticated:
    #     user = request.user
    #     order, created = Cart.objects.get_or_create(user=user)
    #     total = data['form']['total']
        

    #     if total == cart.get_cart_total:
    #         order.complete = True 
    #     order.save()

    #     if order.shipping==True:
    #         ShippingAddress.objects.create(full_name=full_name, order=order, address=data['shipping']['address'], city=data['shipping']['city'] , state=data['shipping']['state'], zipcode = data['shipping']['zipcode'],)
    
    # else:
    #     print('User is not logged in..')
    #F return JsonResponse('Payment complete!', safe=False)
def processOrder(request):
    car = Car.objects.all()
    carts = Cart.objects.get(is_paid=False, user= request.user)
    
    context = {
        'car':car,
        'carts' :carts
    }
    if request.method=='POST':
        address = request.POST.get('address')
        email = request.POST.get('email')
        username = request.POST.get('username')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        days = request.POST.get('days')
        
        ShippingAddress.objects.create(username=username, address= address, email=email,city= city, state=state, zip=zip,days=days,)
    return render(request, 'home/checkout.html', context)

def selling_form(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace 'home' with the appropriate URL name for the home page
    else:
        form = CarForm()
    
    context = {'form': form}
    return render(request, 'seller/selling_form.html', context)

def sell_car(request):
    cars = Car.objects.all()
    context = {'cars': cars}
    return render(request, 'seller/sell_car.html', context)