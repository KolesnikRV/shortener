from django.conf import settings
from rest_framework import generics

import redis

from .serializers import UrlSerializer
from functions.functions import get_session_instance, make_short_url

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


class UrlView(generics.ListCreateAPIView):
    serializer_class = UrlSerializer

    def get_queryset(self):
        session_instance = get_session_instance(self.request)
        print(session_instance)
        return session_instance.urls.all()

    def perform_create(self, serializer):
        serializer.validated_data['short_url'] = make_short_url(
            self.request, redis_instance=redis_instance,
            subpart=self.request.POST.get('short_url'))
        serializer.validated_data['user_id'] = (
            self.request.session._get_session_key()
            )
        return super().perform_create(serializer)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
