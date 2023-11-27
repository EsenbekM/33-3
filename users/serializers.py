from rest_framework import serializers
from django.contrib.auth.models import User


class UserValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=255)


class UserLoginSerializer(UserValidateSerializer):
    pass


class UserRegisterSerializer(UserValidateSerializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=50, required=False)
    last_name = serializers.CharField(max_length=50, required=False)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists!')
        return username
    
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters!')
        if password.isdigit():
            raise serializers.ValidationError('Password must contain letters!')
        if password.isalpha():
            raise serializers.ValidationError('Password must contain numbers!')
        return password
    

class UserProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'is_staff', 'is_superuser', 'is_active', 'date_joined',
                  'last_login']