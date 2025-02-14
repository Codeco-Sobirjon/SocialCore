from django.contrib import admin
from apps.users.models import (
    DemographicData, MedicalHistory, Notes, Interests, MedicalIllness,
    DiseaseHistoryDaily, Followers
)


@admin.register(MedicalIllness)
class MedicalIllnessAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class DemographicDataTableInlines(admin.TabularInline):
    model = DemographicData
    extra = 1
    fields = ['city', 'region', 'position', 'ethnicity', 'type_health_insurance', 'biography']


class MedicalHistoryTableInlines(admin.TabularInline):
    model = MedicalHistory
    extra = 1
    fields = ['medical_illness', 'history', 'start_date']


class NotesTableInlines(admin.TabularInline):
    model = Notes
    extra = 1
    fields = ['id', 'notes', 'start_date']


class InterestsTableInlines(admin.TabularInline):
    model = Interests
    extra = 1
    fields = ['name']


class DiseaseHistoryDailyTableInlines(admin.TabularInline):
    model = DiseaseHistoryDaily
    extra = 1
    fields = ['name']


@admin.register(DemographicData)
class DemographicDataAdmin(admin.ModelAdmin):
    list_display = (
    'user', 'city', 'region', 'position', 'ethnicity', 'type_health_insurance', 'biography', 'is_activate',
    'created_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'city', 'region', 'position', 'ethnicity')
    ordering = ('-created_at',)


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'medical_illness', 'history', 'start_date', 'still_ongoing', 'is_activate', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'history', 'medical_illness__name')
    ordering = ('-created_at',)


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('user', 'notes', 'start_date', 'end_date', 'is_activate', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'notes')
    ordering = ('-created_at',)


@admin.register(Interests)
class InterestsAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_activate', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'name')
    ordering = ('-created_at',)


@admin.register(DiseaseHistoryDaily)
class DiseaseHistoryDailyAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_activate', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'name')
    ordering = ('-created_at',)


@admin.register(Followers)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ("user", "follow", "created_at")
    search_fields = ("user__username", "follow__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
