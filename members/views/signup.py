from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from members.exceptions import UserAlreadyActive, EmailNotFound
from members.seiralizers.user import UserSerializer, UserSerializerWithToken
from members.tasks import dispatch_mail
from members.token import account_activation_token


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


class EmailActivationView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request, uid64, token, format=None):
        """Activate link once the link has been clicked"""
        try:
            uid = force_text(urlsafe_base64_decode(uid64))
            user = get_user_model().objects.get(pk=uid)
            if user is not None and account_activation_token.check_token(user, token):
                user.date_joined = timezone.now()
                user.is_active = True
                user.save()
                return Response({"email": user.email}, status=status.HTTP_202_ACCEPTED)
        except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return Response({"error": ["Link Activation is Invalid"]}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def reactivation_request(request):
    try:
        email = request.data.get('email', None)
        print(email)
        user = get_user_model().objects.get(email=email)
    except get_user_model().DoesNotExist:
        raise EmailNotFound
    if user.is_active:
        raise UserAlreadyActive
    dispatch_mail.delay(user.pk)
    return Response({'message': [f'Verification email is sent to {user.email}']})
