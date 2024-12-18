from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class UserView(APIView):
    
    def post(self, request):
        # Extract the data
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({"error": "Username, password, and email are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Check if the user already exists
        user = User.objects.filter(username=username).first()

        if user:
            # If the user exists, generate new tokens for the existing user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'access': access_token,
                'refresh': refresh_token,
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_200_OK)

        # Step 2: If the user does not exist, create the user
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
        except Exception as e:
            return Response({"error": f"Error creating user: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Step 3: Generate JWT tokens for the newly created user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Return tokens and user info
        return Response({
            'access': access_token,
            'refresh': refresh_token,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)