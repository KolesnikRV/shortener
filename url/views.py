import logging

import redis
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from functions.functions import get_session_instance, make_short_url

from .forms import UrlForm
from .models import Url

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)

logger = logging.getLogger(__package__ + '_logger')


@require_http_methods(["GET", "POST"])
def index(request):
    '''View for processing user requests

    Accepts only GET and POST requests
    Functionality:
        - form validation
        - saving data to database
        - saving data to redis
    Error handling:
        - session key expired (ObjectDoesNotExist)
        - short url already exists (ValueError)

    Returns template (index.html)
    '''
    logger.info(f'{request.method} request from User:'
                f'{request.session.session_key} data:=%s',
                request.POST.dict())
    try:
        session_instance = get_session_instance(request)
    except ObjectDoesNotExist as e:
        logger.warning(f'User:{request.session.session_key}'
                       'session key expired')
        response = redirect('url:index')
        response.delete_cookie('sessionid')
        return response

    form = UrlForm(request.POST or None)
    try:
        if request.POST:
            short_url = make_short_url(request, redis_instance=redis_instance,
                                       subpart=request.POST.get('short_url'))
            if form.is_valid():
                url = form.save(commit=False)
                url.short_url = short_url
                url.user = session_instance
                url.save()
                redis_instance.set(short_url, url.full_url,
                                   ex=int(settings.CLEAR_DATA_MINUTES) * 60)
    except ValueError as e:
        form.add_error('short_url', e)

    url_list = session_instance.urls.all()
    paginator = Paginator(url_list, settings.PAGINATION_PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator,
        'form': form
    }

    return render(request, 'index.html', context)


def url_redirect(request):
    '''
    View for redirecting users to full_url by short_url
    '''
    url = Url.objects.get(short_url=request.build_absolute_uri())

    return redirect(url.full_url)
