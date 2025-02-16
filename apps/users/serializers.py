from django.contrib.auth.models import Group
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.db import transaction

from apps.users.models import (
    DemographicData, MedicalHistory, Notes, Interests, MedicalIllness, DiseaseHistoryDaily, Followers
)
from apps.accounts.serializers import CustomUserDetailSerializer

User = get_user_model()


class GroupListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class DemographicDataListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemographicData
        fields = ['id', 'city', 'region', 'position', 'ethnicity', 'type_health_insurance', 'biography',
                  'user', 'created_at', 'is_activate']

    def create(self, validated_data):
        request = self.context.get('request')

        user = request.user if request and hasattr(request, 'user') else None

        with transaction.atomic():
            create = DemographicData.objects.create(
                **validated_data, user=user
            )
        return create

    def update(self, instance, validated_data):
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

        return instance


class DemographicDataSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer(read_only=True)

    class Meta:
        model = DemographicData
        fields = ['id', 'city', 'region', 'position', 'ethnicity', 'type_health_insurance', 'biography',
                  'user', 'created_at', 'is_activate']


class MedicalIllnessListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalIllness
        fields = ['id', 'name']


class MedicalHistoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ['id', 'medical_illness', 'history', 'start_date', 'still_ongoing', 'created_at', 'user',
                  'is_activate']

    def create(self, validated_data):
        request = self.context.get('request')

        user = request.user if request and hasattr(request, 'user') else None

        with transaction.atomic():
            create = MedicalHistory.objects.create(
                **validated_data, user=user
            )
        return create

    def update(self, instance, validated_data):
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

        return instance


class MedicalHistorySerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer(read_only=True)
    medical_illness = MedicalIllnessListSerializer(read_only=True)

    class Meta:
        model = MedicalHistory
        fields = ['id', 'medical_illness', 'history', 'start_date', 'still_ongoing', 'created_at', 'user',
                  'is_activate']


class NotesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'notes', 'start_date', 'end_date', 'created_at', 'is_activate']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request and hasattr(request, 'user') else None

        if not user:
            raise serializers.ValidationError({"user": "User not found in request context."})

        with transaction.atomic():
            note = Notes.objects.create(**validated_data, user=user)
        return note

    def update(self, instance, validated_data):
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

        return instance


class NotesSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer(read_only=True)

    class Meta:
        model = Notes
        fields = ['id', 'notes', 'start_date', 'end_date', 'created_at', 'user', 'is_activate']


class InterestsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interests
        fields = ['id', 'name', 'created_at', 'is_activate']

    def create(self, validated_data):
        request = self.context.get('request')

        user = request.user if request and hasattr(request, 'user') else None

        with transaction.atomic():
            create = Interests.objects.create(
                **validated_data, user=user
            )
        return create

    def update(self, instance, validated_data):
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

        return instance


class InterestsSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer(read_only=True)

    class Meta:
        model = Interests
        fields = ['id', 'name', 'created_at', 'user', 'is_activate']


class DiseaseHistoryDailyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseHistoryDaily
        fields = ['id', 'name', 'created_at', 'is_activate']

    def create(self, validated_data):
        request = self.context.get('request')

        user = request.user if request and hasattr(request, 'user') else None

        with transaction.atomic():
            create = DiseaseHistoryDaily.objects.create(
                **validated_data, user=user
            )
        return create

    def update(self, instance, validated_data):
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

        return instance


class DiseaseHistoryDailySerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer(read_only=True)

    class Meta:
        model = DiseaseHistoryDaily
        fields = ['id', 'name', 'created_at', 'user', 'is_activate']


class FollowersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = ['id', 'user', 'follow', 'created_at', 'is_activate']

    def create(self, validated_data):
        request = self.context.get('request')

        user = request.user if request and hasattr(request, 'user') else None

        with transaction.atomic():
            create = Followers.objects.create(
                **validated_data, user=user
            )
        return create

    def update(self, instance, validated_data):
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

        return instance


class FollowersSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer(read_only=True)
    follow = CustomUserDetailSerializer(read_only=True)

    class Meta:
        model = Followers
        fields = ['id', 'user', 'follow', 'created_at', 'is_activate']


class UserDetailSerializer(serializers.ModelSerializer):
    groups = GroupListsSerializer(many=True, read_only=True)
    user_demographic_data = DemographicDataListSerializer(read_only=True, many=True)
    user_medical_history = MedicalHistoryListSerializer(read_only=True, many=True)
    user_notes = NotesListSerializer(read_only=True, many=True)
    user_insterest = InterestsListSerializer(read_only=True, many=True)
    user_disease_history_daily = DiseaseHistoryDailyListSerializer(read_only=True, many=True)
    user_follow = FollowersListSerializer(read_only=True, many=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'groups', 'avatar', 'birth_date',
            'user_demographic_data', 'user_medical_history', 'user_notes', 'user_insterest',
            'user_disease_history_daily', 'user_follow'
        ]

