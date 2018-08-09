from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from django.db.models import Q
from Accounts.serializer import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserSearchSerializer,
    UserUpdateSerializer
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView


# Create your views here.


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserLogInAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        seralizer = UserLoginSerializer(data=request.data)
        if seralizer.is_valid():
            return Response(seralizer.data, status=status.HTTP_200_OK)
        else:
            return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSearchSerializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]

    def post(self, request):
        if request.POST.get('search') is None:
            return Response({"message": "Please Provide something to search"}, status=status.HTTP_400_BAD_REQUEST)
        search_key = request.data['search']
        objs = User.objects.filter(
            Q(id__contains=search_key) |
            Q(first_name__contains=search_key) |
            Q(last_name__contains=search_key) |
            Q(email__contains=search_key) |
            Q(username__contains=search_key)
        )
        if objs:
            serializer = UserSearchSerializer(objs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'No such user found'}, status=status.HTTP_204_NO_CONTENT)


class UserUpdateApiView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication,SessionAuthentication]

    def put(self, request):
        data = request.data
        serializer = UserUpdateSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
