# Generated by Django 5.0.1 on 2024-01-11 21:27

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RipplingCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('deleted', models.BooleanField(default=False)),
                ('company_id', models.CharField(default=None, help_text='The id of the company.', max_length=255)),
                ('company_name', models.CharField(default=None, help_text='The name of the company.', max_length=255, null=True)),
                ('access_token', models.CharField(default=None, help_text='The access token for the company.', max_length=255, null=True)),
                ('refresh_token', models.CharField(default=None, help_text='The refresh token for the company.', max_length=255, null=True)),
                ('expires_in', models.CharField(default=None, help_text='The expiration for the access token.', max_length=255, null=True)),
                ('scope', models.CharField(default=None, help_text='The scope for the access token.', max_length=10000, null=True)),
                ('primary_email', models.CharField(default=None, help_text='The primary email for the company.', max_length=255, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RipplingEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('deleted', models.BooleanField(default=False)),
                ('employee_id', models.CharField(default=None, help_text='The id of the employee.', max_length=255)),
                ('role_id', models.CharField(default=None, help_text='The id of the role.', max_length=255, null=True)),
                ('picture', models.CharField(default=None, help_text='The picture of the employee.', max_length=255, null=True)),
                ('name', models.CharField(default=None, help_text='The name of the employee.', max_length=255, null=True)),
                ('family_name', models.CharField(default=None, help_text='The family name of the employee.', max_length=255, null=True)),
                ('given_name', models.CharField(default=None, help_text='The given name of the employee.', max_length=255, null=True)),
                ('birthdate', models.DateField(default=None, help_text='The birthdate of the employee.', null=True)),
                ('gender', models.CharField(default=None, help_text='The given name of the employee.', max_length=255, null=True)),
                ('email', models.CharField(default=None, help_text='The email of the employee.', max_length=255, null=True)),
                ('email_verified', models.BooleanField(default=False, help_text='The email_verified of the employee.')),
                ('street_address', models.CharField(default=None, help_text='The address of the employee.', max_length=255, null=True)),
                ('locality', models.CharField(default=None, help_text='The locality of the employee.', max_length=255, null=True)),
                ('region', models.CharField(default=None, help_text='The region of the employee.', max_length=255, null=True)),
                ('postal_code', models.CharField(default=None, help_text='The postal_code of the employee.', max_length=255, null=True)),
                ('country', models.CharField(default=None, help_text='The country of the employee.', max_length=255, null=True)),
                ('phone_number', models.CharField(default=None, help_text='The phone_number of the employee.', max_length=255, null=True)),
                ('phone_number_verified', models.BooleanField(default=False, help_text='The phone_number_verified of the employee.')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rippling_company_employees', to='app.ripplingcompany')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RipplingGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('deleted', models.BooleanField(default=False)),
                ('group_id', models.CharField(default=None, help_text='The id of the group.', max_length=255)),
                ('name', models.CharField(default=None, help_text='The name of the group.', max_length=255, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rippling_user_groups', to='app.ripplingcompany')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]