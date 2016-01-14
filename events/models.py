from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField

PARTICIPATION_STATUSES = (
    (0, 'No, thanks'),
    (1, 'I may attend'),
    (2, 'I\'ll be there'),
)


class Event(models.Model):
    title = models.CharField(_('title'), max_length=200)
    location = models.CharField(_('location'), max_length=200)
    description = RichTextField()
    organizers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='organized_events', verbose_name=_('organizers'))
    date = models.DateField(_('event date'))
    date_added = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='Participation', related_name='in_events', verbose_name=_('participants'))

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['-date_added']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:event', args=[self.pk])


class Participation(models.Model):
    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='event_participations')
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('person'), related_name='person_participations')
    status = models.PositiveIntegerField(
        _('participation status'), choices=PARTICIPATION_STATUSES)
    date_registered = models.DateTimeField(
        _('date registered'), auto_now_add=True)

    def __str__(self):
        return '{} - {} ({})'.format(self.person, self.event, self.get_status_display())


class Participant(AbstractUser):
    location = models.CharField(_('location'), max_length=200, blank=True)
    website = models.URLField(_('website'), blank=True)
    bdate = models.DateField(_('birthday date'), blank=True, null=True)

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"

    def get_absolute_url(self):
        return reverse('account_profile', args=[self.pk, self.username])
