from django.contrib import admin

from login.models import MagicLinkToken

admin.site.register(MagicLinkToken)
