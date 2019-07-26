from rest_framework import status
from rest_framework_jwt.views import ObtainJSONWebToken


class LoginView(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        return response
