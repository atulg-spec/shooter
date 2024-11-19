from django.contrib import admin
from django.urls import path,include, re_path
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('adminpanel/', admin.site.urls),
    path('', include('dashboard.urls')),
    # path('dashboard/', lambda request: redirect('/')),
    # path('login/', CustomLoginView.as_view(), name='custom_admin_login'),
    # path('', custom_admin_site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

