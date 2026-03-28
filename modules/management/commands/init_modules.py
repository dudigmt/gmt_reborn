from django.core.management.base import BaseCommand
from modules.models import Module

class Command(BaseCommand):
    help = 'Initialize modules with default data'
    
    def handle(self, *args, **options):
        modules_data = [
            {'name': 'hr', 'display_name': 'HR Management', 'icon': 'bi-people', 'order': 1, 'description': 'Human resources management module', 'is_system': False},
            {'name': 'finance', 'display_name': 'Finance', 'icon': 'bi-calculator', 'order': 2, 'description': 'Financial management module', 'is_system': False},
            {'name': 'production', 'display_name': 'Production', 'icon': 'bi-gear', 'order': 3, 'description': 'Production management module', 'is_system': False},
            {'name': 'warehouse', 'display_name': 'Warehouse', 'icon': 'bi-box', 'order': 4, 'description': 'Warehouse management module', 'is_system': False},
            {'name': 'admin', 'display_name': 'Administration', 'icon': 'bi-shield-lock', 'order': 5, 'description': 'System administration module', 'is_system': True},
        ]
        
        for data in modules_data:
            Module.objects.update_or_create(
                name=data['name'],
                defaults=data
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully initialized modules'))