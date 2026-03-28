from django.db import models
# from django.contrib.postgres.fields import JSONField
from django.db.models import JSONField

class Module(models.Model):
    MODULE_TYPES = [
        ('hr', 'HR'),
        ('finance', 'Finance'),
        ('production', 'Production'),
        ('warehouse', 'Warehouse'),
        ('admin', 'Administration'),
    ]
    
    name = models.CharField(max_length=50, choices=MODULE_TYPES, unique=True)
    display_name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='bi-grid')
    is_enabled = models.BooleanField(default=True)
    is_system = models.BooleanField(default=False)  # System modules cannot be disabled/deleted
    order = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    submodules = JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.display_name