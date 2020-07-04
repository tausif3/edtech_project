import json
import requests

# from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view

from . import (
    constants,
    serializers,
    models,
    user_management_utils as utils
)


def home(request):
    # move to separate app if needed
    response = render(request, 'home.html', {})
    return response

###! Move the following to api.py

@csrf_exempt
@api_view(['POST'])
def signup_student(request):
    signup_student_serializer = serializers.SignUpStudent_Serializer(data=request.data)
    if signup_student_serializer.is_valid():
        signup_student_serializer.save()
        return JsonResponse(signup_student_serializer.data,status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(signup_student_serializer.errors,status=400)

@csrf_exempt
@api_view(['POST'])
def signup_educator(request):
    signup_educator_serializer =  serializers.SignUpEducator_Serializer(data=request.data)
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

    # check whether 'user' is an educator or student
    user_type = models.User.objects.get(username=username)
    if user_type.educator:
        return JsonResponse({"message": "student access only"})

    payload = {'username': username, 'password': password}
    headers = {'content-type': 'application/json'}

    # jwt library does authentication internally and then generates a token based on user credentials
    obtain_jwt_token = requests.post(url='/api/token/', data=json.dumps(payload), headers=headers)
    if obtain_jwt_token.status_code == 200:
        data = json.loads(obtain_jwt_token.text)
        redis_token = utils.setex_jwt_token(token=data['access'],
                                                 time=constants.REDIS_CONSTANTS['TIMEOUT'],
                                                 username=username,)

        if redis_token:
            return JsonResponse({"success": data})
    else:
        return JsonResponse({"message": obtain_jwt_token.reason}, status=obtain_jwt_token.status_code)


@csrf_exempt
@api_view(['POST'])
def login_educator(request):
    username = request.data['username']
    password = request.data['password']

    # check whether 'user' is an educator or student
    user_type = models.User.objects.get(username=username)
    if user_type.student:
        return JsonResponse({"message": "educator access only"})

    payload = {'username': username, 'password': password}
    headers = {'content-type': 'application/json'}

    # jwt library does authentication internally and then generates a token based on user credentials
    obtain_jwt_token = requests.post(url='/api/token/', data=json.dumps(payload), headers=headers)
    if obtain_jwt_token.status_code == 200:
        data = json.loads(obtain_jwt_token.text)

        redis_token = utils.setex_jwt_token(token=data['access'],
                                                 time=constants.REDIS_CONSTANTS['TIMEOUT'],
                                                 username=username,)

        if redis_token:
            return JsonResponse({"success": data})
    else:
        return JsonResponse({"message": obtain_jwt_token.reason}, status=obtain_jwt_token.status_code)


@csrf_exempt
@api_view(['POST'])
def new_access_token(request):
    """
    API for obtaining new access token for given refresh token ( 1 day expiration time of refresh token)

    :param request:
    :return: new access token
    """

    payload = {'refresh': request.data['refresh']}
    headers = {'content-type': 'application/json'}

    access_token = requests.post(url='/api/token/refresh/',
                                     data=json.dumps(payload), headers=headers)

    if access_token.status_code == 200:
        data = json.loads(access_token.text)
        return JsonResponse({"success": data})





















