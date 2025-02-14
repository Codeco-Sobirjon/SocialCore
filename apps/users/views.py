from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

from apps.users.models import (
    DemographicData, MedicalHistory, Notes, Interests, DiseaseHistoryDaily, MedicalIllness, Followers
)
from apps.users.serializers import (
    DemographicDataListSerializer, DemographicDataSerializer,
    MedicalHistoryListSerializer, MedicalHistorySerializer,
    NotesListSerializer, NotesSerializer,
    InterestsListSerializer, InterestsSerializer,
    DiseaseHistoryDailyListSerializer, DiseaseHistoryDailySerializer, MedicalIllnessListSerializer,
    FollowersSerializer, FollowersListSerializer
)


class DemographicDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: DemographicDataSerializer(many=True)},
        tags=['Demographic Data']
    )
    def get(self, request):
        data = DemographicData.objects.select_related('user').filter(user=request.user)
        serializer = DemographicDataSerializer(data, many=True, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=DemographicDataListSerializer, tags=['Demographic Data'])
    def post(self, request):
        serializer = DemographicDataListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DemographicDataDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: DemographicDataSerializer()}, tags=['Demographic Data'])
    def get(self, request, pk):
        data = get_object_or_404(DemographicData, pk=pk, user=request.user)
        serializer = DemographicDataSerializer(data, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=DemographicDataListSerializer, tags=['Demographic Data'])
    def put(self, request, pk):
        data = get_object_or_404(DemographicData, pk=pk, user=request.user)
        serializer = DemographicDataListSerializer(instance=data, data=request.data, partial=True,
                                                   context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'}, tags=['Demographic Data'])
    def delete(self, request, pk):
        data = get_object_or_404(DemographicData, pk=pk, user=request.user)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MedicalHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: MedicalHistorySerializer(many=True)}, tags=['Medical History'])
    def get(self, request):
        data = MedicalHistory.objects.select_related('user').filter(user=request.user)
        serializer = MedicalHistorySerializer(data, many=True, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MedicalHistoryListSerializer, tags=['Medical History'])
    def post(self, request):
        serializer = MedicalHistoryListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicalHistoryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: MedicalHistorySerializer()}, tags=['Medical History'])
    def get(self, request, pk):
        data = get_object_or_404(MedicalHistory, pk=pk, user=request.user)
        serializer = MedicalHistorySerializer(data, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MedicalHistoryListSerializer, tags=['Medical History'])
    def put(self, request, pk):
        data = get_object_or_404(MedicalHistory, pk=pk, user=request.user)
        serializer = MedicalHistoryListSerializer(data, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'}, tags=['Medical History'])
    def delete(self, request, pk):
        data = get_object_or_404(MedicalHistory, pk=pk, user=request.user)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: NotesSerializer(many=True)}, tags=['Notes Data'])
    def get(self, request):
        data = Notes.objects.select_related('user').filter(user=request.user)
        serializer = NotesSerializer(data, many=True, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=NotesListSerializer, tags=['Notes Data'])
    def post(self, request):
        serializer = NotesListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotesDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: MedicalHistorySerializer()}, tags=['Notes Data'])
    def get(self, request, pk):
        data = get_object_or_404(Notes, pk=pk, user=request.user)
        serializer = NotesSerializer(data, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=NotesListSerializer, tags=['Notes Data'])
    def put(self, request, pk):
        data = get_object_or_404(Notes, pk=pk, user=request.user)
        serializer = NotesListSerializer(data, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'}, tags=['Notes Data'])
    def delete(self, request, pk):
        data = get_object_or_404(Notes, pk=pk, user=request.user)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InterestsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: InterestsSerializer(many=True)}, tags=['Interests Data'])
    def get(self, request):
        data = Interests.objects.select_related('user').filter(user=request.user)
        serializer = InterestsSerializer(data, many=True, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=InterestsListSerializer, tags=['Interests Data'])
    def post(self, request):
        serializer = InterestsListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InterestsDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: InterestsSerializer()}, tags=['Interests Data'])
    def get(self, request, pk):
        data = get_object_or_404(Interests, pk=pk, user=request.user)
        serializer = InterestsSerializer(data, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=InterestsListSerializer, tags=['Interests Data'])
    def put(self, request, pk):
        data = get_object_or_404(Interests, pk=pk, user=request.user)
        serializer = InterestsListSerializer(data, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'}, tags=['Interests Data'])
    def delete(self, request, pk):
        data = get_object_or_404(Interests, pk=pk, user=request.user)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DiseaseHistoryDailyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: DiseaseHistoryDailySerializer(many=True)}, tags=['Disease History Daily Data'])
    def get(self, request):
        data = DiseaseHistoryDaily.objects.select_related('user').filter(user=request.user)
        serializer = DiseaseHistoryDailySerializer(data, many=True, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=DiseaseHistoryDailyListSerializer, tags=['Disease History Daily Data'])
    def post(self, request):
        serializer = DiseaseHistoryDailyListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiseaseHistoryDailyDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: DiseaseHistoryDailySerializer()}, tags=['Disease History Daily Data'])
    def get(self, request, pk):
        data = get_object_or_404(DiseaseHistoryDaily, pk=pk, user=request.user)
        serializer = DiseaseHistoryDailySerializer(data, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=DiseaseHistoryDailyListSerializer, tags=['Disease History Daily Data'])
    def put(self, request, pk):
        data = get_object_or_404(DiseaseHistoryDaily, pk=pk, user=request.user)
        serializer = DiseaseHistoryDailyListSerializer(data, data=request.data, partial=True,
                                                       context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'}, tags=['Disease History Daily Data'])
    def delete(self, request, pk):
        data = get_object_or_404(DiseaseHistoryDaily, pk=pk, user=request.user)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MedicalIllnessAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: MedicalIllnessListSerializer(many=True)}, tags=['MedicalIllness Data'])
    def get(self, request):
        data = MedicalIllness.objects.all()
        serializer = MedicalIllnessListSerializer(data, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: FollowersSerializer(many=True)}, tags=['Followers'])
    def get(self, request):
        data = Followers.objects.select_related('user').filter(user=request.user)
        serializer = FollowersSerializer(data, many=True, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=FollowersListSerializer, tags=['Followers'])
    def post(self, request):
        serializer = FollowersListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowersDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: FollowersSerializer()}, tags=['Followers'])
    def get(self, request, pk):
        data = get_object_or_404(Followers, pk=pk, user=request.user)
        serializer = FollowersSerializer(data, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=FollowersListSerializer, tags=['Followers'])
    def put(self, request, pk):
        data = get_object_or_404(Followers, pk=pk, user=request.user)
        serializer = FollowersListSerializer(data, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'}, tags=['Followers'])
    def delete(self, request, pk):
        data = get_object_or_404(Followers, pk=pk, user=request.user)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
