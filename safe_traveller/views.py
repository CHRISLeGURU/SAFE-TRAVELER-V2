from django.views.generic import TemplateView
from django.contrib.staticfiles.storage import staticfiles_storage

class SWView(TemplateView):
    template_name = 'sw.js'
    content_type = 'application/javascript'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['STATIC_URL'] = staticfiles_storage.base_url
        return context
