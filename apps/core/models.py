from django.db import models
from django.contrib.auth.models import User

class Loginhistory(models.Model):
    login_time = models.DateTimeField()
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')

    class Meta:
        db_table = 'core_loginhistory'
        verbose_name = 'Login History'
        verbose_name_plural = 'Login Histories'

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


class Companyprofile(models.Model):
    name = models.CharField(max_length=200, default='GMT Reborn')
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='NPWP')
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    fiscal_year_start = models.DateField(blank=True, null=True)
    fiscal_year_end = models.DateField(blank=True, null=True)
    date_format = models.CharField(max_length=20, default='d/m/Y')
    currency = models.CharField(max_length=3, default='IDR')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'core_companyprofile'
        verbose_name = 'Company Profile'
        verbose_name_plural = 'Company Profiles'

    def __str__(self):
        return self.name

    @classmethod
    def get_profile(cls):
        profile, created = cls.objects.get_or_create(id=1)
        return profile
