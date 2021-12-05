from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('api', include('api.urls')),
    path('', include('url.urls', namespace='url')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
