from django.http import HttpRequest
from .models import Tag


def all_tags(request: HttpRequest) -> dict:
    return {'all_tags': Tag.objects.all()}
