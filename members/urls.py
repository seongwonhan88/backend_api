from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from members.views.signup import UserList

urlpatterns = [
    path('get_token/', obtain_jwt_token),
    path('users/', UserList.as_view()),
]