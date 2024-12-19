from django.http import JsonResponse
from collection.models import Collection, MovieCollection
from uuid import uuid4
from movie.models import Movie
from django.db.models import Q, Count
from django.db import transaction


def get_collection_using_uuid(request, collection_uuid):

    collection = Collection.objects.filter(id=collection_uuid, user=request.user).first()
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
    return data

def update_collection_using_uuid(request, collection_uuid):
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
            MovieCollection.objects.create(id=id, collection=collection, movie=movie)
        return collection
    
def delete_collection_using_uuid(request, collection_uuid):
    print('collection_uuid: ', collection_uuid)
    
    if collection_uuid is None:
        raise Exception('Collection ID is required')
    
    if Collection.objects.filter(id=collection_uuid, user=request.user).count() == 0:
        raise Exception('Collection with the given ID does not exist')
    print('deleting the collection with id: ', collection_uuid)
    Collection.objects.filter(id=collection_uuid, user=request.user).delete()
    return

def get_all_collection_and_favourite_genre(request):

    user_id = request.user.id
    collections = Collection.objects.filter(user_id=user_id)
    movie_collections = MovieCollection.objects.filter(collection_id__in=collections.values_list('id', flat=True))
    movie_ids = movie_collections.values_list('movie_id', flat=True)
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
    top_genres = Movie.objects.filter(id__in=movie_ids).values('genre').annotate(movie_count=Count('id')).order_by('-movie_count')[:3]
    top_genre_list = [genres['genre'] for genres in top_genres]
    data['favourite_genres'] = ','.join(top_genre_list)
    return data

def create_new_collection(request):

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
        collection = Collection.objects.create(id=id , title=title, description=description, user=request.user)
        print('collection: ', collection)

        for movie in movies:
            title = movie.get('title', None)
            description = movie.get('description', None)
            genre = movie.get('genre', None)
            uuid = movie.get('uuid', None)
            movie, created = Movie.objects.get_or_create(id=uuid, defaults={'title': title, 'description': description, 'genre': genre, 'id': uuid})
            MovieCollection.objects.create(id=id, collection=collection, movie=movie)
        return collection