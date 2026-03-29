from django.db import models
from django.contrib.auth.models import User


class Companyprofile(models.Model):
    """Auto-synced from database table: core_companyprofile"""
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=254)
    tax_id = models.CharField(max_length=50)
    logo = models.CharField(max_length=100, blank=True, null=True)
    fiscal_year_start = models.DateField(blank=True, null=True)
    fiscal_year_end = models.DateField(blank=True, null=True)
    date_format = models.CharField(max_length=20)
    currency = models.CharField(max_length=3)
    updated_at = models.TextField()
    updated_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'core_companyprofile'
        verbose_name = 'core_companyprofile'
        verbose_name_plural = 'core_companyprofile'
    
    def __str__(self):
        return str(self.id)
