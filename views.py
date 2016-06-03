from django.conf import settings
from django.views.generic import TemplateView


class Dashboard(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['nodes'] = settings.DCMS_NODES
        context['types'] = settings.DCMS_TYPES
        return context
