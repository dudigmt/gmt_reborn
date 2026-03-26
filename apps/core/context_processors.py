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