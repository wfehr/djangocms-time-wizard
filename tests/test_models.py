from app_helper.base_test import BaseTestCase
from cms.api import add_plugin, create_page
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from time_wizard.models import AbsolutePeriodModel, TimeWizardModel


class TestTimeWizardModel(BaseTestCase):
    def setUp(self):
        self.page = self._create_page()
        self.page.set_as_homepage()

    def test_plugin(self):
        time_wizard = TimeWizardModel.objects.create(
            name="dummy",
        )
        plugin = self._add_plugin(time_wizard)
        self._add_text_to_plugin(plugin, body="Hello World!")

        with self.subTest("no periods -> no output"):
            html = self._render_page().strip()
            self.assertNotIn("Hello World!", html)

        period = AbsolutePeriodModel.objects.create(
            content_type=ContentType.objects.get(
                app_label="time_wizard",
                model="timewizardmodel",
            ),
            object_id=time_wizard.pk,
            start=now(),
        )

        with self.subTest("content shown - start given"):
            html = self._render_page().strip()
            self.assertIn("Hello World!", html)

        with self.subTest("content not shown - end given"):
            period.end = now()
            period.save()
            html = self._render_page().strip()
            self.assertNotIn("Hello World!", html)

        with self.subTest("content shown - no start/end given"):
            period.start = None
            period.end = None
            period.save()
            html = self._render_page().strip()
            self.assertIn("Hello World!", html)

    def test_inline_plugin(self):
        plugin = self._add_inline_plugin()
        self._add_text_to_plugin(plugin, body="Hello Inline World!")

        with self.subTest("no periods -> no output"):
            html = self._render_page().strip()
            self.assertNotIn("Hello Inline World!", html)

        period = AbsolutePeriodModel.objects.create(
            content_type=ContentType.objects.get(
                app_label="djangocms_time_wizard",
                model="timewizardinlinemodel",
            ),
            object_id=plugin.pk,
            start=now(),
        )

        with self.subTest("content shown - start given"):
            html = self._render_page().strip()
            self.assertIn("Hello Inline World!", html)

        with self.subTest("content not shown - end given"):
            period.end = now()
            period.save()
            html = self._render_page().strip()
            self.assertNotIn("Hello Inline World!", html)

        with self.subTest("content shown - no start/end given"):
            period.start = None
            period.end = None
            period.save()
            html = self._render_page().strip()
            self.assertIn("Hello Inline World!", html)

    def _add_plugin(self, time_wizard, *args, **kwargs):
        return self._add_plugin_to_page(
            "TimeWizardPlugin",
            *args,
            time_wizard=time_wizard,
            **kwargs,
        )

    def _add_inline_plugin(self, *args, **kwargs):
        return self._add_plugin_to_page(
            "TimeWizardInlinePlugin",
            *args,
            **kwargs,
        )

    def _create_page(self, **kwargs):
        if "template" not in kwargs:
            kwargs["template"] = "page.html"
        if "title" not in kwargs:
            kwargs["title"] = "Home"
        if "language" not in kwargs:
            kwargs["language"] = "en"
        return create_page(**kwargs)

    def _add_text_to_plugin(
        self, parent, *args, page=None, **kwargs
    ):
        if page is None:
            page = self.page
        return add_plugin(
            page.placeholders.get(slot="content"),
            "TextPlugin",
            "en",
            "last-child",
            parent,
            *args,
            **kwargs,
        )

    def _add_plugin_to_page(self, plugin_publisher, *args, page=None, **kwargs):
        if page is None:
            page = self.page
        return add_plugin(
            page.placeholders.get(slot="content"),
            plugin_publisher,
            "en",
            *args,
            **kwargs,
        )

    def _render_page(self, page=None):
        if page is None:
            page = self.page
        page.publish("en")
        response = self.client.get(page.get_absolute_url())
        return response.content.decode("utf-8")
