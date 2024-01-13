import datetime
from django.contrib.auth import get_user_model
from django.db import models


class BaseModel(models.Model):

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(
        editable=False, default=datetime.datetime.now)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    class Meta:
        abstract = True

    def to_dict(self):
        fields = self._meta.get_fields()
        data = {}
        for field in fields:
            field_type = field.get_internal_type()
            try:
                if field_type == 'ForeignKey':
                    data[field.name] = getattr(self, field.name).id
                elif field_type == 'ManyToManyField':
                    data[field.name] = [obj.id for obj in getattr(self, field.name).all()]
                elif field_type == 'DateTimeField':
                    data[field.name] = getattr(self, field.name).isoformat()
                else:
                    data[field.name] = getattr(self, field.name)
            except:
                data[field.name] = None
        return data

class RipplingCompany(BaseModel):

    company_id = models.CharField(max_length=255, default=None, null=False, help_text="The id of the company.")
    company_name = models.CharField(max_length=255, default=None, null=True, help_text="The name of the company.")
    access_token = models.CharField(max_length=255, default=None, null=True, help_text="The access token for the company.")
    refresh_token = models.CharField(max_length=255, default=None, null=True, help_text="The refresh token for the company.")
    expires_in = models.CharField(max_length=255, default=None, null=True, help_text="The expiration for the access token.")
    scope = models.CharField(max_length=10000, default=None, null=True, help_text="The scope for the access token.")

    primary_email = models.CharField(max_length=255, default=None, null=True, help_text="The primary email for the company.")
    def __str__(self):
        return str(self.company_name)

    def is_access_token_valid(self):
        # time data '129600' does not match format '%Y-%m-%d %H:%M:%S.%f'
        if not self.expires_in:
            return False
        iso_format = datetime.datetime.fromtimestamp(int(self.expires_in)).isoformat()
        return datetime.datetime.now() > datetime.datetime.strptime(iso_format, '%Y-%m-%dT%H:%M:%S')


class RipplingEmployee(BaseModel):

    company = models.ForeignKey('app.RipplingCompany', on_delete=models.CASCADE, related_name='rippling_company_employees')

    employee_id = models.CharField(max_length=255, default=None, null=False, help_text="The id of the employee.")
    role_id = models.CharField(max_length=255, default=None, null=True, help_text="The id of the role.")

    picture = models.CharField(max_length=255, default=None, null=True, help_text="The picture of the employee.")
    name = models.CharField(max_length=255, default=None, null=True, help_text="The name of the employee.")
    family_name = models.CharField(max_length=255, default=None, null=True, help_text="The family name of the employee.")
    given_name = models.CharField(max_length=255, default=None, null=True, help_text="The given name of the employee.")
    birthdate = models.DateField(default=None, null=True, help_text="The birthdate of the employee.")
    gender = models.CharField(max_length=255, default=None, null=True, help_text="The given name of the employee.")
    email = models.CharField(max_length=255, default=None, null=True, help_text="The email of the employee.")
    email_verified = models.BooleanField(default=False, help_text="The email_verified of the employee.")
    street_address = models.CharField(max_length=255, default=None, null=True, help_text="The address of the employee.")
    locality = models.CharField(max_length=255, default=None, null=True, help_text="The locality of the employee.")
    region = models.CharField(max_length=255, default=None, null=True, help_text="The region of the employee.")
    postal_code = models.CharField(max_length=255, default=None, null=True, help_text="The postal_code of the employee.")
    country = models.CharField(max_length=255, default=None, null=True, help_text="The country of the employee.")
    phone_number = models.CharField(max_length=255, default=None, null=True, help_text="The phone_number of the employee.")
    phone_number_verified = models.BooleanField(default=False, help_text="The phone_number_verified of the employee.")

    def __str__(self):
        return str(self.name)


class RipplingGroup(BaseModel):

    company = models.ForeignKey('app.RipplingCompany', on_delete=models.CASCADE, related_name='rippling_user_groups')
    group_id = models.CharField(max_length=255, default=None, null=False, help_text="The id of the group.")
    name = models.CharField(max_length=255, default=None, null=True, help_text="The name of the group.")
    users = models.JSONField(default=list, null=True, help_text="The users of the group.")

    def __str__(self):
        return str(self.name)