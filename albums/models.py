import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Album(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.CharField(max_length=255, verbose_name="이미지 경로")
    caption = models.TextField(blank=True, null=True, verbose_name="설명")
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="장소")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_column='author_id', verbose_name="작성자")

    class Meta:
        managed = False
        db_table = 'albums_album'
        ordering = ['-created_at']

    @property
    def image_url(self):
        """Cloudinary 전체 이미지 URL 생성"""
        if not self.image:
            return ""
        # 이미 전체 URL(http)인 경우 예외 처리
        if self.image.startswith('http'):
            return self.image
            
        cloud_name = settings.CLOUDINARY_CLOUD_NAME
        return f"https://res.cloudinary.com/{cloud_name}/image/upload/{self.image}"

    def __str__(self):
        return f"{self.location} - {self.caption[:20] if self.caption else ''}"