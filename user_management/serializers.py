from rest_framework import serializers
from .models import User,StudentInfo,EducatorInfo

class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','birth_date']


class SignUpEducator_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=True)

    class Meta:
        model = EducatorInfo
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        # (new learning) passing serializer class this way
        user_obj = User_Serializer.create(User_Serializer(),validated_data=user_data)
        validated_data['user_id'] = user_obj.id
        educator = EducatorInfo.objects.create(**validated_data)
        return educator


class SignUpStudent_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=True)

    class Meta:
        model = StudentInfo
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_obj = User_Serializer.create(User_Serializer(),validated_data=user_data)
        validated_data['user_id'] = user_obj.id
        student = StudentInfo.objects.create(**validated_data)
        return student

