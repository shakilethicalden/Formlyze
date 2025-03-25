from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']  # Added address and phone fields
        

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2']  # Added image field

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
    

        # Create new user
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'], 
        )
        user.set_password(validated_data['password'])
        user.save()
        return user





class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)