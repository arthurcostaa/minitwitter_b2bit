from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', instance.password)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.set_password(password)
        instance.save()
        return instance

    def validate(self, data):
        user = CustomUser(**data)
        password = data.get('password')
        errors = {}

        if password:
            try:
                validate_password(password, user)
            except exceptions.ValidationError as e:
                errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return data

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'date_joined',
        ]
        read_only_fields = ['date_joined']
