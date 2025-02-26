from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


from resmio_app.repositories import FacilityRepository

class FacilityManageView(LoginRequiredMixin, ListView):
    """
    View to list and create facilities.
    """
    template_name = "facility/facility_manage.html"
    context_object_name = "facilities"
    login_url           = reverse_lazy("login")


    def get_queryset(self):
        """Fetches all facilities using the repository."""
        return FacilityRepository.get_all_facilities()

    def get_context_data(self, **kwargs):
        """Adds facility list to context."""
        context = super().get_context_data(**kwargs)
        context["facilities"] = self.get_queryset()
        return context
