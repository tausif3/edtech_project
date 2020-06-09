from rest_framework import serializers
from .models import User,StudentInfo,EducatorInfo

class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','birth_date']

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                        email=validated_data['email'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'],
                                        educator=validated_data.get('educator',False),
                                        student=validated_data.get('student',False))
        user.set_password(validated_data['password'])
        user.save()
        return user


class SignUpEducator_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=True)

    class Meta:
        model = EducatorInfo
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['educator']=True
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
        user_data['student'] = True
        user_obj = User_Serializer.create(User_Serializer(),validated_data=user_data)
        validated_data['user_id'] = user_obj.id
        student = StudentInfo.objects.create(**validated_data)
        return student

