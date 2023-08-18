from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User
from rest_framework.authtoken.models import Token


class SignUpSerializer(serializers.ModelSerializer):
    """This class implements the interface DRF will use to serve the sign up variables in the api

    Args:
        serializers (_type_): _description_
    """
    email = serializers.EmailField()
    mobile = serializers.CharField(max_length=11)
    account_number = serializers.CharField(max_length=10)
    fullname = serializers.CharField(max_length=300)
    password = serializers.CharField(write_only=True, min_length= 8)
    
    
    class Meta:
        model= User
        fields = [ 'email', 'mobile', 'fullname', 'password', 'account_number' ]


    def validate(self, attrs):
        """validation to check if email exists or not

        Args:
            attrs (_type_): _description_
        """

        email_exists = User.objects.filter(email=attrs.get('email')).exists()
        mobile_exists = User.objects.filter(mobile=attrs.get('mobile')).exists()
        account_exists = User.objects.filter(account_number=attrs.get('account_number')).exists()
        
        
        if email_exists:
            raise ValidationError('Email already exists')
        
        if mobile_exists:
            raise ValidationError('Phone Number already exists')
        
        if account_exists:
            raise ValidationError('Account Number already exists')
        
        return super().validate(attrs)
        

    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user
    


class LoginSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length= 8)

    class Meta:
        model= User
        fields = ['email', 'password']
