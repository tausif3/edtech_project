from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/student', views.signup_student),
    path('signup/educator', views.signup_educator),
    path('login/student', views.login_student),
    path('login/educator', views.login_educator),
    path('new_access_token', views.new_access_token),

]
