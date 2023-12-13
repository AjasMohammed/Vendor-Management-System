from rest_framework import serializers
from home.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed


class SignUpSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=8, max_length=20, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user


class LogInSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        user_data = {
            'email': email,
            'password': password
        }

        if email and password:
            print(user_data)
            user = authenticate(**user_data)
            print(user)

            if user:
                tokens = TokenObtainPairSerializer.get_token(user)

                data = {
                    'refresh': str(tokens),
                    'access': str(tokens.access_token)
                }

                return data
        raise AuthenticationFailed(
            "Authentication credentials were not provided or are invalid.")
