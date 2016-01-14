from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden

from braces.views import LoginRequiredMixin


class Home(TemplateView):
    template_name = "core/index.html"


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = "core/user.html"
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['organized_events'] = self.object.organized_events.all()
        context['in_events'] = self.object.in_events.filter(event_participations__status__in=[1, 2])
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ['first_name', 'last_name', 'username',
              'location', 'email', 'website', 'bdate']
    template_name = "core/user_edit.html"

    def get_object(self, queryset=None):
        return self.request.user
