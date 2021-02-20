from django.urls import path, re_path
from .views import LogoutView, RegisterView, SignView, UserProfileView, ProfileUpdate, change_password

urlpatterns = [

    path('login/', SignView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('userprofile/<int:user_id>/', UserProfileView.as_view(), name='userprofile'),
    path('userprofileupdate/<int:user_id>/', ProfileUpdate.as_view(), name='userprofileupdate'),
    path('password/', change_password, name='change_password'),

]
