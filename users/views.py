from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

    
        user = authenticate(username=email, password=password)

        if user is not None:
        
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful!",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    
class UserDetailView(APIView):
    """
    Fetch the details of the currently authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Get the authenticated user from the token
        serializer = UserSerializer(user)
        return Response(serializer.data)