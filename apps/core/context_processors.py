def gmt_settings(request):
    try:
        settings = GMTSettings.get_settings()
        return {
            'session_timeout': settings.session_timeout,
        }
    except:
        return {
            'session_timeout': 30,
        }

def company_profile(request):
    from .models import CompanyProfile
    try:
        profile = CompanyProfile.get_profile()
        return {'company': profile}
    except:
        return {'company': None}

def enabled_modules(request):
    from modules.models import Module
    try:
        modules = Module.objects.filter(is_enabled=True).order_by('order')
        return {'enabled_modules': modules}
    except:
        return {'enabled_modules': []}