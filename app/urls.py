from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# views
from .views import handle_app_install, handle_oauth_login, handle_incoming_webhook, secure_page

urlpatterns = [
    path('install/', handle_app_install),
    path('sso/', csrf_exempt(handle_oauth_login)),
    path('webhook/', csrf_exempt(handle_incoming_webhook)),
    path('secure-page/', csrf_exempt(secure_page)),
]