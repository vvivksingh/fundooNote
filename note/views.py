import json
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note
from .serializers import NotesSerializer

from .utils import verify_token

from .utils import RedisCache, RedisService

logging.basicConfig(filename="notes.log", filemode="w")


class Notes(APIView):
    """
    class based views for crud operation
    """

    # @swagger_auto_schema(
    #     operation_summary="login",
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             'title': openapi.Schema(type=openapi.TYPE_STRING, description='title'),
    #             'description': openapi.Schema(type=openapi.TYPE_STRING, description='description'),
    #         }
    #     ))

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="Add notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description"),
                'color': openapi.Schema(type=openapi.TYPE_STRING, description="color"),
                'is_archieved': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="archive"),
            }
        )

    )
    @verify_token
    def post(self, request):

        """
        this method is created for inserting the data
        :param request: format of the request
        :return: Response
        """
        print("--------------")
        print(request.data)
        print(request.user)
        try:
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisCache.add_note(serializer.data)

            return Response(
                {
                    "message": "Notes created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="get note by user_id")
    @verify_token
    def get(self, request):
        """
        this method is created for retrieve data
        :param request: format of the request
        :return: Response
        """
        try:
            # note_list = Note.objects.all()

            # note = Note.objects.filter(user_id=request.data.get("user_id"))
            # serializer = NotesSerializer(note_list, many=True)
            # print(serializer.data)

            redis_data = RedisCache().get_note(user_id=request.data.get("user_id"))
            list_data = []
            # for key in redis_data:
            #     list_data.append(redis_data.get(key))
            for key, value in redis_data.items():
                list_data.append(value)

            return Response(
                {
                    "message": "Your Note's",
                    "data": list_data
                },
                status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "No notes found"
                },
                status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="Update notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="id"),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description"),
                'color': openapi.Schema(type=openapi.TYPE_STRING, description="color"),
                'is_archived': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="archive"),

            }
        ))
    @verify_token
    def put(self, request):
        """
        To update a previous note
        :param request:
        :return:
        """
        try:
            note = Note.objects.get(id=request.data.get("id"))
            serializer = NotesSerializer(note, data=request.data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisCache().update_note(serializer.data)
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
            note = Note.objects.get(id=request.data.get("id"))
            note.delete()
            RedisCache.delete_note(request.data.get("user_id"), request.data.get("id"))
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


# class ColorUpdate(APIView):
#     @verify_token
#     @swagger_auto_schema(manual_parameters=[
#         openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING)
#     ], operation_summary="update note's color", request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'color': openapi.Schema(type=openapi.TYPE_STRING, description="color"),
#                 'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="id")
#             }
#         ))
#     def put(self,request, pk):
#         note = Note.objects.get(pk=pk)
#         note.color = request.data.get("color")
#         note.save()
#         return Response(
#             {
#                 "message": "Color Updated"
#             }
#         )


# class ArchieveUpdate(APIView):
#     @verify_token
#     @swagger_auto_schema(manual_parameters=[
#         openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING)
#     ], operation_summary="update archive")
#     def put(self,request, pk):
#         note = Note.objects.get(pk=pk)
#         note.is_archived = True if note.is_archived is True else False
#         note.save()
#         return Response(
#             {
#                 "message": "Archive Updated"
#             }
#         )

class GetSpecific(APIView):
    @verify_token
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="get note by user_id")
    def get(self, request, pk=None):

        """
        this method is created for retrieve data
        :param request: format of the request
        :return: Response
        """
        try:
            note = Note.objects.filter(user_id=request.data.get("user_id"))
            serializer = NotesSerializer(note, many=True)
            redis_data = RedisCache.get_note(user_id=request.data.get("user_id"))

            specific_note = redis_data.get(str(pk))
            if specific_note is None:
                return Response({"msg": "Data Not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response(
                {
                    "message": "Your Note's",
                    "data": specific_note
                },
                status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "No notes found"
                },
                status=status.HTTP_400_BAD_REQUEST)
