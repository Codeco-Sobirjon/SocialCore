from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.db import transaction

from apps.users.models import (
    DemographicData, MedicalHistory, Notes, Interests, MedicalIllness, DiseaseHistoryDaily
)
from apps.accounts.serializers import CustomUserDetailSerializer

User = get_user_model()


class DemographicDataListSerializer(serializers.ModelSerializer):

    class Meta:
        model = DemographicData
        fields = ['id', 'city', 'region', 'position', 'ethnicity', 'type_health_insurance', 'biography',
                  'user', 'created_at']

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
                  'user', 'created_at']


class MedicalIllnessListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalIllness
        fields = ['id', 'name']


class MedicalHistoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalHistory
        fields = ['id', 'medical_illness', 'history', 'start_date', 'still_ongoing', 'created_at', 'user']

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
        fields = ['id', 'medical_illness', 'history', 'start_date', 'still_ongoing', 'created_at', 'user']


class NotesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notes
        fields = ['id', 'notes', 'start_date', 'end_date', 'created_at', 'user']

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


class NotesSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer(read_only=True)

    class Meta:
        model = Notes
        fields = ['id', 'notes', 'start_date', 'end_date', 'created_at', 'user']


class InterestsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interests
        fields = ['id', 'name', 'created_at', 'user']

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


class InterestsSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer(read_only=True)

    class Meta:
        model = Interests
        fields = ['id', 'name', 'created_at', 'user']


class DiseaseHistoryDailyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiseaseHistoryDaily
        fields = ['id', 'name', 'created_at', 'user']

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


class DiseaseHistoryDailySerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer(read_only=True)

    class Meta:
        model = DiseaseHistoryDaily
        fields = ['id', 'name', 'created_at', 'user']
