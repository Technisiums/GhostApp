from django.urls import path
from .views import UserCreateAPIView,UserLogInAPIView,UserSearchAPIView,UserUpdateApiView

urlpatterns = [
    path('create/', UserCreateAPIView.as_view()),
    path('login/', UserLogInAPIView.as_view()),
    path('search/', UserSearchAPIView.as_view()),
    path('update/', UserUpdateApiView.as_view()),
]
"""
create
login
search
change credentials
change personal info

"""

#cf0093eb3d8583c412e6a7217b7b6c62ab326f00