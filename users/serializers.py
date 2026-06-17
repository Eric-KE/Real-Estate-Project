from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'phone', 'role', 'avatar']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({
                'password': 'Passwords do not match.'
            })
        
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [ 'id', 'email', 'first_name', 'last_name', 'full_name', 'phone', 'role', 'avatar']
