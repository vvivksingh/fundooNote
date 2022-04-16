from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import NotesUserSerializer
from .models import NotesUser

from django.contrib.auth import authenticate


class UserRegistration(APIView):
    """
    class based views for User registration
    """

    def post(self, request):
        """
        this method is created for inserting the data
        :param request: format of the request
        :return: Response
        """
        serializer = NotesUserSerializer(data=request.data)

        if serializer.is_valid():
            user = NotesUser.objects.create_user(username=serializer.data.get('username'),
                                                 password=serializer.data.get('password'),
                                                 email=serializer.data.get('email'),
                                                 first_name=serializer.data.get('first_name'),
                                                 last_name=serializer.data.get('last_name'),
                                                 mobile=serializer.data.get('mobile'),
                                                 age=serializer.data.get('age'))
            return Response({
                "message": "User Registered Successfully "}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if user is not None:
            return Response({'msg': 'Login Successful'}, status=status.HTTP_200_OK)
        return Response({'errors': {'non_field_errors': ['email or password is not valid']}},
                        status=status.HTTP_400_BAD_REQUEST)
