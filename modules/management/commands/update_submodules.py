from django.core.management.base import BaseCommand
from modules.models import Module

class Command(BaseCommand):
    help = 'Update submodules data for each module'
    
    def handle(self, *args, **options):
        submodules_data = {
            'hr': [
                {'name': 'employees', 'display_name': 'Employees', 'icon': 'fa-address-card', 'url': '/hr/employees/', 'order': 1, 'is_enabled': True},
                {'name': 'attendance', 'display_name': 'Attendance', 'icon': 'fa-clock', 'url': '/hr/attendance/', 'order': 2, 'is_enabled': True},
                {'name': 'payroll', 'display_name': 'Payroll', 'icon': 'fa-money-bill-wave', 'url': '/hr/payroll/', 'order': 3, 'is_enabled': True},
            ],
            'finance': [
                {'name': 'chart_of_accounts', 'display_name': 'Chart of Accounts', 'icon': 'fa-list', 'url': '/finance/accounts/', 'order': 1, 'is_enabled': True},
                {'name': 'journal_entries', 'display_name': 'Journal Entries', 'icon': 'fa-pen-to-square', 'url': '/finance/journal/', 'order': 2, 'is_enabled': True},
                {'name': 'financial_reports', 'display_name': 'Financial Reports', 'icon': 'fa-chart-simple', 'url': '/finance/reports/', 'order': 3, 'is_enabled': True},
            ],
            'production': [
                {'name': 'production_orders', 'display_name': 'Production Orders', 'icon': 'fa-clipboard-list', 'url': '/production/orders/', 'order': 1, 'is_enabled': True},
                {'name': 'bill_of_materials', 'display_name': 'Bill of Materials', 'icon': 'fa-diagram-project', 'url': '/production/bom/', 'order': 2, 'is_enabled': True},
                {'name': 'quality_control', 'display_name': 'Quality Control', 'icon': 'fa-check-double', 'url': '/production/quality/', 'order': 3, 'is_enabled': True},
            ],
            'warehouse': [
                {'name': 'inventory', 'display_name': 'Inventory', 'icon': 'fa-boxes', 'url': '/warehouse/inventory/', 'order': 1, 'is_enabled': True},
                {'name': 'stock_movement', 'display_name': 'Stock Movement', 'icon': 'fa-arrows-spin', 'url': '/warehouse/movement/', 'order': 2, 'is_enabled': True},
                {'name': 'receiving', 'display_name': 'Receiving', 'icon': 'fa-truck-ramp-box', 'url': '/warehouse/receiving/', 'order': 3, 'is_enabled': True},
            ],
        }
        
        for module_name, submodules in submodules_data.items():
            module = Module.objects.get(name=module_name)
            module.submodules = submodules
            module.save()
            self.stdout.write(f'Updated submodules for {module.display_name}')
        
        self.stdout.write(self.style.SUCCESS('Successfully updated all submodules'))