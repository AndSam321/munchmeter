from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField(default=0.0)
    carbs = models.FloatField(default=0.0)
    protein = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class FoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    meal_type = models.CharField(max_length=10, choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner')])

    def __str__(self):
        return f"{self.user} - {self.food} - {self.meal_type} - {self.date}"
