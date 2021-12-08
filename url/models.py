from django.contrib.sessions.models import Session
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Url(models.Model):
    '''Model for storage full and short url versions'''
    user = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        null=False,
        related_name='urls'
    )
    full_url = models.URLField(
        verbose_name=_('Полная ссылка')
    )
    short_url = models.CharField(
        verbose_name=_('Сокращенная ссылка'),
        max_length=100,
        blank=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_,/.:;&@]*$',
                message=_('Неверный формат, '
                          'пробельные символы не поддерживаются.'),
            ),
        ]
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Cсылка')
        verbose_name_plural = _('Ссылки')
        ordering = ('-creation_date',)

    def __str__(self):
        return self.short_url
