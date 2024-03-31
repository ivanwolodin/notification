import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDTimeStampedMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NotificationType(models.TextChoices):
    PERIOD = 'period'
    MOMENT = 'now'


class Template(UUIDTimeStampedMixin, models.Model):
    name = models.CharField(
        _('Name'), max_length=250, unique=True, help_text='Template name'
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
        help_text='Template description',
    )
    subject = models.CharField(_('Subject'), max_length=250)
    body = models.TextField(_('Body'))

    class Meta:
        db_table = 'templates'
        verbose_name = _('Templates')
        verbose_name_plural = _('Templates')

    def __str__(self):
        return self.name


class Notification(UUIDTimeStampedMixin, models.Model):
    name = models.CharField(_('Name'), max_length=254)
    description = models.TextField(_('Description'), blank=True, null=True)
    user_id = models.CharField(
        max_length=255, blank=True, null=True, help_text=_('User ID')
    )
    email = models.CharField(
        max_length=255, blank=True, null=True, help_text=_('Email')
    )
    template = models.ForeignKey(
        Template, on_delete=models.PROTECT, verbose_name=_('Template')
    )
    event_type = models.CharField(
        _('Event type'),
        max_length=50,
        choices=NotificationType.choices,
        default=NotificationType.PERIOD,
    )
    every_day = models.IntegerField(_('Every_day'), null=True, blank=True)
    processed = models.DateTimeField(_('Processed'), null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = _('Notifications')
        verbose_name_plural = _('Notifications')

    def __str__(self):
        return self.name
