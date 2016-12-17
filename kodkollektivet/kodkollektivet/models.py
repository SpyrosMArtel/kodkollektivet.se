# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta

from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers.UserManager import UserManager
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

class BaseUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=254, blank=True)
    last_name = models.CharField(max_length=254, blank=True)

    email = models.EmailField(_('email address'), max_length=254, unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('baseuser')
        verbose_name_plural = _('baseusers')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.first_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def set_last_login(self, last_login):
        self.last_login = last_login

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish=True)


class Event(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(help_text="Markdown syntax can be used!")
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    date = models.DateField()
    time = models.TimeField()
    publish = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)

    #objects = PostQuerySet.as_manager()

    def is_upcomming_event(self):
        return self.datetime >= timezone.now()

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """Set slug"""
        if not self.slug:
            self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Event post"
        verbose_name_plural = "Event posts"
        ordering = ["-created_date"]


class Project(models.Model):
    name = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(blank=True)

    # Github specific
    gh_name = models.CharField(max_length=254, blank=True)
    gh_id = models.IntegerField(blank=True, null=True)
    gh_url = models.CharField(max_length=254, blank=True)
    gh_readme = models.TextField(blank=True, help_text='Project readme. Markdown syntax!')

    def save(self, *args, **kwargs):

        """
        Set slug
        """
        if not self.name:
            self.name = self.gh_name

        if not self.slug:
            self.slug = slugify(self.name)

        super(Project, self).save(*args, **kwargs)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.slug


class Role(models.Model):
    role = models.CharField(max_length=254, blank=True)
    slug = models.CharField(max_length=254, blank=True)

    def save(self, *args, **kwargs):
        """
        Set slug
        """
        self.slug = slugify(self.role)
        super(Role, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

class Contributor(BaseUser):
    slug = models.CharField(max_length=254, blank=True, null=True)
    website = models.CharField(max_length=254, blank=True, null=True)
    linkedin = models.CharField(max_length=254, blank=True, null=True)

    about = models.TextField(blank=True, help_text='Markdown syntax', null=True)
    has_paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(_('date paid'), null=True)
    # Github specific
    gh_login = models.CharField(max_length=254, null=True)
    gh_url = models.CharField(max_length=254, null=True)
    gh_id = models.IntegerField(null=True)
    gh_html = models.CharField(max_length=254, blank=True, null=True)
    gh_avatar = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        ordering = ['slug']

class Language(models.Model):
    name = models.CharField(max_length=254)
    slug = models.CharField(max_length=254, blank=True)

    def save(self, *args, **kwargs):
        """
        Set slug
        """
        self.slug = self.name
        super(Language, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Framework(models.Model):
    name = models.CharField(max_length=254)
    slug = models.CharField(max_length=254, blank=True)

    def save(self, *args, **kwargs):
        """
        Set slug
        """
        self.slug = self.name
        super(Framework, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class ProFra(models.Model):
    project = models.ForeignKey(Project)
    framework = models.ForeignKey(Framework)

    class Meta:
        verbose_name = 'Project-Framework relation'


class ProCon(models.Model):
    project = models.ForeignKey(Project)
    contributor = models.ForeignKey(Contributor)

    class Meta:
        verbose_name = 'Project-Contributor relation'


class ProLan(models.Model):
    project = models.ForeignKey(Project)
    language = models.ForeignKey(Language)

    class Meta:
        verbose_name = 'Project-Language relation'


class ProRol(models.Model):
    project = models.ForeignKey(Project)
    contributor = models.ForeignKey(Contributor)
    role = models.ForeignKey(Role)

    class Meta:
        verbose_name = 'Project-Role-Contributor relation'

