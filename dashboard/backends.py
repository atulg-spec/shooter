from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.sessions.models import Session
from django.utils.timezone import now

User = get_user_model()

class SingleSessionBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user:
            # If user is already authenticated, log out from all other sessions
            self.logout_previous_sessions(user)
        return user

    def logout_previous_sessions(self, user):
        sessions = Session.objects.filter(expire_date__gte=now())
        for session in sessions:
            data = session.get_decoded()
            if data.get('_auth_user_id') == str(user.id):
                session.delete()
