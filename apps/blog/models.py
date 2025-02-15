from django.conf import settings
from django.db import models

from apps.users.models import MedicalIllness


class Blog(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True, verbose_name="Название")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    medical_illness = models.ForeignKey(MedicalIllness, on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name='Тип заболевания', related_name='blog_medical_illness')
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()

    class Meta:
        verbose_name = "Блоги"
        verbose_name_plural = "Блоги"

    def __str__(self):
        return f"{self.title} {self.medical_illness.name}"


class BlogImage(models.Model):
    image = models.ImageField(upload_to='blog/images/', null=True, blank=True, verbose_name='')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images', verbose_name="Блог")

    objects = models.Manager()

    def __str__(self):
        return f"Blog: {self.blog}"

    class Meta:
        verbose_name = "Изображения блога"
        verbose_name_plural = "Изображения блога"


class BlogViews(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='views', verbose_name="Блог")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='Кто это видел?', related_name='user_blog_views')
    last_viewed_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего просмотра")

    objects = models.Manager()

    def __str__(self):
        return f"Blog: {self.blog}"

    class Meta:
        verbose_name = "Просмотры блога"
        verbose_name_plural = "Просмотры блога"


class Directory(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True, verbose_name="Название")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочник"

    def __str__(self):
        return f"{self.title}"
