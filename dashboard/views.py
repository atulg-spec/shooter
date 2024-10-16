import json
from .models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *

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
    campaign = Campaign.objects.filter(ip_address=ipaddress).filter(status='created')
    if campaign:
        campaign = campaign.first()
        campaign.status = 'success'
        campaign.save()
    else:
        return JsonResponse({'status':False,'data':{}}, safe=False)
    print(campaign.user)
    for x in AudienceData.objects.all():
        print(x.user)
    emails = [mail.email for mail in AudienceData.objects.filter(user=campaign.user)]
    msg = Messages.objects.filter(user=campaign.user).first()
    if not msg:
        return JsonResponse({'status':False,'data':{'error':'No Message Added'}}, safe=False)
    rendered_message = render_to_string('template.html', {'message': msg.content})
    accounts = []
    accountsObjects = EmailAccounts.objects.filter(user=campaign.user)
    if not accountsObjects:
        return JsonResponse({'status':False,'data':{'error':'No Email Accounts Added'}}, safe=False)
    for acc in accountsObjects:
        accounts.append({'email':acc.email,'password':acc.password})
    campaign_data = {
            'id': campaign.id,
            'frequency': campaign.frequency,
            'accounts': accounts,
            'emails': emails,
            'subject': msg.subject,
            'message': rendered_message,
        }
    # Return JSON response
    return JsonResponse({'status':True,'data':campaign_data}, safe=False)