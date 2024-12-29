import json
from .models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
import csv
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout

def handlelogout(request):
    logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect('/')

def handlelogin(request):
    if request.user.is_authenticated:
        return redirect('/home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,'Logged In Successfully')
                return redirect('/home?greeting=True')
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = LoginForm()
    return render(request, 'dashboard/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def home(request):
    accounts = EmailAccounts.objects.filter(user=request.user)
    audience = AudienceData.objects.filter(user=request.user)
    total_emails = 0
    total_audience = 0
    if accounts:
        total_emails = accounts.__len__()
    if audience:
        total_audience = audience.__len__()
    context = {
        'accounts':accounts,
        'total_emails':total_emails,
        'total_audience':total_audience,
    }
    return render(request,'dashboard/home.html',context)


@login_required
def email_accounts_list(request):
    accounts = EmailAccounts.objects.filter(user=request.user)
    return render(request, 'dashboard/add-account.html', {'accounts': accounts})

@login_required
def email_account_create(request):
    if request.method == 'POST':
        form = EmailAccountsForm(request.POST)
        if form.is_valid():
            email_account = form.save(commit=False)
            email_account.user = request.user
            email_account.save()
            messages.success(request,f'{email_account.email} added Successfully !')
            return redirect('/email-accounts')
    else:
        form = EmailAccountsForm()
    return render(request, 'dashboard/add-account.html', {'form': form})


@login_required
def email_account_bulk_upload(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        file = request.FILES['csv_file']
        # Validate file extension
        if not file.name.endswith('.csv'):
            messages.error(request, "Only CSV files are allowed.")
            return redirect('/email-accounts')
        try:
            # Read and process CSV file
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            
            # Process each row
            for row in reader:
                # Validate email and password fields
                if not row[0] or not row[1]:
                    messages.error(request, "Each row must have non-empty 'email' and 'password' fields.")
                    return redirect('/email-accounts')
                
                email = row[0]
                password = row[1]
                # Save to the database
                EmailAccounts.objects.create(
                    user=request.user,
                    email=email,
                    password=password
                )
            
            # Success message
            messages.success(request, "Bulk upload completed successfully.")
            return redirect('/email-accounts')
        
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('/email-accounts')
    
    return render(request, 'dashboard/add-account.html')


@login_required
def email_account_delete(request, pk):
    email_account = get_object_or_404(EmailAccounts, pk=pk, user=request.user)
    email_account.delete()
    messages.error(request,f'{email_account.email} deleted Successfully !')
    return redirect('/email-accounts')


@login_required
def email_accounts(request):
    accounts = EmailAccounts.objects.filter(user=request.user)
    context = {
        'accounts':accounts,
    }
    return render(request,'dashboard/email_accounts.html',context)

@login_required
def email_accounts_delete_all(request):
    try:
        EmailAccounts.objects.filter(user=request.user).delete()
        messages.error(request,f'Some error occured {e}')
    except Exception as e:
        messages.error(request,f'All data deleted successfully ! ')
    return redirect('/email-accounts/')



@login_required
def audiences(request):
    audience = AudienceData.objects.filter(user=request.user)
    context = {
        'audience':audience,
    }
    return render(request,'dashboard/audiences.html',context)

@login_required
def audience_data_view(request):
    if request.method == 'POST':
        if 'individual' in request.POST:
            form = AudienceDataForm(request.POST)
            if form.is_valid():
                audience = form.save(commit=False)
                audience.user = request.user  # Set the user
                audience.save()
                messages.success(request, "Audience data added successfully!")
                return redirect('/audiences/')
        elif 'bulk' in request.POST:
            bulk_form = BulkDataUploadForm(request.POST, request.FILES)
            if bulk_form.is_valid():
                csv_file = request.FILES['csv_file']
                tag = bulk_form.cleaned_data.get('tag')  
                try:
                    decoded_file = csv_file.read().decode('utf-8').splitlines()
                    reader = csv.reader(decoded_file)
                    next(reader)  # Skip header row
                    for row in reader:
                        AudienceData.objects.create(
                            user=request.user,
                            tag=tag,
                            email=row[0].strip(),
                        )
                    messages.success(request, "Bulk upload successful!")
                    return redirect('/audiences/')
                except Exception as e:
                    messages.error(request, f"Error processing file: {e}")
            else:
                messages.error(request, "Please upload a valid CSV file.")
                messages.error(request, f"{bulk_form.errors}")

    form = AudienceDataForm()
    bulk_form = BulkMessageUploadForm()
    return render(request, 'dashboard/add-audience.html', {'form': form, 'bulk_form': bulk_form})


@login_required
def audience_delete(request, pk):
    aud = get_object_or_404(AudienceData, pk=pk, user=request.user)
    aud.delete()
    messages.error(request,f'{aud.email} deleted Successfully !')
    return redirect('/audiences/')


@login_required
def audience_delete_all(request):
    try:
        AudienceData.objects.filter(user=request.user).delete()
        messages.error(request,f'Some error occured {e}')
    except Exception as e:
        messages.error(request,f'All data deleted successfully ! ')
    return redirect('/audiences/')

# EMAILS
@login_required
def maillist(request):
    mails = Messages.objects.filter(user=request.user)
    context = {
        'mails':mails,
    }
    return render(request,'dashboard/mails.html',context)

@login_required
def edit_message(request, pk):
    # Get the message object
    message_instance = get_object_or_404(Messages, id=pk, user=request.user)

    # Check permissions for the format_type
    PERMISSION_MAP = {
        'HTML': 'can_use_html',
        'HTML_IMG': 'can_use_html_img',
        'HTML_TO_IMG': 'can_use_html_to_img',
        'PDF': 'can_use_pdf',
        'IMG_TO_PDF': 'can_use_img_to_pdf',
        'HTML_TO_PDF': 'can_use_html_to_pdf',
        'HTML_TO_IMG_TO_PDF': 'can_use_html_to_img_to_pdf',
    }

    permission_key = message_instance.format_type

    if permission_key:
        # Get the SoftwarePermissions object for the current user
        try:
            software_permissions = SoftwarePermissions.objects.get(user=request.user)
        except SoftwarePermissions.DoesNotExist:
            software_permissions = None

        # If no software permissions found or the user doesn't have the required permission
        if not software_permissions or permission_key not in [perm.name for perm in software_permissions.permissions.all()]:
            messages.error(request, f"You do not have permission to edit messages of type {message_instance.format_type}.")
            return redirect('/mails/')  # Redirect to appropriate page if no permission

    if request.method == "POST":
        form = EditMessageForm(request.POST, request.FILES, instance=message_instance)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.clean()  # Run model-level validation
                instance.save()
                messages.success(request, "Message updated successfully!")
                return redirect('/mails/')  # Replace with the appropriate redirect URL
            except ValidationError as e:
                form.add_error(None, e.message)
                for error in e.messages:
                    messages.error(request, error)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = EditMessageForm(instance=message_instance)

    return render(request, 'dashboard/edit-message.html', {
        'form': form,
        'message': message_instance,
    })


@login_required
def upload_messages(request):
    single_form = SingleMessageForm()
    bulk_form = BulkMessageUploadForm()

    if request.method == "POST":
        # Single Upload
        if 'single_upload' in request.POST:
            single_form = SingleMessageForm(request.POST, request.FILES)
            if single_form.is_valid():
                instance = single_form.save(commit=False)

                # Permission check based on format_type
                PERMISSION_MAP = {
                    'HTML': 'can_use_html',
                    'HTML_IMG': 'can_use_html_img',
                    'HTML_TO_IMG': 'can_use_html_to_img',
                    'PDF': 'can_use_pdf',
                    'IMG_TO_PDF': 'can_use_img_to_pdf',
                    'HTML_TO_PDF': 'can_use_html_to_pdf',
                    'HTML_TO_IMG_TO_PDF': 'can_use_html_to_img_to_pdf',
                    'ONLY_IMG': 'Image as Content',
                }
                permission_key = PERMISSION_MAP.get(instance.format_type)

                if permission_key:
                    # Get the SoftwarePermissions object for the current user
                    try:
                        software_permissions = SoftwarePermissions.objects.get(user=request.user)
                    except SoftwarePermissions.DoesNotExist:
                        software_permissions = None


                    # If no software permissions found or the user doesn't have the required permission
                    if not software_permissions or instance.format_type not in [per.name for per in software_permissions.permissions.all()]:
                        messages.error(request, f"You do not have permission to upload messages of type {instance.format_type}.")
                        return redirect('/mails/')  # Redirect if user lacks permission

                try:
                    instance.user = request.user
                    instance.clean()  # Run model-level validation
                    instance.save()
                    messages.success(request, "Message uploaded successfully!")
                    return redirect('/mails/')
                except ValidationError as e:
                    single_form.add_error(None, e.message)
                    for error in e.messages:
                        messages.error(request, error)
            else:
                messages.error(request, single_form.errors)

        # Bulk Upload
        elif 'bulk_upload' in request.POST:
            bulk_form = BulkMessageUploadForm(request.POST, request.FILES)
            if bulk_form.is_valid():
                csv_file = request.FILES['csv_file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.reader(decoded_file)
                messages_to_create = []
                try:
                    software_permissions = SoftwarePermissions.objects.get(user=request.user)
                except SoftwarePermissions.DoesNotExist:
                    software_permissions = None

                for row in reader:
                    if row[2].strip():
                        if not software_permissions or row[2].strip() not in [perm.name for perm in software_permissions.permissions.all()]:
                            messages.error(request, f"You do not have permission to upload messages of type {row[2].strip()}.")
                        else:
                            try:
                                if row[2].strip() in ['HTML','HTML_TO_IMG','HTML_TO_PDF','HTML_TO_IMG_TO_PDF']:
                                    message = Messages(
                                        user=request.user,
                                        subject=row[0].strip(),
                                        content=row[1].strip(),
                                        format_type=row[2].strip(),
                                        attachment_content=row[3].strip(),
                                    )
                                    message.clean()  # Run model-level validation
                                    messages_to_create.append(message)
                                else:
                                    messages.error(request,f'Cannot add {row[2].strip()} message.')
                            except ValidationError as e:
                                messages.error(request, f"Error in row {reader.line_num}: {e.message}")
                if messages_to_create:
                    Messages.objects.bulk_create(messages_to_create, batch_size=10000)
                    messages.success(request, "Bulk upload completed successfully!")
                return redirect('/mails/')

    return render(request, 'dashboard/add-emails.html', {
        'single_form': single_form,
        'bulk_form': bulk_form,
    })


@login_required
def mails_delete(request, pk):
    msg = get_object_or_404(Messages, pk=pk, user=request.user)
    msg.delete()
    messages.error(request,f'Message deleted Successfully !')
    return redirect('/mails/')


@login_required
def mails_delete_all(request):
    try:
        Messages.objects.filter(user=request.user).delete()
        messages.error(request,f'Some error occured {e}')
    except Exception as e:
        messages.error(request,f'All messages deleted successfully ! ')
    return redirect('/mails/')


# TAGS
@login_required
def tags(request):
    tagz = Tags.objects.filter(user=request.user)
    context = {
        'tagz':tagz,
    }
    return render(request,'dashboard/tags.html',context)

@login_required
def add_tag_view(request):
    if request.method == 'POST':
        tag_form = TagsForm(request.POST, user=request.user)
        bulk_upload_form = BulkUploadForm(request.POST, request.FILES, user=request.user)

        # Handle Tag creation
        if 'add_tag' in request.POST:
            if tag_form.is_valid():
                tag_form.save()
                messages.success(request, "Tag added successfully!")
                return redirect('/add-tags/')

        # Handle Bulk Upload
        elif 'bulk_upload' in request.POST:
            if bulk_upload_form.is_valid():
                tag = bulk_upload_form.cleaned_data['tag']
                file = bulk_upload_form.cleaned_data['file']
                try:
                    csv_file = file.read().decode('utf-8').splitlines()
                    reader = csv.reader(csv_file)
                    for row in reader:
                        if row:  # Ensure non-empty rows
                            tags_data.objects.create(user=request.user,tag=tag, data=row[0])
                    messages.success(request, "Data uploaded successfully!")
                except Exception as e:
                    messages.error(request, f"Error during upload: {e}")
                return redirect('/add-tags/')

    else:
        tagz = Tags.objects.filter(user=request.user)
        tag_form = TagsForm(user=request.user)
        bulk_upload_form = BulkUploadForm(user=request.user)

    return render(request, 'dashboard/add-tags.html', {
        'tagz': tagz,
        'tag_form': tag_form,
        'bulk_upload_form': bulk_upload_form,
    })


@login_required
def show_tags_data(request,pk):
    tagz = get_object_or_404(Tags, pk=pk, user=request.user)
    tagz_data = tags_data.objects.filter(tag=tagz)
    context = {
        'tagz':tagz,
        'tagz_data':tagz_data,
    }
    return render(request,'dashboard/tags-data.html',context)

@login_required
def delete_tag(request, pk):
    tg = get_object_or_404(Tags, pk=pk, user=request.user)
    tg.delete()
    messages.error(request,f'Tag deleted Successfully !')
    return redirect('/add-tags/')
# END TAGS

# CAMPAIGNS
@login_required
def campaigns(request):
    if request.method == "POST":
        form = CampaignForm(request.POST, user=request.user)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.user = request.user
            campaign.save()
            return redirect('campaigns')
    else:
        form = CampaignForm(user=request.user)
    
    camps = Campaign.objects.filter(user=request.user)
    context = {
        'camps': camps,
        'form': form,
    }
    return render(request, 'dashboard/campaigns.html', context)

@login_required
def start_campaign(request, pk):
    cp = get_object_or_404(Campaign, pk=pk, user=request.user)
    cp.status = 'processing'
    cp.save()
    messages.success(request,f'Campaign started successfully !')
    return redirect('/campaigns')


# END CAMPAIGNS


# API AND LOGIC
@login_required
def create_campaign(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ip_address = data.get('ip_address')
            frequency = data.get('frequency')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        if not ip_address:
            return JsonResponse({'error': 'IP address is required.'}, status=400)

        user = request.user  # Get the logged-in user
        campaign = Campaign.objects.create(
            user=user,
            ip_address=ip_address,
            frequency=frequency,
            status="created"
        )
        return JsonResponse({'message': 'Campaign created successfully!', 'campaign_id': campaign.id})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def getcampaigns(request,ipaddress):
    campaign = Campaign.objects.filter(ip_address=ipaddress).filter(status='processing')
    if campaign:
        campaign = campaign.first()
        campaign.status = 'success'
        campaign.save()
    else:
        return JsonResponse({'status':False,'data':{}}, safe=False)
    tags = Tags.objects.filter(user=campaign.user)
    custom_tag_data = []
    for tag in tags:
        temp_list = []
        data = tags_data.objects.filter(user=campaign.user).filter(tag=tag)
        for d in data:
            temp_list.append(d.data)
        custom_tag_data.append({tag.tag_name:temp_list})
    emails = [mail.email for mail in AudienceData.objects.filter(user=campaign.user,tag=campaign.audience_data)]
    msgs = Messages.objects.filter(user=campaign.user)
    if not msgs:
        return JsonResponse({'status':False,'data':{'error':'No Message Added'}}, safe=False)
    messages = []
    for mail in msgs: 
        rendered_message = render_to_string('template.html', {'message': mail.content})
        temp = {
            'subject': mail.subject,
            'mail': rendered_message,
            'format_type': mail.format_type,
            'attachment_content': mail.attachment_content,
            'file_name': mail.file_name,
            'attachment': mail.attachment.url if mail.attachment else None
        }
        messages.append(temp)
    accounts = []
    accountsObjects = EmailAccounts.objects.filter(user=campaign.user)
    if not accountsObjects:
        return JsonResponse({'status':False,'data':{'error':'No Email Accounts Added'}}, safe=False)
    for acc in accountsObjects:
        accounts.append({'email':acc.email,'password':acc.password})
    campaign_data = {
            'id': campaign.id,
            'send_from': campaign.sending_from,
            'custom_tags': custom_tag_data,
            'frequency': campaign.frequency,
            'accounts': accounts,
            'emails': emails,
            'messages': messages,
        }
    # Return JSON response
    return JsonResponse({'status':True,'data':campaign_data}, safe=False)

def getRandomTagValue(request, id, tagName):
    try:
        campaign = Campaign.objects.filter(pk=id).first()
        if not campaign:
            return JsonResponse({'status': False, 'error': 'Campaign not found'}, status=404)
        user = campaign.user
        tag = Tags.objects.filter(user=user, tag_name=tagName).first()
        if not tag:
            return JsonResponse({'status': False, 'error': 'Tag not found'}, status=404)
        random_tag_data = tags_data.objects.filter(user=user, tag=tag).order_by('?').first()
        if not random_tag_data:
            return JsonResponse({'status': False, 'error': 'No data found for the tag'}, status=404)
        return JsonResponse({'status': True, 'data': {'random': random_tag_data.data}}, safe=False)
    except Exception as e:
        return JsonResponse({'status': False, 'error': 'An unexpected error occurred: ' + str(e)}, status=500)
