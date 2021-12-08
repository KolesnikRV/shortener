import redis
from django.conf import settings
from rest_framework import serializers

from functions.functions import make_short_url
from url.models import Url

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


class UrlSerializer(serializers.ModelSerializer):
    '''Serializer for Url model'''
    class Meta:
        model = Url
        fields = ('full_url', 'short_url')

    def create(self, validated_data):
        '''Setting user_id and short_url to validated data'''
        request = self.context.get('request')
        validated_data['user_id'] = (
                request.session._get_session_key()
            )
        try:
            validated_data['short_url'] = make_short_url(
                request, redis_instance=redis_instance,
                subpart=request.POST.get('short_url'))
        except ValueError as e:
            raise serializers.ValidationError(e)

        return Url.objects.create(**validated_data)
