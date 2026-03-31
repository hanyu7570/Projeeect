from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 用户角色
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "管理员"
        ENGINEER = "ENGINEER", "工程师"
        VIEWER = "VIEWER", "查看员"

    # 扩展字段
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ENGINEER,
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"