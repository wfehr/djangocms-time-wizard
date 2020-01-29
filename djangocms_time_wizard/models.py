from cms.models import CMSPlugin
from time_wizard.mixins import TimeWizardInlineMixin, TimeWizardMixin


class TimeWizardModel(TimeWizardMixin, CMSPlugin):
    pass


class TimeWizardInlineModel(TimeWizardInlineMixin, CMSPlugin):
    pass
