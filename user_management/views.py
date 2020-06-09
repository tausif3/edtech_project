from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .serializers import SignUpStudent_Serializer,SignUpEducator_Serializer
from rest_framework import status
from rest_framework.decorators import api_view
import requests
import json
from . import user_management_utils as user_utils
from . import constants


def index(request):
    # test view
    return HttpResponse("hello world")


@csrf_exempt
@api_view(['POST'])
def signup_student(request):

    signup_student_serializer = SignUpStudent_Serializer(data=request.data)
        
    if signup_student_serializer.is_valid():
        signup_student_serializer.save()
        return JsonResponse(signup_student_serializer.data,status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(signup_student_serializer.errors,status=400)


@csrf_exempt
@api_view(['POST'])
def signup_educator(request):
    signup_educator_serializer = SignUpEducator_Serializer(data=request.data)

    if signup_educator_serializer.is_valid():
        signup_educator_serializer.save()
        return JsonResponse(signup_educator_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(signup_educator_serializer.errors, status=400)


@csrf_exempt
@api_view(['POST'])
def login_student(request):
    username = request.data['username']
    password = request.data['password']

    payload = {'username': username, 'password': password}
    headers = {'content-type': 'application/json'}

    obtain_jwt_token = requests.post(url='http://127.0.0.1:8000/api/token/', data=json.dumps(payload), headers=headers)
    if obtain_jwt_token.status_code == 200:
        data = json.loads(obtain_jwt_token.text)
        redis_token = user_utils.setex_jwt_token(username=username,
                                                 time=constants.REDIS_CONSTANTS['TIMEOUT'],
                                                 token=data['access'])

        if redis_token:
            return JsonResponse({"sucess": data})
    else:
        return JsonResponse({"message": obtain_jwt_token.reason}, status=obtain_jwt_token.status_code)


@csrf_exempt
@api_view(['POST'])
def login_educator(request):
    username = request.data['username']
    password = request.data['password']

    payload = {'username': username, 'password': password}
    headers = {'content-type': 'application/json'}

    obtain_jwt_token = requests.post(url='http://127.0.0.1:8000/api/token/', data=json.dumps(payload), headers=headers)
    if obtain_jwt_token.status_code == 200:
        data = json.loads(obtain_jwt_token.text)
        redis_token = user_utils.setex_jwt_token(username=username,
                                                 time=constants.REDIS_CONSTANTS['TIMEOUT'],
                                                 token=data['access'],)

        if redis_token:
            return JsonResponse({"sucess": data})
    else:
        return JsonResponse({"message": obtain_jwt_token.reason}, status=obtain_jwt_token.status_code)


