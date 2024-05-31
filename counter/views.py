# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Food, FoodEntry
import requests
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from datetime import date, datetime

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('track_calories')
        else:
            error_message = 'Invalid login credentials'
            return render(request, 'events/login.html', {'error': error_message})
    return render(request, 'events/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('track_calories')
    else:
        form = UserCreationForm()
    return render(request, 'events/register.html', {'form': form})


@login_required
@csrf_exempt  # Ensure you use this decorator to exempt the view from CSRF verification, only if necessary
def add_food_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        food_item_name = data.get('food_item')
        meal_type = data.get('meal_type')

        if not meal_type:
            return JsonResponse({'status': 'failed', 'error': 'Meal type is required'}, status=400)

        # Find or create the food item in your database
        food_item, created = Food.objects.get_or_create(name=food_item_name, defaults={
            'calories': 0,  # Default values if not available
            'carbs': 0.0,
            'protein': 0.0
        })

        # Create a new FoodEntry for the current user
        FoodEntry.objects.create(
            user=request.user,
            food=food_item,
            meal_type=meal_type,
        )

        return JsonResponse({'status': 'success', 'food_item': food_item_name})
    
    return JsonResponse({'status': 'failed'}, status=400)

@login_required(login_url='login')
def delete_food(request, food_id):
    food_item = get_object_or_404(Food, pk=food_id)
    if request.method == 'POST':
        food_item.delete()
        return redirect('track_calories')
    return render(request, 'events/delete_food_confirm.html', {'food_item': food_item})

@login_required
def track_calories(request):
    api_data = None
    error_message = None

    if request.method == 'POST':
        query = request.POST.get('query')
        meal_type = request.POST.get('meal_type')

        if query:
            # Query the API to get nutritional information
            api_url = f'https://api.api-ninjas.com/v1/nutrition?query={query}'
            headers = {
                'X-Api-Key': '2bNS35WyvM2dlE+U2zFp/g==6UyQTyoR6PaimCqd'
            }
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                api_data = response.json()
                if api_data:
                    food_data = api_data[0]
                    calories = food_data.get('calories', 0.0)
                    carbs = food_data.get('carbohydrates_total_g', 0.0)
                    protein = food_data.get('protein_g', 0.0)

                    food = Food.objects.create(
                        name=food_data.get('name', 'Unknown Food'),
                        calories=calories,
                        carbs=carbs,
                        protein=protein
                    )

                    FoodEntry.objects.create(
                        user=request.user,
                        food=food,
                        meal_type=meal_type
                    )
                else:
                    error_message = "No data returned from the API."
            else:
                error_message = "Error...There was an error in the request!"

    # Get all food entries for the current user grouped by date
    entries_by_date = {}
    food_entries = FoodEntry.objects.filter(user=request.user).order_by('-date')
    for entry in food_entries:
        entry_date = entry.date.strftime('%B %d, %Y')
        if entry_date not in entries_by_date:
            entries_by_date[entry_date] = {
                'breakfast': [],
                'lunch': [],
                'dinner': [],
                'total_calories': 0
            }
        entries_by_date[entry_date][entry.meal_type].append(entry)
        entries_by_date[entry_date]['total_calories'] += entry.food.calories

    context = {
        'api': api_data,
        'error': error_message,
        'entries_by_date': entries_by_date
    }
    return render(request, 'events/track_calories.html', context)

def home(request):
    import requests
    import json

    if request.method == 'POST':
        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(api_url + query, headers={'X-Api-Key': '2bNS35WyvM2dlE+U2zFp/g==6UyQTyoR6PaimCqd'})
        try:
            api = json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            api = "Error...There was an error in the request!"
            print(e)
        return render(request, 'events/home.html', {'api': api})
    else:
        return render(request, 'events/home.html', {'query': 'Enter a valid food item to get the nutrition facts!'})
