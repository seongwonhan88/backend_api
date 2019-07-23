from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from members.seiralizers.user import UserSerializer, UserSerializerWithToken
from members.tasks import dispatch_mail


@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request)
    return Response(serializer.data, status=status.HTTP_200_OK)


class UserList(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dispatch_mail.delay(serializer.instance.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)