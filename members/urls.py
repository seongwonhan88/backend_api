from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from members.views.login import LoginView
from members.views.signup import UserList, EmailActivationView, reactivation_request, current_user

urlpatterns = [
    path('get_token/', obtain_jwt_token),
    path('users/', UserList.as_view()),
    path('<uid64>/<token>/', EmailActivationView.as_view()),
    path('reactivate/', reactivation_request),
    path('login/', LoginView.as_view()),
]