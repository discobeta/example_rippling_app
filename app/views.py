import json

from django.http import JsonResponse

from app.lib.rippling import RipplingIntegration
from app.models import RipplingCompany, RipplingEmployee


# Create your views here.

def handle_app_install(request):
    rippling = RipplingIntegration()
    oauth_data = rippling.handle_oauth_redirect(request)

    if not oauth_data or oauth_data and 'error' in oauth_data:
        return JsonResponse({
            "current_user": None,
            "oauth_data": None
        })

    # get the current user
    current_user = rippling.get_current_user()

    # update the RipplingCompany data
    company_record = RipplingCompany.objects.get_or_create(
        company_id=current_user['company']
    )[0]
    company_record.access_token = oauth_data['access_token']
    company_record.refresh_token = oauth_data['refresh_token']
    company_record.expires_in = oauth_data['expires_in']
    company_record.scope = oauth_data['scope']
    company_record.save()

    # update the RipplingEmployee data
    user_info = rippling.get_user_info()
    company_employee = RipplingEmployee.objects.get_or_create(
        company=company_record,
        employee_id=user_info['sub']
    )[0]
    company_employee.role_id = user_info['role_id']
    company_employee.picture = user_info['picture']
    company_employee.name = user_info['name']
    company_employee.family_name = user_info['family_name']
    company_employee.given_name = user_info['given_name']
    company_employee.birthdate = user_info['birthdate']
    company_employee.gender = user_info['gender']
    company_employee.email = user_info['email']
    company_employee.email_verified = user_info['email_verified']
    address = json.loads(user_info['address'])
    company_employee.street_address = address['street_address']
    company_employee.locality = address['locality']
    company_employee.region = address['region']
    company_employee.postal_code = address['postal_code']
    company_employee.country = address['country']
    company_employee.phone_number = user_info['phone_number']
    company_employee.phone_number_verified = user_info['phone_number_verified']
    company_employee.save()

    # Refresh the access token
    refresh_token = oauth_data.get('refresh_token')
    if refresh_token:
        refresh_response = rippling.refresh_token(refresh_token)
        # update the company record
        company_record = RipplingCompany.objects.get_or_create(company_id=current_user['company'])[0]
        company_record.access_token = refresh_response.get('access_token')
        company_record.save()

        company_employee.access_token = refresh_response.get('access_token')
        company_employee.save()

        # update the current access token
        rippling.access_token = refresh_response.get('access_token')

    # make the first API call
    current_company = rippling.get_current_company()

    return JsonResponse({
        "current_user": current_user,
        "oauth_data": oauth_data
    })


def handle_oauth_login(request):
    return None


def handle_incoming_webhook(request):
    """
    Handle incoming webhooks from Rippling.
    """

    event_mapping = {
        'employee.created': '_webhook_employee_created',
        'employee.updated': '_webhook_employee_updated',
        'employee.deleted': '_webhook_employee_deleted',
        'company.updated': '_webhook_company_updated',
        'company.deleted': '_webhook_company_deleted',
        'company.created': '_webhook_company_created',
        'group.updated': '_webhook_group_updated',
        'group.created': '_webhook_group_created',
        'group.deleted': '_webhook_group_deleted',
    }

    event_name = request.POST.get('event_name')

    if event_name in event_mapping:
        rippling = RipplingIntegration()
        method = getattr(rippling, event_mapping[event_name])
        method(request.POST)

    return JsonResponse({'success': True})
