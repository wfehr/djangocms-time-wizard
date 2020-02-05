from cms.models import CMSPlugin
from time_wizard.mixins import TimeWizardInlineMixin, TimeWizardMixin


class TimeWizardModel(TimeWizardMixin, CMSPlugin):
    pass


class TimeWizardInlineModel(TimeWizardInlineMixin, CMSPlugin):
    # Copy of related PeriodModels when publishing the page
    def copy_relations(self, old_instance):
        for periods in old_instance.periods.all():
            # pk + id to None: https://stackoverflow.com/a/25852807
            periods.pk = None
            periods.id = None
            periods.object_id = self.id
            periods.save()
