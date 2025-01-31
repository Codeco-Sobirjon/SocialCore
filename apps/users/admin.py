from django.contrib import admin
from apps.users.models import (
    DemographicData, MedicalHistory, Notes, Interests, MedicalIllness,
    DiseaseHistoryDaily
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



