import json
from django.shortcuts import render
from .documents import ServerDocument
from .models import Server
from django.core.exceptions import ObjectDoesNotExist
from .tasks import log_search
from .serializers import UserRegisterSerializer, UserLoginSerializer, ServerSerializer
from .utils import generate_access_token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
import jwt
from django.contrib.auth.models import User
from django.conf import settings


class SearchAPIView(APIView):
    def convert_to_es_query(self, key, value):
        return {"wildcard": {key: f"*{value}*"}}

    def get(self, request):

        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return Response({"detail": "Authorization header is missing!"}, status=status.HTTP_401_UNAUTHORIZED)
        # Extract the token from the Authorization header
        try:
            authorization_key, access_token = authorization_header.split(" ")
            if not authorization_key == "Octoxlabs":
                return Response({"detail": "Invalid Authorization header format!"}, status=status.HTTP_401_UNAUTHORIZED)

            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.filter(id=payload['user_id']).first()

        except ValueError:
            return Response({"detail": "Invalid Authorization header format."}, status=status.HTTP_401_UNAUTHORIZED)

        except ObjectDoesNotExist:
            return Response({"detail": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED)
        if not user:
            return Response({"detail": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user_query = self.request.data
            print(f"user_query {user_query} and {type(user_query)}")
            if type(user_query) is str:
                key, value = user_query.split("=")
                key = key.strip().lower()
                value = value.strip()
                if key == "hostname":
                    query = self.convert_to_es_query(key, value)
                    servers = ServerDocument.search().query(query)

                    task_result = log_search.apply_async(
                        args=[],
                        kwargs={
                            "username": user.username,
                            "key": key,
                            "value": value,
                        }
                    )
                    # Serialize the data
                    serializer = ServerSerializer(servers, many=True)

                    # Return the serialized data in the response
                    return Response({"octoxlabsdata": serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'key is not valid'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response({'error': 'Input format must be str "'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except ValueError as ve:
            return Response({'error': 'Invalid JSON'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class UserRegistrationAPIView(APIView):
    serialization_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        context = {"message": "Hello"}
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serialization_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            if new_user:
                access_token = generate_access_token(new_user)
                data = {"access_token": access_token}
                response = Response(data, status.HTTP_201_CREATED)
                response.set_cookie(key='access_token', value=access_token, httponly=True)
                return response
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = request.data.get('username', None)
            user_password = request.data.get('password', None)

            if not user_password:
                raise AuthenticationFailed('A user password is needed.')

            if not username:
                raise AuthenticationFailed('An user email is needed.')

            user_instance = authenticate(username=username, password=user_password)

            if not user_instance:
                raise AuthenticationFailed('User not found.')

            if user_instance.is_active:
                access_token = generate_access_token(user_instance)
                data = {"access_token": access_token}
                response = Response(data, status.HTTP_200_OK)
                response.set_cookie(key='access_token', value=access_token, httponly=True)
                return response

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserViewAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            raise AuthenticationFailed('Authorization header is missing.')

        # Extract the token from the Authorization header
        try:
            authorization_key, access_token = authorization_header.split(" ")
            if not authorization_key == "Octoxlabs":
                raise AuthenticationFailed(f'Invalid Authorization header formatx. {authorization_header}')
        except ValueError:
            raise AuthenticationFailed('Invalid Authorization header formaty.')

        if not access_token:
            raise AuthenticationFailed('Unauthenticated user.')

        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        try:
            user = User.objects.filter(id=payload['user_id']).first()
            user_serializer = UserRegisterSerializer(user)
        except:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

