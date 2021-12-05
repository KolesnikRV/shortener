import string
import random

from django.conf import settings

from url.models import Session, Url


def get_session_instance(request) -> Session:
    if not request.session or not request.session.session_key:
        request.session.save()

    return Session.objects.get(session_key=request.session.session_key)


def get_short_random_string(N=settings.SHORT_URL_LENGTH) -> str:

    return ''.join(random.SystemRandom().choice(
                   string.ascii_letters + string.digits)
                   for _ in range(N))


def url_exists(short_url, redis_instance) -> bool:

    return (Url.objects.filter(short_url=short_url).exists()
            or redis_instance.get(short_url))


def get_shor_url_str(domain, subpart) -> str:
    return 'http://{domain}/{subpart}'.format(
            domain=domain,
            subpart=subpart
        )


def make_short_url(request, subpart, redis_instance) -> str:
    if not subpart:
        subpart = get_short_random_string()
    domain = request.get_host()
    short_url = get_shor_url_str(domain, subpart)

    while url_exists(short_url, redis_instance):
        print('hamster ------')
        subpart += get_short_random_string(2)
        short_url = get_shor_url_str(domain, subpart)

    print(short_url)
    return short_url
