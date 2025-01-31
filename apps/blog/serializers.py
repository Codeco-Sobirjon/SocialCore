from rest_framework import serializers

from django.db import transaction

from apps.blog.models import (
    Blog, Directory
)

from apps.users.serializers import MedicalIllnessListSerializer


class BlogSerializer(serializers.ModelSerializer):
    medical_illness = MedicalIllnessListSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'description', 'medical_illness', 'created_at'
        ]


class DirectorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Directory
        fields = [
            'id',  'title', 'description', 'created_at'
        ]
