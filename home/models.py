from urllib import request
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum
from django.urls import reverse
from django.core.validators import MaxValueValidator

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField( auto_now_add=True)

    class Meta:
        abstract=True

class CarCategory(BaseModel):
    category_name = models.CharField(max_length=100)
    def __str__(self):
        return self.category_name


class Car(BaseModel):
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE, related_name='cars')
    car_name = models.CharField(max_length=200)
    desc = models.CharField(max_length=500, null=True, blank=True)
    price = models.IntegerField()
    color = models.CharField(max_length=500, null=True, blank=True)
    images = models.ImageField(upload_to='car', blank=True)
    images2 = models.FileField(upload_to='car', null=True, blank=True)
    images3 = models.ImageField(upload_to='car', null=True, blank=True)
    images4 = models.ImageField(upload_to='car', null=True, blank=True)
    images5 = models.ImageField(upload_to='car', null=True, blank=True)
    
    fuel_economy_rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(10)])
    repair_cost_rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(10)])
    off_road_performance_rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(10)])
    phone_number = models.CharField(max_length=20)
    def calculate_overall_rating(self):
        total_ratings = [
            self.fuel_economy_rating,
            self.repair_cost_rating,
            self.off_road_performance_rating
        ]
        overall_rating = sum(total_ratings) / len(total_ratings)
        return overall_rating
    def __str__(self):
        return self.car_name
    def get_absolute_url(self):
        return reverse('sell')
    
    
class CarModel(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, primary_key=True)
    car_name = models.CharField(max_length=200)

    def __str__(self):
        return self.car_name
  
class CarRating(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_ratings')
    fuel_economy_rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(10)])
    repair_cost_rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(10)])
    off_road_performance_rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(10)])

    @property
    def overall_rating(self):
        total_ratings = [
            self.fuel_economy_rating,
            self.repair_cost_rating,
            self.off_road_performance_rating
        ]
        overall_rating = sum(total_ratings) / len(total_ratings)
        return overall_rating

    @property
    def car_name(self):
        return self.car.car_name    


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,  related_name = 'carts')
    is_paid = models.BooleanField(default=False)
    

    def sub_cart_total(self):
         return 
    
    
    @property
    def sub_cart_total(self):
        t= (CartItems.objects.filter(cart = self).aggregate(Sum('car__price'))['car__price__sum'])
        
        if t==0:
            return 0
        else:
            return t
        
    @property
    def tax_cart_total(self):
        t= (CartItems.objects.filter(cart = self).aggregate(Sum('car__price'))['car__price__sum'])*0.5
        if t==0:
            return 0
        else:
            return t
    
    @property
    def get_cart_total(self):
        t= (CartItems.objects.filter(cart = self).aggregate(Sum('car__price'))['car__price__sum']) + (CartItems.objects.filter(cart = self).aggregate(Sum('car__price'))['car__price__sum'])*0.5 + 10000
        
        if t==0:
            return 0
        else:
            return t
    
    
    
    

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name= 'cart_items')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)


class ShippingAddress(models.Model):
    username = models.CharField(max_length=500, null=True, blank= True)
    address = models.CharField(max_length=50, null=True, blank= True)
    city = models.CharField(max_length=50, null=True, blank= True)
    state = models.CharField(max_length=50, null=True, blank= True)
    zip = models.CharField(max_length=50, null=True, blank= True)
    date_added = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=50, null=True, blank= True)
    days = models.IntegerField(null=True, blank=True, default=1)
    def __str__(self):
        return self.address
    