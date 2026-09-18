# board/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_column='author_id', verbose_name="작성자")

    class Meta:
        managed = False  # 기존 테이블을 활용, 마이그레이션으로 테이블을 변경/생성하지 않도록 설정
        db_table = 'board_post'
        ordering = ['-created_at']

    def __str__(self):
        return self.title