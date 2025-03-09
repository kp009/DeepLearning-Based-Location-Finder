import os
from django.http import JsonResponse
from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Image
from .serializers import ImageSerializer
from rest_framework import status
import cv2
import numpy as np
from keras._tf_keras.keras.models import load_model


class ImageListView(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImagePredictor(APIView):
    
    file_path = os.path.abspath(os.path.join(os.getcwd(), "../location_identifier_model.keras"))

    model = load_model(file_path)  # Load your pre-trained model
    
    label_mapping = {  # Update this mapping with your actual label mapping
        "Denmark": 0, "Disney land": 1, "Eiffel-Tower": 2, "Iceland": 3, "Niagara Falls": 4
        # Add other location labels here
    }

    
   
    def get_coordinates(self, location_name):
        """Fetch latitude and longitude from OpenStreetMap Nominatim API."""
        try:
            url = f"https://nominatim.openstreetmap.org/search?q={location_name}&format=json"
            headers = {'User-Agent': 'images'}
            response = requests.get(url, headers=headers)
            data = response.json()

            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
            else:
                return None, None
        except Exception as e:
            print(f"Error fetching coordinates: {e}")
            return None, None
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES['image']
            img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
            img = cv2.resize(img, (224, 224)) / 255.0  # Resize & normalize
            img = np.expand_dims(img, axis=0)

            # Predict location
            prediction = self.model.predict(img)
            location_index = np.argmax(prediction)
            location = list(self.label_mapping.keys())[location_index]

            # Fetch latitude and longitude dynamically
            latitude, longitude = self.get_coordinates(location)

            # Save the image and its location data in the database
            image_instance = Image.objects.create(
                image=file,
                location=location,
                latitude=latitude,
                longitude=longitude
            )

            return Response({
                'location': location,
                'latitude': latitude,
                'longitude': longitude
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ImageUpdateView(APIView):
    def put(self, request, pk, *args, **kwargs):
        try:
            image_instance = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response({"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ImageSerializer(image_instance, data=request.data, partial=True)  # partial allows for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ImageDeleteView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            image_instance = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response({"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND)
        
        image_instance.delete()
        return Response({"message": "Image deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
from django.http import JsonResponse
import math

# Haversine formula to calculate the distance between two coordinates (latitude, longitude)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  # Distance in kilometers
    return distance

def calculate_distance(request, latitude, longitude):
    # Convert latitude and longitude to float values
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return JsonResponse({"error": "Invalid latitude or longitude."}, status=400)

    # Washington, D.C. coordinates
    base_latitude = 38.8954  # Washington, D.C. latitude
    base_longitude = -77.0369  # Washington, D.C. longitude

    # Calculate distance using Haversine formula
    distance = haversine(base_latitude, base_longitude, latitude, longitude)

    # Calculate cost (for example, $0.10 per kilometer)
    cost = distance * 0.1  # Assuming cost is $0.10 per kilometer

    return JsonResponse({"distance": distance, "cost": cost})
