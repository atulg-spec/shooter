# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.handlelogin, name='login'),
    path('logout/', views.handlelogout, name='logout'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    # EMAIL ACCOUNTS
    path('email-accounts/', views.email_accounts, name='email-accounts'),
    path('add-account/', views.email_account_create, name='add-account'),
    path('add-account-bulk/', views.email_account_bulk_upload, name='email_account_bulk_upload'),
    path('email-account/<int:pk>/delete/', views.email_account_delete, name='email_account_delete'),
    path('email-accounts/delete-all/', views.email_accounts_delete_all, name='email_accounts_delete_all'),
    # END EMAIL ACCOUNTS
    # Audiences
    path('audiences/', views.audiences, name='audiences'),
    path('add-audience/', views.audience_data_view, name='add-audience'),
    path('audience/<int:pk>/delete/', views.audience_delete, name='audience_delete'),
    path('audience/delete-all/', views.audience_delete_all, name='audience_delete_all'),
    # END Audiences
    # mails
    path('mails/', views.maillist, name='maillist'),
    path('add-mails/', views.upload_messages, name='add-mails'),
    path('mails/<int:pk>/edit/', views.edit_message, name='edit_message'),
    path('mails/<int:pk>/delete/', views.mails_delete, name='delete_mail'),
    path('mails/delete-all/', views.mails_delete_all, name='mails_delete_all'),
    # end mails
    # tags
    path('tags/', views.tags, name='tags'),
    path('add-tags/', views.add_tag_view, name='add-tags'),
    path('tags/<int:pk>/show-data/', views.show_tags_data, name='show_tags_data'),
    path('tags/<int:pk>/delete/', views.delete_tag, name='delete_tag'),
    # end tags
    # campaigns
    path('campaigns/', views.campaigns, name='campaigns'),
    # end campaigns

    path('create-campaign/', views.create_campaign, name='create_campaign'),
    path("getcampaigns/<str:ipaddress>",views.getcampaigns,name='getcampaigns'),
    path('getRandomTagValue/<int:id>/<str:tagName>', views.getRandomTagValue, name='getRandomTagValue'),
]
