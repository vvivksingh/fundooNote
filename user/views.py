import logging

from django.core.mail import send_mail
from django.http import HttpResponse

from .models import NotesUser

from fundooNotes import settings
from .serializers import NotesUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate

from .utils import EncodeDecodeToken

logging.basicConfig(filename="views.log", filemode="w")


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

            encoded_token = EncodeDecodeToken.encode_token(payload={"user_id": user.pk})
            send_mail(from_email=settings.EMAIL_HOST, recipient_list=[serializer.data['email']],
                      message="Thanks for using fundooNotes services\n Your activation token = "
                              "http://127.0.0.1:8000/user/api/{}".format(
                          encoded_token),
                      subject="Link for Your Registration", fail_silently=False, )
            return Response({
                "message": "User Registered Successfully ",
                "token": "{}".format(encoded_token)}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        """
        For login of user
        :param request:
        :return:response
        """
        try:
            user = authenticate(username=request.data.get("username"), password=request.data.get("password"))

            if user is not None:
                token = EncodeDecodeToken.encode_token(payload={"user_id": user.pk})
                return Response({"message": "Login Successfully!!", "token": "{}".format(token)},
                                status=status.HTTP_201_CREATED)

            return Response({
                "message": "login Failed"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as excp:

            logging.error(excp)
            return Response({"error": "{}".format(excp)}, status=status.HTTP_400_BAD_REQUEST)


class ValidateToken(APIView):
    def get(self, request, token):
        """
        validating user through token
        :param request:
        :param token:
        :return:Response
        """
        try:

            decoded_token = EncodeDecodeToken.decode_token(token)
            user = NotesUser.objects.get(id=decoded_token.get('user_id'))
            user.is_verified = True
            user.save()
            return Response({"message": "Validation Successfully"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return HttpResponse(e)
