from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

import redis

from functions.functions import get_session_instance, make_short_url
from .models import Url
from .forms import UrlForm

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


def index(request):
    try:
        session_instance = get_session_instance(request)
    except ObjectDoesNotExist as e:
        response = redirect('url:index')
        response.delete_cookie('sessionid')
        return response

    form = UrlForm(request.POST or None)
    try:
        if request.POST:
            short_url = make_short_url(request, redis_instance=redis_instance,
                                       subpart=request.POST.get('short_url'))
            if form:  # is_valid()
                url = form.save(commit=False)
                url.short_url = short_url
                url.user = session_instance
                url.save()
                redis_instance.set(short_url, url.full_url,
                                   ex=int(settings.CLEAR_DATA_MINUTES) * 60)
    except ValueError as e:
        form.add_error('short_url', str(e))  # lazy

    url_list = session_instance.urls.all()
    paginator = Paginator(url_list, settings.PAGINATION_PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator,
        'form': form
    }
    print(request.session.session_key)
    return render(request, 'index.html', context)


def url_redirect(request):
    url = Url.objects.get(short_url=request.build_absolute_uri())

    return redirect(url.full_url)
