from rest_framework import generics

from .serializers import UrlSerializer
from functions.functions import get_session_instance


class UrlView(generics.ListCreateAPIView):
    serializer_class = UrlSerializer

    def get_queryset(self):
        session_instance = get_session_instance(self.request)
        return session_instance.urls.all()
