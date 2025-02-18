from django.db import models
from django.conf import settings


class DemographicData(models.Model):
    city = models.CharField(max_length=700, verbose_name="Страна", null=True, blank=True)
    region = models.CharField(max_length=700, verbose_name="Город", null=True, blank=True)
    position = models.CharField(max_length=700, verbose_name="Образование", null=True, blank=True)
    ethnicity = models.CharField(max_length=700, verbose_name="Этническая принадлежность", null=True, blank=True)
    type_health_insurance = models.CharField(max_length=700, verbose_name="Вид медицинской страховки", null=True,
                                             blank=True)
    biography = models.CharField(max_length=700, verbose_name="Биография", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='Демографические данные пользователя', related_name='user_demographic_data')
    is_activate = models.BooleanField(default=True, null=True, blank=True, verbose_name="Активируется")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()

    class Meta:
        verbose_name = "Демографические данные пользователя"
        verbose_name_plural = "1. Демографические данные пользователя"

    def __str__(self):
        return f"{self.user}"


class MedicalIllness(models.Model):
    name = models.CharField(max_length=700, verbose_name="Наименование заболеваний", null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Тип заболевания"
        verbose_name_plural = "2. Тип заболевания"

    def __str__(self):
        return f"{self.name}"


class MedicalHistory(models.Model):
    history = models.TextField(null=False, blank=False, verbose_name="Моя история болезни")
    start_date = models.DateField(null=True, blank=True, verbose_name="Дата начала")
    still_ongoing = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Все еще продолжается")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")
    medical_illness = models.ForeignKey(MedicalIllness, on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name='Тип заболевания', related_name='medical_illness')
    is_activate = models.BooleanField(default=True, null=True, blank=True, verbose_name="Активируется")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='История болезни пользователя', related_name='user_medical_history')

    objects = models.Manager()

    class Meta:
        verbose_name = "История болезни пользователя"
        verbose_name_plural = "3. История болезни пользователя"

    def __str__(self):
        return f"{self.user}"


class Notes(models.Model):
    notes = models.TextField(null=False, blank=False, verbose_name="Название заметки")
    start_date = models.DateField(null=True, blank=True, verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='Заметки пользователя', related_name='user_notes')
    is_activate = models.BooleanField(default=True, null=True, blank=True, verbose_name="Активируется")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()

    class Meta:
        verbose_name = "Заметки пользователя"
        verbose_name_plural = "4. Заметки пользователя"

    def __str__(self):
        return f"{self.user}"


class Interests(models.Model):
    name = models.CharField(max_length=700, verbose_name="Название интереса", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='Интерес пользователя', related_name='user_insterest')
    is_activate = models.BooleanField(default=True, null=True, blank=True, verbose_name="Активируется")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()

    class Meta:
        verbose_name = "Интерес пользователя"
        verbose_name_plural = "5. Интерес пользователя"

    def __str__(self):
        return f"{self.user}"


class DiseaseHistoryDaily(models.Model):
    name = models.TextField(null=True, blank=True, verbose_name='Ежедневное написание статей о болезнях')
    is_activate = models.BooleanField(default=True, null=True, blank=True, verbose_name="Активируется")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='Интерес пользователя', related_name='user_disease_history_daily')

    objects = models.Manager()

    class Meta:
        verbose_name = "История пользователя ежедневно"
        verbose_name_plural = "6. История пользователя ежедневно"

    def __str__(self):
        return f"{self.user}"


class Followers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name="Автор", related_name='author')
    follow = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name="Подписчик", related_name='user_follow')
    is_activate = models.BooleanField(default=True, null=True, blank=True, verbose_name="Активируется")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата подписки")

    objects = models.Manager()

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "7. Подписки"

    def __str__(self):
        return f"{self.user} → {self.follow}"
