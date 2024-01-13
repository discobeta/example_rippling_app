# Rippling Integration Example

### Create a new directory for the project
`mkdir example_rippling_app`

`cd example_rippling_app `
### Create a new virtual environment
`python -m venv venv`

`source venv/bin/activate`
### Install Django and Requests
`pip install django`

`pip install requests`

`pip freeze|grep Django > requirments.txt`

`pip freeze|grep requests >> requirments.txt`
### Create an .env file to contain the secrets
`touch .env`
### Create a new Django project
`django-admin startproject project`

`mv project example_rippling_app`

`cd example_rippling_app`
### Create a new Django app
`./manage.py startapp app`

`touch app/urls.py`

`touch app/lib/__init__.py`

`mkdir app/lib`

`touch app/lib/rippling.py`

### Create a Rippling integration class
File `app/lib/rippling.py`
```python```

### Create a Django model to store Rippling data
File `app/models.py`
```python```

### Create a Django admin to manage Rippling data
File `app/admin.py`
```python```

### Create a Django view to handle Rippling OAuth redirect, SSO and the webhooks
File `app/views.py`
```python```

### Create a Django urls entry point for the Rippling integration
File `app/urls.py`
```python
from django.urls import path
from .views import handle_app_install, handle_oauth_login, handle_incoming_webhook, secure_page
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('install/', handle_app_install),
    path('sso/', csrf_exempt(handle_oauth_login)),
    path('webhook/', csrf_exempt(handle_incoming_webhook)),
    path('secure-page/', secure_page),
]
```

### Add the newly created app to INSTALLED_APPS in the project/settings.py file
File `project/settings.py`
```python
INSTALLED_APPS = [
    'app',
    ...
]
```

### Add your public hostname to ALLOWED_HOSTS in the project/settings.py file
File `project/settings.py`
```python
ALLOWED_HOSTS = [
    'xxx.ngrok-free.app',
    ...
]
```

### Add the newly created app to the project/urls.py file
```python
path('integration/', include('app.urls')),
```

### Add the Rippling Client-ID, Client-Secret and Redirect-URI to the project/settings.py file
File `project/settings.py`
```python
RIPPLING_CLIENT_ID = os.environ.get('RIPPLING_CLIENT_ID', 'xxx')
RIPPLING_CLIENT_SECRET = os.environ.get('RIPPLING_CLIENT_SECRET', 'xxx')
RIPPLING_REDIRECT_URI = os.environ.get('RIPPLING_REDIRECT_URI', 'https://xxx.ngrok-free.app/integration/install/')
RIPPLING_BASE_URL = os.environ.get('RIPPLING_BASE_URL', 'https://api.rippling.com')
RIPPLING_APP_SLUG = os.environ.get('RIPPLING_APP_SLUG', 'your-app-slug')
```

### Add the Rippling Client-ID and Client-Secret to the .env file
File `.env`
```shell
export RIPPLING_CLIENT_ID=xxx
export RIPPLING_CLIENT_SECRET=xxx
```
