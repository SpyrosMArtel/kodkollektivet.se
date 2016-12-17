from datetime import datetime, timedelta, time
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .forms import ContributorForm
from django.utils import timezone

from . import models


class IndexView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        m = models.Event.objects.filter(date__gte=datetime.now())
        context['upcomming_events'] = m
        context['header_text'] = 'Kodkollektivet'
        return context


class BoardTemplateView(TemplateView):
    template_name = 'board.html'

    def get_context_data(self, **kwargs):
        context = super(BoardTemplateView, self).get_context_data(**kwargs)
        context['header_text'] = _('Board')
        return context
    

class EventsListView(ListView):
    queryset = models.Event.objects.all()
    template_name = "events/events_list_view.html"

    def get_context_data(self, **kwargs):
        context = super(EventsListView, self).get_context_data(**kwargs)
        context['header_text'] = _('Events')
        return context


class EventsDetailView(DetailView):
    model = models.Event
    template_name = "events/events_detail_view.html"


class ProjectsListView(ListView):
    """Project List View"""
    model = models.Project
    template_name = 'projects/projects.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectsListView, self).get_context_data(**kwargs)
        context['header_text'] = _('Projects')
        return context


class ProjectsDetailView(DetailView):
    """Project Detail View"""
    model = models.Project
    template_name = 'projects/projects_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectsDetailView, self).get_context_data(**kwargs)
        gh_id = kwargs['object'].gh_id
        procons = models.ProCon.objects.filter(project__gh_id=gh_id)
        profras = models.ProFra.objects.filter(project__gh_id=gh_id)
        prolans= models.ProLan.objects.filter(project__gh_id=gh_id)
        languages = [i.language for i in prolans]
        contributors = [i.contributor for i in procons]
        frameworks = [i.framework for i in profras]
        context['header_text'] = kwargs['object'].name
        context['languages'] = languages
        context['contributors'] = contributors
        context['frameworks'] = frameworks
        return context

class ContributorRegisterView(CreateView):
    form_class = ContributorForm
    model = models.Contributor
    template_name = 'registration/registration_form.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(form.cleaned_data['password'])
        obj.save()

        # This form only requires the "email" field, so will validate.
        reset_form = PasswordResetForm(self.request.POST)
        reset_form.is_valid()  # Must trigger validation
        # Copied from django/contrib/auth/views.py : password_reset
        opts = {
            'use_https': self.request.is_secure(),
            'email_template_name': 'registration/verification.html',
            'subject_template_name': 'registration/verification_subject.txt',
            'request': self.request,
            # 'html_email_template_name': provide an HTML content template if you desire.
        }
        # This form sends the email on save()
        reset_form.save(**opts)

        return redirect('kodkollektivet:register-done')

        # return redirect('accounts:register-done')

class ContributorDetailView(DetailView):
    """Contributor Detail View"""
    model = models.Contributor
    template_name = 'projects/contributor_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(ContributorDetailView, self).get_context_data(**kwargs)
        gh_id = kwargs['object'].gh_id
        procons = models.ProCon.objects.filter(contributor__gh_id=gh_id)
        projects = [i.project for i in procons]
        context['projects'] = projects
        return context
    
