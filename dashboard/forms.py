from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(forms.Form):
    username = forms.CharField(label="Username or Email",max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class EmailAccountsForm(forms.ModelForm):
    class Meta:
        model = EmailAccounts
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
        }

class AudienceDataForm(forms.ModelForm):
    class Meta:
        model = AudienceData
        fields = ['email']

class BulkUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Upload CSV File",
        widget=forms.FileInput(attrs={'accept': '.csv'}),
    )


class EmailAccountsBulkUploadForm(forms.Form):
    csv_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Upload'))

class AudienceBulkUploadForm(forms.Form):
    csv_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Upload'))


class SingleMessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['subject', 'content','format_type','attachment','attachment_content']

class EditMessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['subject', 'content', 'format_type', 'attachment_content', 'attachment']


class BulkMessageUploadForm(forms.Form):
    csv_file = forms.FileField()

class TagsForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ['tag_name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        tag = super().save(commit=False)
        if self.user:
            tag.user = self.user
        if commit:
            tag.save()
        return tag

class BulkUploadForm(forms.Form):
    tag = forms.ModelChoiceField(queryset=Tags.objects.none(), label="Select Tag")
    file = forms.FileField(label="Upload CSV File")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['tag'].queryset = Tags.objects.filter(user=self.user)

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['frequency', 'ip_address']
        widgets = {
            'frequency': forms.NumberInput(attrs={'class': 'form-control'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
        }
