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

class CompanyProfile(models.Model):
    """Data profil perusahaan"""
    name = models.CharField(max_length=200, default='GMT Reborn')
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    tax_id = models.CharField(max_length=50, blank=True, verbose_name='NPWP')
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    
    fiscal_year_start = models.DateField(null=True, blank=True, help_text='Start of fiscal year')
    fiscal_year_end = models.DateField(null=True, blank=True, help_text='End of fiscal year')
    
    date_format = models.CharField(max_length=20, default='d/m/Y', help_text='Date format (d/m/Y, m/d/Y, etc)')
    currency = models.CharField(max_length=3, default='IDR')
    
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Company Profile"
    
    def __str__(self):
        return self.name
    
    @classmethod
    def get_profile(cls):
        """Singleton - hanya ada 1 record"""
        profile, created = cls.objects.get_or_create(id=1)
        return profile

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