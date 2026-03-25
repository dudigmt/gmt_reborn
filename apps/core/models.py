from django.db import models
from django.contrib.auth.models import User

class GMTSettings(models.Model):
    session_timeout = models.IntegerField(default=30)
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "GMT Setting"
        verbose_name_plural = "GMT Settings"
    
    def __str__(self):
        return f"GMT Settings (session: {self.session_timeout} minutes)"
    
    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(id=1)
        return settings

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-login_time']
        verbose_name_plural = "Login Histories"
    
    def __str__(self):
        return f"{self.user.username} - {self.login_time}"