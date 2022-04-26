import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note
from .serializers import NotesSerializer

from .utils import verify_token

from .utils import RedisCache, RedisService

logging.basicConfig(filename="notes.log", filemode="w")


class NotesDetails(APIView):
    @verify_token
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


class Notes(APIView):
    """
    class based views for crud operation
    """

    @verify_token
    def post(self, request):
        """
        this method is created for inserting the data
        :param request: format of the request
        :return: Response
        """
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
            logging.error(e)
            return Response({"message": "validation failed"}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def get(self, request):
        """
        this method is created for retrieve data
        :param request: format of the request
        :return: Response
        """
        try:
            note = Note.objects.filter(user_id=request.data.get("user_id"))
            serializer = NotesSerializer(note, many=True)
            RedisCache().get_note(user_id=request.data.get("user_id"))
            return Response(
                {
                    "message": "Your Note's",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "No notes found"
                },
                status=status.HTTP_400_BAD_REQUEST)

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
            print(serializer)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisCache().update_note(serializer.data)
            return Response({"Message": "Note Updated", "Data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response({"message": "Note Update Failed", "error": "{}".format(e)},
                            status=status.HTTP_400_BAD_REQUEST)
