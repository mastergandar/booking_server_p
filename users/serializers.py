from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from post_office import mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'password',
            'avatar',
            'status',
            'phone_number',
            'email',
            'bio',
            'rating',
            'is_verified',
            'created_at',
        ]
        read_only_fields = [
            'pk',
            'rating',
            'is_verified',
            'created_at',
        ]

    def validate(self, attrs):
        x = self.context['request']
        try:
            User.objects.get(email=attrs['email'])
            raise ValidationError({'email': 'User already exists.'})
        except User.DoesNotExist:
            pass

        try:
            from django.contrib.auth.password_validation import validate_password

            validate_password(attrs['password'])

        except Exception as e:
            from core.validators import CustomPasswordValidator

            chars = CustomPasswordValidator.SPECIAL_CHARS
            raise ValidationError(
                {'password': f'Password is too simple. Use 8 characters, digits, upper/lowercase letters and special chars: {chars}'}
            )

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):

        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            username=validated_data.get('username')
        )
        mail_subject = 'Activate your account.'
        current_site = get_current_site(self.context['request'])
        uid = user.pk
        token = user.activation_email_code
        activation_link = f"{current_site}/account/register/{uid}/{token}"
        message = f"Hello {user.username},\n{activation_link}"
        to_email = user.email
        mail.send(
            to_email,  # List of email addresses also accepted
            'register@roompesa.goodbit.dev',
            subject=mail_subject,
            message=message,
        )
        return user

    def to_representation(self, instance):

        ret = super(UserRegisterSerializer, self).to_representation(instance)

        return ret


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'avatar',
            'status',
            'phone_number',
            'email',
            'bio',
            'rating',
            'is_verified',
            'created_at',
        ]
        read_only_fields = [
            'pk',
            'rating',
            'is_verified',
            'created_at',
        ]

    def update(self, instance, validated_data):

        return super().update(instance, validated_data)

    def to_representation(self, instance):

        ret = super(UserSerializer, self).to_representation(instance)

        return ret
