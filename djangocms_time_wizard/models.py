from cms.models import CMSPlugin
from time_wizard.models import TimeWizardMixin


class TimeWizardModel(TimeWizardMixin, CMSPlugin):
    pass
