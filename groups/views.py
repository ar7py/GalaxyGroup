# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.checks import messages
from django.db import models
from django.db.models import fields

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
from django.views import generic
from groups.models import Group, GroupMember
from . import models

app_name = 'groups'
# Create your views here.


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group


class SingleGroup(generic.DetailView):
    model = Group


class ListGroups(generic.ListView):
    model = Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except:
            messages.Warning(self.request, "WARNING! Already A Member")
        else:
            messages.success(
                self.request, "Joined The Group Succesfully! Now You Are A Member Of The Group")

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):

        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.Warning(
                self.request, "Sorry You Are Not A Member Of This Group!")
        else:
            membership.delete()
            messages.success(
                self.request, "You Have Left The Group Successfully!")

        return super().get(request, *args, **kwargs)
