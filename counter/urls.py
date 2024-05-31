
from django.urls import path
from .views import login_view, logout_view, register_view, track_calories, home, delete_food, add_food_item

urlpatterns = [
    path('', home, name='home'),
    path('track-calories/', track_calories, name='track_calories'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('delete-food/<int:food_id>/', delete_food, name='delete_food'),
    path('add_food_item/', add_food_item, name='add_food_item'),
]