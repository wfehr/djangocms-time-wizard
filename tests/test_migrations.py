from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class MigrationTestCase(TestCase):
    def test_for_missing_migrations(self):
        output = StringIO()
        try:
            call_command(
                "makemigrations",
                "djangocms_time_wizard",
                interactive=False,
                dry_run=True,
                stdout=output,
                check_changes=True,
            )
        except SystemExit:
            self.fail("Missing migrations:\n{}".format(output.getvalue()))
        else:
            pass
