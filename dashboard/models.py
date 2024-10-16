from django.db import models
from django.contrib.auth.models import User

status_choices = [
        ('success', 'success'),
        ('created', 'created'),
    ]

class EmailAccounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    email = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Email Account"
        verbose_name_plural = "Email Accounts"

class AudienceData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    email = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Audience Data"
        verbose_name_plural = "Audiences"

class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    subject = models.CharField(max_length=150, default='')
    content = models.TextField(default='')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(choices=status_choices, max_length=12, default="created")
    frequency = models.PositiveIntegerField(default=10)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username.upper()} started a Campaign at Machine IP Address: {self.ip_address} at {self.date_time}.'

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"