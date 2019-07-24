from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from members.views.signup import UserList, EmailActivationView

urlpatterns = [
    path('get_token/', obtain_jwt_token),
    path('users/', UserList.as_view()),
    path('<uid64>/<token>/', EmailActivationView.as_view()),
]