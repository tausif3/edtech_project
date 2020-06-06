from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import SignUpStudent_Serializer,SignUpEducator_Serializer
from rest_framework import status
import json

def index(request):
    # test view
    return HttpResponse("hello world")


@csrf_exempt
def signup_student(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)

        signup_student_serializer = SignUpStudent_Serializer(data=request_data)
        
        if signup_student_serializer.is_valid():
            signup_student_serializer.save()
            return JsonResponse(signup_student_serializer.data,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(signup_student_serializer.errors,status=400)


@csrf_exempt
def signup_educator(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)

        signup_educator_serializer = SignUpEducator_Serializer(data=request_data)

        if signup_educator_serializer.is_valid():
            signup_educator_serializer.save()
            return JsonResponse(signup_educator_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(signup_educator_serializer.errors, status=400)

    return HttpResponse("success educator")


def login_student(request):
  return HttpResponse("success student")


def login_educator(request):
  return HttpResponse("success educator")


