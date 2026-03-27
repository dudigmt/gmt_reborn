from django.db import models

class Module(models.Model):
    MODULE_TYPES = [
        ('hr', 'HR'),
        ('finance', 'Finance'),
        ('production', 'Production'),
        ('warehouse', 'Warehouse'),
    ]
    
    name = models.CharField(max_length=50, choices=MODULE_TYPES, unique=True)
    display_name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='bi-grid')
    is_enabled = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.display_name