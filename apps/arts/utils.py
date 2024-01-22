from django.core.cache import cache

from apps.core.utils import get_client_ip


def check_valid_ip_for_hit_count(request):
    return cache.get(get_client_ip(request), None)
