from django.http import HttpResponseForbidden
from django.views.generic import View


# a custom mixin to enforce create/update restrictions for non-admins
class RoleRequiredMixin(View):
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        if user_profile.role != self.required_role:
            return HttpResponseForbidden("This page is only accessible for admins.")
        return super().dispatch(request, *args, **kwargs)
