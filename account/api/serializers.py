from rest_framework import serializers
from django.conf import settings

from account import models
from djoser import serializers as dj_serializers


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MyUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


# Djoser

class UserCreateSerializer(dj_serializers.UserCreateSerializer):
    class Meta(dj_serializers.UserCreateSerializer.Meta):
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
        )

