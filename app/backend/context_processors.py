from .models import Settings

def site_settings(request):
    return {
        'settings': Settings.objects.first()
    }