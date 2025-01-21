from django.contrib.auth.models import User
from rest_framework import serializers

from task_calendar_backend.models import Task


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password= serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields ='__all__'
    def validate(self,data):
        if len(data['username'])>10:
            raise ValueError('Username must be at most 10 characters')
        if data['password'] != data['confirm_password']:
            raise ValueError('Passwords must match')
        return data

    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password= validated_data["password"]
        )
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
