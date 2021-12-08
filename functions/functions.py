import random

from django.conf import settings

from url.models import Session, Url


def get_session_instance(request) -> Session:
    '''Function for creating and saving session instance

    Params:
        request

    Returns:
        Session object
    '''
    if not request.session or not request.session.session_key:
        request.session.save()

    return Session.objects.get(session_key=request.session.session_key)


def get_short_random_string(N=settings.SHORT_URL_LENGTH, subpart=None,
                            alphabet=settings.ALPHABET) -> str:
    '''Creationg random string of symbols

    Params:
        SHORT_URL_LENGTH: int - lengs of generated string
        ALPHABED: str - string of symbols from whitch to choose
        subpart: str - desired subpart by user

    Returns:
        String
    '''
    if subpart:
        return subpart

    return ''.join(random.SystemRandom().choice(alphabet) for _ in range(N))


def url_exists(short_url, redis_instance) -> bool:
    '''Check if url already exists

    Params:
        short_url: str - short version of long url
        redis_instance -  instance of redis connection

    Returns:
        True/False
    '''


    return (Url.objects.filter(short_url=short_url).exists()
            or redis_instance.get(short_url))


def get_shor_url_str(domain, subpart) -> str:
    '''Make string in Url format http://{domain}/{subpart}

    Params:
        domain: str - domain part of url
        subpart: str - address on domain


    '''
    return 'http://{domain}/{subpart}'.format(
            domain=domain,
            subpart=subpart
        )


def make_short_url(request, subpart, redis_instance) -> str:
    '''Make short url from request data.

    If url is exists raise Exception()
    Note if subpart=None, then make random subpart until url not exists

    Params:
        request
        subpart: str - desired subpart by user
        redis_instance -  instance of redis connection

    Returns:
        String
    '''
    domain = request.get_host()
    subpart = get_short_random_string(subpart=subpart.strip())
    short_url = get_shor_url_str(domain, subpart)

    if subpart and url_exists(short_url, redis_instance):
        raise ValueError('Ссылка уже существует')

    while url_exists(short_url, redis_instance):
        subpart = get_short_random_string()
        short_url = get_shor_url_str(domain, subpart)

    return short_url
