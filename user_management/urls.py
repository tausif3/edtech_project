from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('signup/student', views.signup_student),
    path('signup/educator', views.signup_educator),
    # path('signup/student', views.signup_student),
    # path('signup/educator', views.signup_educator),

]
