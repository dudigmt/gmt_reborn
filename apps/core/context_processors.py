from modules.models import Module

def gmt_settings(request):
    try:
        # GMTSettings model sudah dihapus, pake default 30
        return {
            'session_timeout': 30,
        }
    except:
        return {
            'session_timeout': 30,
        }

def company_profile(request):
    return {'company': None}

def enabled_modules(request):
    from modules.models import Module
    try:
        modules = Module.objects.filter(is_enabled=True).order_by('order')
        return {'enabled_modules': modules}
    except:
        return {'enabled_modules': []}