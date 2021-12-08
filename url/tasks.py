
import logging
from datetime import datetime, timedelta

from django.conf import settings

from shortener.celery import app
from url.models import Url

logger = logging.getLogger('celery_logger')


@app.task
def delete_old_data_db():
    '''Celery task for deleting old records in database

    Using CLEAR_DATA_MINUTES param from django settings
    '''
    clear_data_timedelta = timedelta(minutes=settings.CLEAR_DATA_MINUTES)
    old_data_time = datetime.now() - clear_data_timedelta
    old_data_query = Url.objects.filter(creation_date__lte=old_data_time)
    count_data = old_data_query.count()

    logger.info(
        f'Delete {count_data} records from database older than {old_data_time}'
    )

    old_data_query.delete()
