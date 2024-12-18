from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.conf import settings
import requests
from django.http import JsonResponse

# Create your views here.

class MovieView(views.APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        try:
            MOVIE_API_URL = 'https://demo.credy.in/api/v1/maya/movies/'
            MOVIE_API_USERNAME = settings.CLIENT_ID
            MOVIE_API_PASSWORD = settings.CLIENT_SECRET

            print(MOVIE_API_PASSWORD)

            print('calling the api for movies')
            response = requests.get(MOVIE_API_URL, auth=(MOVIE_API_USERNAME, MOVIE_API_PASSWORD))
            print('response from the api for movies: ', response)
            
            if response.status_code == 200:
            # If successful, return the data as JSON
                return JsonResponse(response.json(), safe=False)
            else:
                # Handle the case where the request fails
                print('Did not receive a 200 response from the external API')
                return JsonResponse({'error': 'Failed to fetch movies from the external API'}, status=500)
        
        except Exception as e:
            print('Error fetching movies from the external API: ', e)
            return JsonResponse({'error': 'Failed to fetch movies from the external API'}, status=500)