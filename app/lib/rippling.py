import logging
from base64 import b64encode

import requests
from django.conf import settings

from app.models import RipplingCompany, RipplingEmployee, RipplingGroup

logger = logging.getLogger(__name__)


class RipplingIntegration:
    access_token = None

    def __init__(self):
        self.client_id = settings.RIPPLING_CLIENT_ID
        self.client_secret = settings.RIPPLING_CLIENT_SECRET
        self.redirect_uri = settings.RIPPLING_REDIRECT_URI
        self.base_url = settings.RIPPLING_BASE_URL

    def _get_request_headers(self):
        headers = {
            'Accept': 'application/json'
        }
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        return headers

    def _execute_request(self, method, url, headers=None, data=None):

        if not headers:
            headers = self._get_request_headers()

        try:
            response = requests.request(method, url, headers=headers, data=data)
            return response.json()
        except Exception as e:
            logger.error(f'Error executing request')
            return None

    def get_employee(self, employee_id):
        url = f'{self.base_url}/platform/api/employees/{employee_id}'
        return self._execute_request('GET', url)

    def get_employees(self):
        url = f'{self.base_url}/platform/api/employees'
        return self._execute_request('GET', url)

    def get_current_user(self):
        url = f'{self.base_url}/platform/api/me'
        return self._execute_request('GET', url)

    def get_saml_metadata(self):
        url = f'{self.base_url}/platform/api/saml/metadata'
        return self._execute_request('GET', url)

    def get_current_company(self):
        url = f'{self.base_url}/platform/api/companies/current'
        return self._execute_request('GET', url)

    def refresh_token(self, refresh_token):
        url = f'{self.base_url}/api/o/token/'
        headers = {
            'Authorization': f'Basic {b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()}'
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        return self._execute_request('POST', url, headers=headers, data=data)

    def handle_oauth_redirect(self, request):
        code = request.GET.get('code')
        if code:
            headers = {
                'Authorization': f'Basic {b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()}'
            }
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri
            }
            url = f'{self.base_url}/api/o/token/'
            response = self._execute_request('POST', url, headers=headers, data=data)
            self.access_token = response.get('access_token')
            return response

    def get_user_info(self):
        """
        curl --location --request GET 'https://api.rippling.com/platform/api/userinfo' \
        --header 'Authorization: Bearer REDACTED'
        """
        url = f'{self.base_url}/platform/api/userinfo'
        return self._execute_request('GET', url)

    @staticmethod
    def _webhook_company_updated(data):
        """
        Handle incoming event about a company being updated.
        """
        id = data.get('id')
        company_id = data.get('company_id')
        company_primary_email = data.get('company_primary_email')

        if id and company_id and company_primary_email:
            company = RipplingCompany.objects.get_or_create(company_id=company_id)[0]
            if not company.primary_email == company_primary_email:
                company.primary_email = company_primary_email
                company.save()

    @staticmethod
    def _webhook_company_deleted(data):
        """
        Handle incoming event about a company being deleted.
        """
        id = data.get('id')
        company_id = data.get('company_id')
        company_primary_email = data.get('company_primary_email')

        if id and company_id and company_primary_email:
            company = RipplingCompany.objects.get_or_create(company_id=company_id)[0]
            if not company.primary_email == company_primary_email:
                company.primary_email = company_primary_email
                company.save()

            company.deleted = True
            company.save()

    @staticmethod
    def _webhook_company_created(data):
        """
        Handle incoming event about a company being created.
        """
        id = data.get('id')
        company_id = data.get('company_id')
        company_primary_email = data.get('company_primary_email')

        if id and company_id and company_primary_email:
            company = RipplingCompany.objects.get_or_create(company_id=company_id)[0]
            if not company.primary_email == company_primary_email:
                company.primary_email = company_primary_email
                company.save()

    @staticmethod
    def _webhook_employee_created(data):
        """
        Handle incoming event about an employee being created.
        """
        id = data.get('id')
        company_id = data.get('company_id')
        company_primary_email = data.get('company_primary_email')

        if id and company_id and company_primary_email:

            company = RipplingCompany.objects.get_or_create(company_id=company_id)[0]
            if not company.primary_email == company_primary_email:
                company.primary_email = company_primary_email
                company.save()

            employee = RipplingEmployee.objects.get_or_create(
                company=company,
                employee_id=id
            )[0]

    @staticmethod
    def _webhook_employee_deleted(data):
        """
        Handle incoming event about an employee being deleted.
        """
        id = data.get('id')
        company_id = data.get('company_id')
        company_primary_email = data.get('company_primary_email')

        if id and company_id and company_primary_email:
            company = RipplingCompany.objects.get_or_create(company_id=company_id)[0]
            if not company.primary_email == company_primary_email:
                company.primary_email = company_primary_email
                company.save()

            employee = RipplingEmployee.objects.get_or_create(
                company=company,
                employee_id=id
            )[0]
            employee.deleted = True
            employee.save()

    @staticmethod
    def _webhook_employee_updated(data):
        """
        Handle incoming event about an employee being updated.
        """
        id = data.get('id')
        company_id = data.get('company_id')
        company_primary_email = data.get('company_primary_email')

        if id and company_id and company_primary_email:
            company = RipplingCompany.objects.get_or_create(company_id=company_id)[0]
            if not company.primary_email == company_primary_email:
                company.primary_email = company_primary_email
                company.save()

            employee = RipplingEmployee.objects.get_or_create(
                company=company,
                employee_id=id
            )[0]

    @staticmethod
    def _webhook_group_updated(data):
        """
        Handle incoming event about a group being updated.
        """
        id = data.get('id')
        company_id = data.get('company_id')
        company_primary_email = data.get('company_primary_email')

        if id and company_id and company_primary_email:
            company = RipplingCompany.objects.get_or_create(company_id=company_id)[0]
            if not company.primary_email == company_primary_email:
                company.primary_email = company_primary_email
                company.save()

            group = RipplingGroup.objects.get_or_create(
                company=company,
                group_id=id
            )[0]

    @staticmethod
    def _webhook_group_created(data):
        """
        Handle incoming event about a group being created.
        """
        id = data.get('id')
        company_id = data.get('company_id')
        company_primary_email = data.get('company_primary_email')

        if id and company_id and company_primary_email:
            company = RipplingCompany.objects.get_or_create(company_id=company_id)[0]
            if not company.primary_email == company_primary_email:
                company.primary_email = company_primary_email
                company.save()

            group = RipplingGroup.objects.get_or_create(
                company=company,
                group_id=id
            )[0]

    @staticmethod
    def _webhook_group_deleted(data):
        """
        Handle incoming event about a group being deleted.
        """
        id = data.get('id')
        company_id = data.get('company_id')
        company_primary_email = data.get('company_primary_email')

        if id and company_id and company_primary_email:
            company = RipplingCompany.objects.get_or_create(company_id=company_id)[0]
            if not company.primary_email == company_primary_email:
                company.primary_email = company_primary_email
                company.save()

            group = RipplingGroup.objects.get_or_create(
                company=company,
                group_id=id
            )[0]
            group.deleted = True
            group.save()
