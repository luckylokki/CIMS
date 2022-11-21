from django.http import HttpResponseRedirect
from CIMS import settings


class WithoutLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return super(WithoutLoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class StaffProfileRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return super(StaffProfileRequiredMixin, self).dispatch(request, *args, **kwargs)
