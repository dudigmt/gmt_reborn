from .models import GMTSettings

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