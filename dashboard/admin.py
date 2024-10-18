from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth import login
from django.contrib import messages  # Import messages for notifications
from django.contrib.auth.views import LoginView
from django.urls import path
from django.shortcuts import redirect
from django.template.response import TemplateResponse
import csv
from .forms import EmailAccountsBulkUploadForm, AudienceBulkUploadForm
from django.conf import settings

# Custom login view
class CustomLoginView(LoginView):
    template_name = 'admin/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(settings.LOGIN_REDIRECT_URL or '/')


# Custom admin site to allow all authenticated users to access admin
class CustomAdminSite(admin.AdminSite):
    def has_permission(self, request):
        return request.user.is_authenticated  # Allow any authenticated user to access

    def has_module_permission(self, request):
        return request.user.is_authenticated  # Allow any authenticated user to see the modules

custom_admin_site = CustomAdminSite(name='custom_admin')


class EmailAccountsAdmin(admin.ModelAdmin):
    list_display = ('email', 'password',)
    search_fields = ('email',)
    
    # Adding the bulk upload functionality
    change_list_template = "admin/email_accounts_changelist.html"  # Custom template

    def get_queryset(self, request):
        """Filter the queryset to show only the audience data for the current user unless they are superuser or staff."""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs  # Superusers and staff can see all data
        return qs.filter(user=request.user)  # Regular users only see their data

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user  # Set the current logged-in user
        super().save_model(request, obj, form, change)

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated

    def has_add_permission(self, request):
        return request.user.is_authenticated

    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated

    def has_delete_permission(self, request, obj=None):
        return True

    # Custom view for bulk upload
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.bulk_upload, name='email_accounts_bulk_upload'),
        ]
        return custom_urls + urls

    def bulk_upload(self, request):
        if request.method == "POST":
            form = EmailAccountsBulkUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data["csv_file"]
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.reader(decoded_file)

                # Loop through each row in the CSV
                for row in reader:
                    if len(row) >= 2:
                        email = row[0].strip()  # Extract the email
                        password = row[1].strip()  # Extract the password
                        if email == '' or password == '':
                            messages.error(request, f"Skipping invalid row: {row}")
                        else:
                            EmailAccounts.objects.create(
                                user=request.user,  # Set the current logged-in user as owner
                                email=email,
                                password=password,
                            )
                    else:
                        messages.error(request, f"Skipping invalid row: {row}")
                messages.success(request, "Email accounts uploaded successfully.")
                return redirect("/dashboard/emailaccounts/")
        form = EmailAccountsBulkUploadForm()
        context = {
            'form': form,
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
        }
        return TemplateResponse(request, "admin/email_accounts_bulk_upload.html", context)

custom_admin_site.register(EmailAccounts, EmailAccountsAdmin)
admin.site.register(EmailAccounts, EmailAccountsAdmin)

class AudienceAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)
    
    # Adding the bulk upload functionality
    change_list_template = "admin/audience_changelist.html"  # Custom template

    def get_queryset(self, request):
        """Filter the queryset to show only the audience data for the current user unless they are superuser or staff."""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs  # Superusers and staff can see all data
        return qs.filter(user=request.user)  # Regular users only see their data

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user  # Set the current logged-in user
        super().save_model(request, obj, form, change)

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated

    def has_add_permission(self, request):
        return request.user.is_authenticated

    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated

    def has_delete_permission(self, request, obj=None):
        return True

    # Custom view for bulk upload
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('audience-bulk-upload/', self.bulk_upload, name='audience_bulk_upload'),
        ]
        return custom_urls + urls

    def bulk_upload(self, request):
        if request.method == "POST":
            form = AudienceBulkUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data["csv_file"]
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.reader(decoded_file)

                # Loop through each row in the CSV
                for row in reader:
                    if len(row) >= 2:
                        email = row[0].strip()  # Extract the email
                        if email == '':
                            messages.error(request, f"Skipping invalid row: {row}")
                        else:
                            AudienceData.objects.create(
                                user=request.user,  # Set the current logged-in user as owner
                                email=email,
                            )
                    else:
                        messages.error(request, f"Skipping invalid row: {row}")
                messages.success(request, "Audience data uploaded successfully.")
                return redirect("/dashboard/audiencedata/")

        form = AudienceBulkUploadForm()
        context = {
            'form': form,
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
        }
        return TemplateResponse(request, "admin/audience_bulk_upload.html", context)

custom_admin_site.register(AudienceData, AudienceAdmin)
admin.site.register(AudienceData, AudienceAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    
    # Adding the bulk upload functionality
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user  # Set the current logged-in user
        super().save_model(request, obj, form, change)

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated

    def has_add_permission(self, request):
        return request.user.is_authenticated

    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated

    def has_delete_permission(self, request, obj=None):
        return True

custom_admin_site.register(Messages, MessageAdmin)
admin.site.register(Messages, MessageAdmin)


class CampaignAdmin(admin.ModelAdmin):
    list_filter = ('user', 'status', 'ip_address','date_time')
    readonly_fields = ('user', 'frequency', 'status', 'ip_address','date_time')

    def get_queryset(self, request):
        """Filter the queryset to show only the audience data for the current user unless they are superuser or staff."""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs  # Superusers and staff can see all data
        return qs.filter(user=request.user)  # Regular users only see their data

admin.site.register(Campaign, CampaignAdmin)

admin.site.site_header = "GMAIL SHOOTER"
admin.site.site_title = "GMAIL SHOOTER"
admin.site.index_title = "GMAIL SHOOTER"
