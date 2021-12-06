import random

from django.conf import settings

from url.models import Session, Url


def get_session_instance(request) -> Session:
    if not request.session or not request.session.session_key:
        request.session.save()

    return Session.objects.get(session_key=request.session.session_key)


def get_short_random_string(N=settings.SHORT_URL_LENGTH, subpart=None,
                            alphabet=settings.ALPHABET) -> str:
    if subpart:
        return subpart

    return ''.join(random.SystemRandom().choice(alphabet) for _ in range(N))


def url_exists(short_url, redis_instance) -> bool:

    return (Url.objects.filter(short_url=short_url).exists()
            or redis_instance.get(short_url))


def get_shor_url_str(domain, subpart) -> str:
    return 'http://{domain}/{subpart}'.format(
            domain=domain,
            subpart=subpart
        )


def make_short_url(request, subpart, redis_instance) -> str:
    domain = request.get_host()
    subpart = get_short_random_string(subpart=subpart)
    short_url = get_shor_url_str(domain, subpart)

    if subpart and url_exists(short_url, redis_instance):
        raise ValueError('url already exists')

    while url_exists(short_url, redis_instance):
        subpart = get_short_random_string()
        short_url = get_shor_url_str(domain, subpart)

    return short_url
