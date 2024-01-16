import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect

from app.lib.rippling import RipplingIntegration
from app.models import RipplingCompany, RipplingEmployee


# Create your views here.

def handle_app_install(request):
    rippling = RipplingIntegration()
    oauth_data = rippling.handle_oauth_redirect(request)

    if not oauth_data or oauth_data and 'error' in oauth_data:
        return JsonResponse({
            "current_user": None,
            "oauth_data": oauth_data
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

    # update the RipplingCompany data
    company_record.company_name = current_company['name']
    company_record.primary_email = current_company['primaryEmail']
    company_record.save()

    return HttpResponseRedirect(f'https://app.rippling.com/apps/{settings.RIPPLING_APP_SLUG}/settings')


def handle_oauth_login(request):
    rippling = RipplingIntegration()

    code = request.POST.get('code')
    role_id = request.POST.get('roleId')
    company_id = request.POST.get('companyId')

    if not code:
        return JsonResponse({'error': 'No code provided.'})

    oauth_data = rippling.handle_oauth_redirect(request, code)
    current_user = rippling.get_current_user()

    # try to find the employee record
    employee_record = None
    try:
        employee_record = RipplingEmployee.objects.get(employee_id=current_user.get('id'))
    except:
        # find the commpany record
        company_record = None
        try:
            company_record = RipplingCompany.objects.get(company_id=current_user.get('company'))
        except:
            return JsonResponse({'error': 'Company not found.'})
        # creaet the employee record
        employee_record = RipplingEmployee.objects.create(
            company=company_record,
            employee_id=current_user.get('id'),
            role_id=role_id
        )

    # get the userinfo
    user_info = rippling.get_employee(employee_record.employee_id)
    current_user = rippling.get_current_user()
    employee_record.given_name = user_info.get('firstName')
    employee_record.family_name = user_info.get('lastName')
    employee_record.email = current_user.get('workEmail')
    employee_record.updated_at = user_info.get('updatedAt')
    employee_record.created_at = user_info.get('createdAt')
    employee_record.save(update_fields=['given_name', 'family_name', 'email', 'updated_at', 'created_at'])

    # if the employee record doesn't have a user, create one
    if not employee_record.user:
        try:
            user = get_user_model().objects.get(username=f"{employee_record.employee_id}:{employee_record.company.company_id}")
            employee_record.user = user
            employee_record.save()
        except:
            # create the user
            user = get_user_model().objects.create_user(
                username=f"{employee_record.employee_id}:{employee_record.company.company_id}",
                email=employee_record.email,
                first_name=employee_record.given_name,
                last_name=employee_record.family_name,
            )
            employee_record.user = user
            employee_record.save()

    login(request, employee_record.user)
    return HttpResponseRedirect('/integration/secure-page/')


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


@login_required
def secure_page(request):
    """
    A secure page that requires a logged in user.
    """
    return JsonResponse({'success': True, 'user': request.user.id})
