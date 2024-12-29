from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.utils.translation import gettext_lazy as _

admin.site.register(Permission)

@admin.register(SoftwarePermissions)
class SoftwarePermissionsAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    list_filter = ('permissions',)
    fieldsets = (
        (None, {
            'fields': ('user', 'permissions')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(EmailAccounts)
class EmailAccountsAdmin(admin.ModelAdmin):
    list_display = ('email', 'user')
    search_fields = ('email',)
    list_filter = ('user',)
    ordering = ('email',)

@admin.register(AudienceData)
class AudienceDataAdmin(admin.ModelAdmin):
    list_display = ('email', 'tag', 'user')
    search_fields = ('email', 'tag')
    list_filter = ('user', 'tag')

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'user')
    search_fields = ('tag_name',)
    list_filter = ('user',)

@admin.register(tags_data)
class TagsDataAdmin(admin.ModelAdmin):
    list_display = ('tag', 'data','user')
    search_fields = ('data',)
    list_filter = ('tag','user')

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user','format_type')
    search_fields = ('subject', 'content','format_type')
    list_filter = ('user','format_type')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'frequency', 'sending_from', 'ip_address', 'date_time')
    search_fields = ('ip_address', 'user__username')
    list_filter = ('status', 'date_time', 'sending_from')
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

@admin.register(SiteSettings)
class SiteIconAdmin(admin.ModelAdmin):
    list_display = ('icon_preview','login_image_preview')

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" alt="{}">',
                obj.icon.url,
                'icon',
            )
        return "No Icon"
    def login_image_preview(self, obj):
        if obj.login_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" alt="{}">',
                obj.login_image.url,
                'Login',
            )
        return "No Login Image"
    icon_preview.short_description = "Login Image"


admin.site.site_header = "GMAIL SHOOTER 8.0"
admin.site.site_title = "GMAIL SHOOTER 8.0"
admin.site.index_title = "GMAIL SHOOTER 8.0"
