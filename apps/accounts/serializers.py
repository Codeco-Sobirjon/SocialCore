from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from captcha.models import CaptchaStore


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'placeholder': 'Введите пароль'})
    password_confirm = serializers.CharField(write_only=True, required=True,
                                             style={'placeholder': 'Введите повторение пароль'})
    captcha_key = serializers.CharField(write_only=True, required=True, style={'placeholder': 'Введите код Captcha'})
    captcha_value = serializers.CharField(write_only=True, required=True,
                                          style={'placeholder': 'Введите значение Captcha'})

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'birth_date',
                  'password', 'password_confirm', 'captcha_key', 'captcha_value', 'is_agree']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise ValidationError({"password_confirm": "Пароли не совпадают"})

        try:
            captcha = CaptchaStore.objects.get(hashkey=data['captcha_key'])
        except CaptchaStore.DoesNotExist:
            raise ValidationError({"captcha": "Неверный ключ CAPTCHA"})

        if captcha.response != data['captcha_value'].lower():
            raise ValidationError({"captcha": "Неверный код CAPTCHA"})

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        validated_data.pop('captcha_key', None)
        validated_data.pop('captcha_value', None)

        groups_data = get_object_or_404(Group, id=1)

        user = get_user_model().objects.create_user(
            **validated_data
        )

        if groups_data:
            user.groups.set([groups_data])

        user.save()
        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    captcha_key = serializers.CharField(write_only=True, required=True, style={'placeholder': 'Введите код Captcha'})
    captcha_value = serializers.CharField(write_only=True, required=True,
                                          style={'placeholder': 'Введите значение Captcha'})
    password = serializers.CharField(write_only=True, style={'placeholder': 'Введите пароль'})

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        if not identifier or not password:
            raise serializers.ValidationError("Ham telefon/parol, ham parol talab qilinadi")

        user_model = get_user_model()

        try:
            captcha = CaptchaStore.objects.get(hashkey=data['captcha_key'])
        except CaptchaStore.DoesNotExist:
            raise ValidationError({"captcha": "Неверный ключ CAPTCHA"})

        if captcha.response != data['captcha_value'].lower():
            raise ValidationError({"captcha": "Неверный код CAPTCHA"})

        user = user_model.objects.filter(username=identifier).first()

        if user is None:
            raise AuthenticationFailed("Noto‘g‘ri ma’lumotlar, foydalanuvchi topilmadi")

        if not user.check_password(password):
            raise AuthenticationFailed("Noto‘g‘ri ma’lumotlar, noto‘g‘ri parol")

        return {
            'user': user,
        }


class CustomUserDetailSerializer(serializers.ModelSerializer):
    groups = GroupListSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'groups', 'avatar', 'birth_date'
        ]


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'username', 'email', 'first_name', 'last_name', 'avatar', 'birth_date'
        ]

        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'birth_date': {'required': False},
            'avater': {'required': False}
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class PasswordUpdateSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
