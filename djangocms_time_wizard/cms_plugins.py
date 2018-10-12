from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from djangocms_time_wizard.models import TimeWizardModel
from djangocms_time_wizard.conf import DJANGOCMS_TIME_WIZARD_WRAPPER


class TimeWizardPlugin(CMSPluginBase):
    model = TimeWizardModel
    module = _('Time Wizard')
    name = _('Time Wizard')
    render_template = 'djangocms_time_wizard/time_wizard.html'
    allow_children = True

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['show_wrapper'] = DJANGOCMS_TIME_WIZARD_WRAPPER
        return context


plugin_pool.register_plugin(TimeWizardPlugin)
