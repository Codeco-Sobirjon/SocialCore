from rest_framework import serializers

from django.db import transaction

from apps.blog.models import (
    Blog, Directory, BlogImage, BlogViews
)

from apps.users.serializers import MedicalIllnessListSerializer


class BlogImagesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogImage
        fields = ['id', 'image']


class BlogSerializer(serializers.ModelSerializer):
    medical_illness = MedicalIllnessListSerializer(read_only=True)
    images = BlogImagesListSerializer(read_only=True, many=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'description', 'medical_illness', 'created_at', 'images'
        ]


class DirectorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Directory
        fields = [
            'id',  'title', 'description', 'created_at'
        ]
