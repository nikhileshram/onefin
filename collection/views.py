from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
import traceback
from .service import get_collection_using_uuid, update_collection_using_uuid, delete_collection_using_uuid,\
    get_all_collection_and_favourite_genre, create_new_collection

# Create your views here.

class CollectionDetailView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, collection_uuid):
        try:
            data = get_collection_using_uuid(request, collection_uuid)
            return JsonResponse(data, status=200, safe=False)
        
        except Exception as e:
            traceback.print_exc()
            print('Error getting the collection: ', e)
            return JsonResponse({'error': 'Failed to get the collection'}, status=500)
    
    
    
    def put(self, request, collection_uuid):
        
        try:
            collection = update_collection_using_uuid(request, collection_uuid)
            return JsonResponse({'collection_uuid': collection.id}, status=200)
        
        except Exception as e:
            traceback.print_exc()
            print('Error creating the collection: ', e)
            return JsonResponse({'error': 'Failed to create the collection'}, status=500)

    def delete(self, request, collection_uuid):
        
        try:
            delete_collection_using_uuid(request, collection_uuid)
            return JsonResponse({'message': 'Collection deleted successfully'}, status=200)
        
        # here we can create multiple exception types and handle them separately for better error propagation
        except Exception as e:
            traceback.print_exc()
            print('Error deleting the collection: ', e)
            return JsonResponse({'error': 'Failed to delete the collection'}, status=500)
        

class CollectionListView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, collection_uuid=None):

        try:
            data = get_all_collection_and_favourite_genre(request)
            return JsonResponse(data, status=200, safe=False)
        
        except Exception as e:
            print('Error getting the collections: ', e)
            traceback.print_exc()
            return JsonResponse({'error': 'Failed to get the collections'}, status=500)

    
    def post(self, request):
        
        try:
            collection = create_new_collection(request)
            return JsonResponse({'collection_uuid': collection.id}, status=201)
        
        except Exception as e:
            print('Error creating the collection: ', e)
            traceback.print_exc()
            return JsonResponse({'error': 'Failed to create the collection'}, status=500)