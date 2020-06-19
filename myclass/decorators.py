from django.http import HttpResponse
from django.shortcuts import redirect
#from django.core.exceptions import PermissionDenied
from guardian.shortcuts import get_user_perms
from . import models


def user_is_approved(function):
    def wrap(request, *args, **kwargs):
        class_item = models.Class.objects.get(id=kwargs['pk'])
        print(class_item.user.all())

        if class_item.user.all().filter(username=request.user.username).exists():
            if 'view_class' in get_user_perms(request.user, class_item):
                return function(request, *args, **kwargs)
        return HttpResponse('Unauthorized', status=401)
    return wrap

