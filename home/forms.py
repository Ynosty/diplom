from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['category', 'car_name', 'desc', 'price', 'color', 'images', 'images2', 'images3', 'images4', 'images5']

class RatingForm(forms.Form):
    fuel_economy_rating = forms.ChoiceField(
        label='Економія палива:',
        choices=[(str(i), str(i)) for i in range(1, 11)]
    )
    repair_cost_rating = forms.ChoiceField(
        label='Вартість ремонту та обслуговування:',
        choices=[(str(i), str(i)) for i in range(1, 11)]
    )
    off_road_performance_rating = forms.ChoiceField(
        label='Проходимість авто:',
        choices=[(str(i), str(i)) for i in range(1, 11)]
    )