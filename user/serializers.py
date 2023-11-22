from rest_framework import serializers

from .models import User 


class RegisterUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone']
        labels = {
            'password': 'گذر واژه',
        }
