from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import IntegerField, Case, When, Count
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from notifications.signals import notify

from .models import PARTICIPATION_STATUSES, Event, Participation, Participant
from .forms import NotificationForm


class EventListView(ListView):
    model = Event
    template_name = "events/events.html"
    context_object_name = 'events'
    paginate_by = 10


class EventsStatistics(LoginRequiredMixin, StaffuserRequiredMixin, ListView):
    model = Event
    template_name = "events/events_stats.html"
    context_object_name = 'events'
    paginate_by = 25

    def get_queryset(self):
        queryset = self.model.objects.all()
        queryset = queryset.annotate(
            declined=Count(
                Case(When(event_participations__status=0, then=1),
                     output_field=IntegerField())
            ),
            not_sure=Count(
                Case(When(event_participations__status=1, then=1),
                     output_field=IntegerField())
            ),
            accepted=Count(
                Case(When(event_participations__status=2, then=1),
                     output_field=IntegerField())
            )
        )
        return queryset


class EventDetailView(DetailView):
    model = Event
    template_name = "events/event.html"
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        context['participation_statuses'] = PARTICIPATION_STATUSES
        if self.request.user.is_authenticated():
            try:
                context['user_status'] = Participation.objects.get(
                    person=self.request.user, event=self.object).status
            except Participation.DoesNotExist:
                pass
        return context


class EventCreateView(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    model = Event
    template_name = "events/event_create.html"
    fields = ['title', 'description', 'date', 'organizers']


class EventUpdateView(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):
    model = Event
    template_name = "events/event_edit.html"
    fields = ['title', 'description', 'date', 'organizers']


class SendNotification(LoginRequiredMixin, StaffuserRequiredMixin, FormView):
    template_name = 'events/send_notification.html'
    form_class = NotificationForm
    success_url = '/'

    def form_valid(self, form):
        actor = self.request.user
        title = form.cleaned_data['verb']
        description = form.cleaned_data['description']
        to_events = form.cleaned_data['related_events']
        for event in to_events:
            users_to_notify = event.participants.filter(
                person_participations__status__in=[1, 2])
            for user in users_to_notify:
                notify.send(
                    actor, recipient=user, verb=title, target=event, description=description)
        return super(SendNotification, self).form_valid(form)


@require_POST
@login_required
@transaction.atomic
def participate(request):
    status_n = request.POST.get('status_n', None)
    event_pk = request.POST.get('event_pk', None)
    if status_n:
        event = get_object_or_404(Event, pk=event_pk)
        try:
            participation = Participation.objects.get(
                event=event, person=request.user)
            participation.status = status_n
            participation.save()
        except Participation.DoesNotExist:
            participation = Participation(
                event=event, person=request.user, status=status_n)
            participation.save()
        return HttpResponse()
    return HttpResponseBadRequest()


@require_GET
@login_required
@staff_member_required
def get_attendees(request):
    event_pk = request.GET.get('event_pk', None)
    if event_pk:
        event = get_object_or_404(Event, pk=event_pk)
        event_participants = event.participants.all()
        context = {}
        context['attendees_sure'] = list(event_participants.filter(
            person_participations__status=2).values('pk', 'username'))
        context['attendees_not_sure'] = list(event_participants.filter(
            person_participations__status=1).values('pk', 'username'))
        context['attendees_declined'] = list(event_participants.filter(
            person_participations__status=0).values('pk', 'username'))
        return JsonResponse(context)
    return HttpResponseBadRequest()
