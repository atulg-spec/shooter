from django.conf import settings
from .models import SiteSettings

class UpdateJazzminSettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Fetch the latest SiteSettings object
            site_settings = SiteSettings.objects.last()
            if site_settings and site_settings.icon:
                # Use the storage system to get the full URL
                settings.JAZZMIN_SETTINGS["site_logo"] = site_settings.icon.url
        except Exception as e:
            print(f"Error updating Jazzmin settings: {e}")  # For debugging
            pass

        return self.get_response(request)
