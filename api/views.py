import logging

from django.conf import settings
from rest_framework import generics

from functions.functions import get_session_instance

from .serializers import UrlSerializer, redis_instance

logger = logging.getLogger(__package__ + '_logger')


class UrlView(generics.ListCreateAPIView):
    '''Api view for Url model
    Supports GET and POST methods
    '''
    serializer_class = UrlSerializer

    def get_queryset(self):
        '''Getting all records of current user'''
        logger.info(f'{self.request.method} request from User:'
                    f'{self.request.session.session_key} data:=%s',
                    self.request.POST.dict())
        session_instance = get_session_instance(self.request)

        return session_instance.urls.all()

    def perform_create(self, serializer):
        '''Creating new records in database and redis'''
        short_url = serializer.validated_data.get('short_url')
        full_url = serializer.validated_data.get('full_url')
        redis_instance.set(short_url, full_url,
                           ex=int(settings.CLEAR_DATA_MINUTES) * 60)

        serializer.save()
