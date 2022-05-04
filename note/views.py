import json
import logging

from django.db import connection
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note
from .serializers import NotesSerializer

from .utils import verify_token

# from .utils import RedisCache, RedisService

logging.basicConfig(filename="notes.log", filemode="w")

cursor = connection.cursor()


class Notes(APIView):
    """
    class based views for crud operation
    """

    @verify_token
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="Add notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description")
            }
        ))
    def post(self, request):

        """
        this method is created for inserting the data
        :param request: format of the request
        :return: Response
        """
        try:
            cursor.execute('INSERT into note_note (title,description,user_id_id) values (%s,%s,%s)',
                           [request.data.get('title'), request.data.get('description'), request.data.get('user_id')])
            serializer = NotesSerializer(data=request.data)
            print(serializer)
            serializer.is_valid(raise_exception=True)
            # serializer.save()
            # RedisCache.add_note(serializer.data)

            return Response(
                {
                    "message": "Notes created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response({"message": "validation failed"}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="get note by user_id")
    def get(self, request):
        """
        this method is created for retrieve data
        :param request: format of the request
        :return: Response
        """
        try:
            for notes in Note.objects.raw(
                    'SELECT id,description from note_note where user_id_id= %s', [request.data.get('user_id')]):
                note = Note.objects.filter(user_id=request.data.get("user_id"))
                serializer = NotesSerializer(note, many=True)
                print(serializer.data)

            # redis_data = RedisCache().get_note(user_id=request.data.get("user_id"))
            # list_data = []
            # # for key in redis_data:
            # #     list_data.append(redis_data.get(key))
            # for key, value in redis_data.items():
            #     list_data.append(value)

            return Response(
                {
                    "message": "Your Note's",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "No notes found"
                },
                status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="Update notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="id"),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description")
            }
        ))
    def put(self, request):
        """
        To update a previous note
        :param request:
        :return:
        """
        try:
            cursor.execute(
                'UPDATE  note_note SET title = %s,description=%s,WHERE user_id_id=%s AND id=%s',
                [request.data.get('title'), request.data.get('description'), request.data.get('user_id'),
                 request.data.get('id')])

            note = Note.objects.get(id=request.data.get("id"))
            serializer = NotesSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            # serializer.save()
            # RedisCache().update_note(serializer.data)
            return Response({"Message": "Note Updated", "Data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response({"message": "Note Update Failed", "error": "{}".format(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="delete note",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="note_id"),
            }
        ))
    def delete(self, request):
        """
        this method is created for delete the note
        :param request:
        :return: response
        """
        try:
            cursor.execute('DELETE FROM note_note WHERE id=%s', [request.data.get('id')])
            # note = Note.objects.get(id=request.data.get("id"))
            # note.delete()
            # RedisCache.delete_note(request.data.get("user_id"), request.data.get("id"))
            # RedisService().delete(user_id=request.data.get("user_id"),note_id=request.data.get("id"))
            return Response(
                {
                    "message": "Data deleted"
                },
                status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "Unable to delete"
                },
                status=status.HTTP_400_BAD_REQUEST)


# class GetSpecific(APIView):
#     @verify_token
#     @swagger_auto_schema(manual_parameters=[
#         openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING)
#     ], operation_summary="get note by user_id")
#     def get(self, request, pk=None):
#
#         """
#         this method is created for retrieve data
#         :param request: format of the request
#         :return: Response
#         """
#         try:
#             note = Note.objects.filter(user_id=request.data.get("user_id"))
#             serializer = NotesSerializer(note, many=True)
#             # redis_data = RedisCache.get_note(user_id=request.data.get("user_id"))
#
#             specific_note = redis_data.get(str(pk))
#             if specific_note is None:
#                 return Response({"msg": "Data Not found"}, status=status.HTTP_404_NOT_FOUND)
#
#             return Response(
#                 {
#                     "message": "Your Note's",
#                     "data": specific_note
#                 },
#                 status=status.HTTP_200_OK)
#         except Exception as e:
#             logging.error(e)
#             return Response(
#                 {
#                     "message": "No notes found"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST)
