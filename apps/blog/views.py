from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.utils import timezone

from apps.blog.filters import BlogFilter
from apps.blog.models import Blog, Directory, BlogViews
from apps.blog.pagination import BlogPageNumberPagination
from apps.blog.serializers import BlogSerializer, DirectorySerializer


class BlogListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Blog'],
        operation_description="Retrieve a list of all blogs with optional filters and pagination",
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description="Filter by title", type=openapi.TYPE_STRING),
            openapi.Parameter('medical_illness', openapi.IN_QUERY, description="Filter by medical illness ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('created_at', openapi.IN_QUERY, description="Filter by creation date range", type=openapi.TYPE_STRING),
            openapi.Parameter('new', openapi.IN_QUERY, description="Filter by New blogs", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('old', openapi.IN_QUERY, description="Filter by Old blogs", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('popular', openapi.IN_QUERY, description="Filter by Popular blogs", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of results per page", type=openapi.TYPE_INTEGER),
        ],
        responses={200: BlogSerializer(many=True)}
    )
    def get(self, request):
        blogs = Blog.objects.all()
        filtered_blogs = BlogFilter(request.GET, queryset=blogs).qs

        paginator = BlogPageNumberPagination()
        paginated_blogs = paginator.paginate_queryset(filtered_blogs, request)
        serializer = BlogSerializer(paginated_blogs, many=True)
        return paginator.get_paginated_response(serializer.data)


class BlogDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Blog'],
        operation_description="Retrieve blog details by ID",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Blog ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: BlogSerializer()}
    )
    def get(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        user = request.user

        blog_view = BlogViews.objects.filter(blog=blog, user=user).first()

        if blog_view:
            blog_view.last_viewed_at = timezone.now()
            blog_view.save()
            serializer = BlogSerializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)

        BlogViews.objects.create(blog=blog, user=user, last_viewed_at=timezone.now())
        blog.views_count = blog.views_count + 1
        blog.save()

        serializer = BlogSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DirectoryListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Directory'],
        operation_description="Retrieve a list of all directories",
        responses={200: DirectorySerializer(many=True)}
    )
    def get(self, request):
        directories = Directory.objects.all()
        serializer = DirectorySerializer(directories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DirectoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Directory'],
        operation_description="Retrieve directory details by ID",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Directory ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: DirectorySerializer()}
    )
    def get(self, request, id):
        directory = get_object_or_404(Directory, id=id)
        serializer = DirectorySerializer(directory)
        return Response(serializer.data, status=status.HTTP_200_OK)
