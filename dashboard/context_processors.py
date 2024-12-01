from django.utils import timezone
from django.db.models.functions import TruncDay
from django.db.models import Count
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import now, timedelta
from .models import SiteSettings
from dashboard.models import *

def custom_site_context(request):
    settings = SiteSettings.objects.all().first()
    context = {
        'settings':settings,
    }
    return context