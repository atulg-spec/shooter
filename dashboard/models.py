from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

status_choices = [
        ('success', 'success'),
        ('created', 'created'),
    ]

class EmailAccounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Email Account"
        verbose_name_plural = "Email Accounts"

class AudienceData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Audience Data"
        verbose_name_plural = "Audiences"

class Tags(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=50, default="")

    def save(self, *args, **kwargs):
        # Prepend '{custom_}' to tag_name if not already added
        if not self.tag_name.startswith("{custom_}"):
            self.tag_name = f"{{custom_{self.tag_name}}}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = "Custom tag"
        verbose_name_plural = "Custom tags"

class tags_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    data = models.CharField(max_length=500, default="")

    def __str__(self):
        return f'{self.tag.tag_name}-{self.data}'

    class Meta:
        verbose_name = "Custom tag data"
        verbose_name_plural = "Custom tags Data"


class Messages(models.Model):
    FORMAT_CHOICES = [
        ('HTML', 'HTML Message Only'),
        ('HTML_IMG', 'HTML with Image Attachment'),
        ('HTML_TO_IMG', 'HTML to Image Conversion'),
        ('PDF', 'PDF Attachment'),
        ('IMG_TO_PDF', 'Image to PDF Conversion'),
        ('HTML_TO_IMG_TO_PDF', 'HTML to Image to PDF'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150, default='')
    content = models.TextField(default='')
    format_type = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='HTML')
    attachment_content = models.TextField(default='', blank=True, null=True)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)  # To handle file attachments like images or PDFs

    def clean(self):
        # Validation for format_type
        if self.format_type == 'HTML' and (not self.subject or not self.content):
            raise ValidationError("Subject and content are required for HTML format.")

        if self.format_type == 'HTML_IMG' and (not self.content or not self.attachment):
            raise ValidationError("HTML content and an image attachment are required for HTML_IMG format.")
        
        if self.format_type == 'HTML_IMG' and self.attachment and not self.attachment.name.lower().endswith(('png', 'jpg', 'jpeg')):
            raise ValidationError("Attachment must be an image file for HTML_IMG format.")
        
        if self.format_type == 'PDF' and not self.attachment:
            raise ValidationError("A PDF attachment is required for PDF format.")
        
        if self.format_type == 'PDF' and self.attachment and not self.attachment.name.lower().endswith('pdf'):
            raise ValidationError("Attachment must be a PDF file for PDF format.")
        
        if self.format_type == 'IMG_TO_PDF' and self.attachment and not self.attachment.name.lower().endswith(('png', 'jpg', 'jpeg')):
            raise ValidationError("Attachment must be an image file for IMG_TO_PDF format.")

        if self.format_type == 'HTML_TO_IMG_TO_PDF' and (not self.content or not self.attachment):
            raise ValidationError("HTML content and an image attachment are required for HTML_TO_IMG_TO_PDF format.")

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