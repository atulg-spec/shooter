from django.contrib import admin
from .models import EmailAccounts, AudienceData, Tags, tags_data, Messages, Campaign
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Permission
from django import forms
from django.utils.translation import gettext_lazy as _

# Custom form for the User model
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    # Customize the permissions field
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_("User Permissions"),
    )

# Custom UserAdmin class
class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm

    # Optionally customize the fieldsets to include the permissions field
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

# Unregister the default User admin
admin.site.unregister(User)

# Register the custom User admin
admin.site.register(User, CustomUserAdmin)


@admin.register(EmailAccounts)
class EmailAccountsAdmin(admin.ModelAdmin):
    list_display = ('email', 'user')
    search_fields = ('email',)
    list_filter = ('user',)
    ordering = ('email',)

@admin.register(AudienceData)
class AudienceDataAdmin(admin.ModelAdmin):
    list_display = ('email', 'user')
    search_fields = ('email',)
    list_filter = ('user',)

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'user')
    search_fields = ('tag_name',)
    list_filter = ('user',)

@admin.register(tags_data)
class TagsDataAdmin(admin.ModelAdmin):
    list_display = ('tag', 'data','user')
    search_fields = ('data','user')
    list_filter = ('tag','user')

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user','format_type')
    search_fields = ('subject', 'content','format_type')
    list_filter = ('user','format_type')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'frequency', 'ip_address', 'date_time')
    search_fields = ('ip_address', 'user__username')
    list_filter = ('status', 'date_time')
    ordering = ('-date_time',)

# Inline Configurations
class TagsDataInline(admin.TabularInline):
    model = tags_data
    extra = 1

class TagsAdminWithInline(TagsAdmin):
    inlines = [TagsDataInline]

# Admin overrides for inline demonstration
admin.site.unregister(Tags)
admin.site.register(Tags, TagsAdminWithInline)

admin.site.site_header = "GMAIL SHOOTER 0.8"
admin.site.site_title = "GMAIL SHOOTER 0.8"
admin.site.index_title = "GMAIL SHOOTER 0.8"
