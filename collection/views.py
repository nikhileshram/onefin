from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
from collection.models import Collection, MovieCollection
from uuid import uuid4
from movie.models import Movie
from django.db.models import Q, Count
from django.db import transaction
import traceback

# Create your views here.

class CollectionDetailView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, collection_uuid=None):

        try:
            user_id = request.user.id
            movie_collections = MovieCollection.objects.filter(user_id=user_id)
            collection_ids = movie_collections.values_list('collection_id', flat=True)
            movie_ids = movie_collections.values_list('movie_id', flat=True)
            collections = Collection.objects.filter(id__in=collection_ids)
            data = {}
            data['is_success'] = True
            collection_data = []
            for collection in collections:
                collection_data.append({
                    'title': collection.title,
                    'description': collection.description,
                    'uuid': collection.id
                })
            data['collections'] = collection_data
            top_genres = Movie.objects.values('genre').annotate(movie_count=Count('id')).order_by('-movie_count')[:3]
            top_genre_list = [genres['genre'] for genres in top_genres]
            data['favourite_genres'] = ','.join(top_genre_list)
            return JsonResponse(data, status=200, safe=False)
        
        except Exception as e:
            print('Error getting the collections: ', e)
            traceback.print_exc()
            return JsonResponse({'error': 'Failed to get the collections'}, status=500)


    def get(self, request, collection_uuid):
        try:
            collection = Collection.objects.filter(id=collection_uuid).first()
            if collection is None:
                return JsonResponse({'error': 'Collection with the given ID does not exist'}, status=404)
            data = []
            movies = MovieCollection.objects.filter(collection=collection)
            movie_data = []
            for movie in movies:
                movie_data.append({
                    'title': movie.movie.title,
                    'description': movie.movie.description,
                    'genre': movie.movie.genre,
                    'uuid': movie.movie.id
                })
            data.append({
                'title': collection.title,
                'description': collection.description,
                'uuid': collection.id,
                'movies': movie_data
            })
            return JsonResponse(data, status=200, safe=False)
        
        except Exception as e:
            traceback.print_exc()
            print('Error getting the collection: ', e)
            return JsonResponse({'error': 'Failed to get the collection'}, status=500)
    

    def post(self, request):
        
        try:
            with transaction.atomic():
                data = request.data
                print('data: ', data)
                
                # check if name is present in the request data
                if 'title' not in data:
                    return JsonResponse({'error': 'Collection title is required'}, status=400)
                
                title = data['title']
                description = data.get('description', None)
                movies = data.get('movies', [])
                id = uuid4()
                collection = Collection.objects.create(id=id , title=title, description=description)
                print('collection: ', collection)

                for movie in movies:
                    title = movie.get('title', None)
                    description = movie.get('description', None)
                    genre = movie.get('genre', None)
                    uuid = movie.get('uuid', None)
                    movie, created = Movie.objects.get_or_create(id=uuid, defaults={'title': title, 'description': description, 'genre': genre, 'id': uuid})
                    MovieCollection.objects.create(id=id, collection=collection, movie=movie, user=request.user)

                return JsonResponse({'collection_uuid': collection.id}, status=201)
        
        except Exception as e:
            print('Error creating the collection: ', e)
            traceback.print_exc()
            return JsonResponse({'error': 'Failed to create the collection'}, status=500)
    
    
    def put(self, request, collection_uuid):
        
        try:
            with transaction.atomic():
                data = request.data
                print('data: ', data)

                if collection_uuid is None:
                    return JsonResponse({'error': 'Collection ID is required'}, status=400)
                
                collection = Collection.objects.filter(id=collection_uuid).first()
                if collection is None:
                    return JsonResponse({'error': 'Collection with the given ID does not exist'}, status=404)
                
                if 'title' in data:
                    collection.title = data['title']
                if 'description' in data:
                    collection.description = data['description']
                
                collection.save()
                
                movies = data.get('movies', [])

                if len(movies) > 0:
                    movieCollections = MovieCollection.objects.filter(collection=collection)
                    Movie.objects.filter(~Q(id__in=MovieCollection.objects.values_list('movie_id', flat=True))).delete()
                

                for movie in movies:
                    title = movie.get('title', None)
                    description = movie.get('description', None)
                    genre = movie.get('genre', None)
                    uuid = movie.get('uuid', None)
                    movie, created = Movie.objects.get_or_create(id=uuid, defaults={'title': title, 'description': description, 'genre': genre, 'id': uuid})
                    id = uuid4()
                    MovieCollection.objects.create(id=id, collection=collection, movie=movie, user=request.user)

                return JsonResponse({'collection_uuid': collection.id}, status=201)
        
        except Exception as e:
            traceback.print_exc()
            print('Error creating the collection: ', e)
            return JsonResponse({'error': 'Failed to create the collection'}, status=500)

    def delete(self, request, collection_uuid):
        
        try:
            print('collection_uuid: ', collection_uuid)
            if collection_uuid is None:
                return JsonResponse({'error': 'Collection ID is required'}, status=400)
            else:
                if Collection.objects.filter(id=collection_uuid).count() == 0:
                    return JsonResponse({'error': 'Collection with the given ID does not exist'}, status=404)
                print('deleting the collection with id: ', collection_uuid)
                Collection.objects.filter(id=collection_uuid).delete()
                return JsonResponse({'message': 'Collection deleted successfully'}, status=200)
        
        except Exception as e:
            traceback.print_exc()
            print('Error deleting the collection: ', e)
            return JsonResponse({'error': 'Failed to delete the collection'}, status=500)
        

class CollectionListView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, collection_uuid=None):

        try:
            user_id = request.user.id
            movie_collections = MovieCollection.objects.filter(user_id=user_id)
            collection_ids = movie_collections.values_list('collection_id', flat=True)
            movie_ids = movie_collections.values_list('movie_id', flat=True)
            collections = Collection.objects.filter(id__in=collection_ids)
            data = {}
            data['is_success'] = True
            collection_data = []
            for collection in collections:
                collection_data.append({
                    'title': collection.title,
                    'description': collection.description,
                    'uuid': collection.id
                })
            data['collections'] = collection_data
            top_genres = Movie.objects.values('genre').annotate(movie_count=Count('id')).order_by('-movie_count')[:3]
            top_genre_list = [genres['genre'] for genres in top_genres]
            data['favourite_genres'] = ','.join(top_genre_list)
            return JsonResponse(data, status=200, safe=False)
        
        except Exception as e:
            print('Error getting the collections: ', e)
            traceback.print_exc()
            return JsonResponse({'error': 'Failed to get the collections'}, status=500)