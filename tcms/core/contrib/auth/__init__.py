# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import Group

# Python 2.7 has an importlib with import_module; for older Pythons,
# Django's bundled copy provides it.
try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module


def get_backend(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured(
            'Error loading registration backend %s: "%s"' % (module, e)
        )
    try:
        backend_class = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured(
            'Module "%s" does not define a registration '
            'backend named "%s"' % (module, attr)
        )
    return backend_class()


def get_using_backend():
    return get_backend(settings.AUTHENTICATION_BACKENDS[0])


def initiate_user_with_default_setups(user):
    '''
    Add default groups, permissions, status to a newly
    created user.
    '''
    default_groups = Group.objects.filter(name__in=settings.DEFAULT_GROUPS)
    user.is_active = True
    for grp in default_groups:
        user.groups.add(grp)
    user.save()
