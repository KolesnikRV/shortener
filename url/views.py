from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

import redis

from functions.functions import get_session_instance, make_short_url
from .models import Url
from .forms import UrlForm

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


def index(request):
    try:
        session_instance = get_session_instance(request)
        form = UrlForm(request.POST or None)

        if request.POST:
            short_url = make_short_url(request, redis_instance=redis_instance,
                                       subpart=request.POST.get('short_url'))
            if form:  # is_valid()
                url = form.save(commit=False)
                url.short_url = short_url
                url.user = session_instance
                print(short_url, len(short_url), '--------')
                url.save()
                redis_instance.set(short_url, url.full_url,
                                   ex=settings.CLEAR_DATA_MINUTES*60)

        url_list = session_instance.urls.all()
        paginator = Paginator(url_list, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        context = {
            'page': page,
            'paginator': paginator,
            # 'urls_list': url_list,
            'form': form
        }
        print(request.session.session_key)
        return render(request, 'index.html', context)

    except ObjectDoesNotExist as e:
        print(e.__class__)
        response = redirect('url:index')
        response.delete_cookie('sessionid')
        return response


def url_redirect(request):
    print(dir(request))
    print(request.get_host() + request.path)

    url = Url.objects.get(short_url=request.build_absolute_uri())
    print('----------')

    print(url.full_url)
    return redirect(url.full_url)
