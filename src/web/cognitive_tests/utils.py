from django.db import models
import ast
from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.decorators import available_attrs, decorator_from_middleware
from functools import wraps
from .models import Participant
from django.core import urlresolvers
import urllib.parse


def redirect_with_args(to, query_string, *args, **kwargs):
    if query_string:
        path = "%s?%s" % (urlresolvers.reverse(to, *args, **kwargs), urllib.parse.urlencode(query_string))
        return redirect(path, *args, **kwargs)
    return redirect(to, *args, **kwargs)


def reverse_with_args(to, query_string, *args, **kwargs):
    if query_string:
        path = "%s?%s" % (urlresolvers.reverse(to, *args, **kwargs), urllib.parse.urlencode(query_string))
        return path
    return urlresolvers.reverse(to, *args, **kwargs)



def participant_required(redirect_to):
    def _actual_decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view_func(request, *args, **kwargs):
            participant = get_participant(request)
            if not participant:
                if redirect_to:
                    return redirect(redirect_to)
                else:
                    raise Http404
            return view_func(request, participant, *args, **kwargs)
        return _wrapped_view_func
    return _actual_decorator


def get_participant(request):
    if Participant.PARTICIPANT_SESSION_KEY not in request.session:
        return None
    try:
        return Participant.objects.get(session=request.session.session_key)
    except:
        del request.session[Participant.PARTICIPANT_SESSION_KEY]
        return None


class ListField(models.CharField):
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class SeparatedValuesField(models.CharField):

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value, **kwargs):
        if not value:
            return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([str(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
