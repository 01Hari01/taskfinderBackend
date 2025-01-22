from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from task_calendar_backend.models import Task


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password','confirm_password']

    def validate(self, data):
        username = data.get('username', '')

        if len(username) > 10:
            raise serializers.ValidationError({"username": "Username must be at most 10 characters."})
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords must match.'})
        data['password'] = make_password(data['password'])

        # Clean up sensitive data (no need to send confirm_password to db)
        del data['confirm_password']
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
