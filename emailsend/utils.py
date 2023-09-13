from django.conf import settings


def build_absolute_url(reverse):
    return f"{settings.BASE_URL}{reverse}"
