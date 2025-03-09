from django.urls import path
from .views import  ImageListView , ImagePredictor, ImageUpdateView, ImageDeleteView
from . import views

urlpatterns = [
    path('images/', ImageListView.as_view(), name='image_list'),
    path('predict/', ImagePredictor.as_view(), name='image-predict'),
    path('images/update/<int:pk>/', ImageUpdateView.as_view(), name='image-update'),
    path('images/delete/<int:pk>/', ImageDeleteView.as_view(), name='image-delete'),
    path('distance/<str:latitude>/<str:longitude>/', views.calculate_distance, name='calculate_distance'),

]
