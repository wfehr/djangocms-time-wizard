from app_helper.base_test import BaseTestCase
from cms.models import Placeholder
from cms.api import add_plugin, create_page
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from time_wizard.models import AbsolutePeriodModel, TimeWizardModel

from cms.plugin_rendering import ContentRenderer
from django.test.client import RequestFactory


class TestTimeWizardModel(BaseTestCase):
    def setUp(self):
        self.page = self._create_page()
        self.page.set_as_homepage()

    def test_plugin(self):
        time_wizard = TimeWizardModel.objects.create(
            name="dummy",
        )
        model_instance = self._add_plugin(time_wizard)
        self._add_text_to_plugin(model_instance, body="Hello World!")

        with self.subTest("no periods -> no output"):
            html = self._render_plugin(model_instance)
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
            html = self._render_plugin(model_instance)
            model_instance.refresh_from_db()
            self.assertIn("Hello World!", html)

        with self.subTest("content not shown - end given"):
            period.end = now()
            period.save()
            html = self._render_plugin(model_instance)
            self.assertNotIn("Hello World!", html)

        with self.subTest("content shown - no start/end given"):
            period.start = None
            period.end = None
            period.save()
            html = self._render_plugin(model_instance)
            self.assertIn("Hello World!", html)

    def test_inline_plugin(self):
        model_instance = self._add_inline_plugin()
        self._add_text_to_plugin(model_instance, body="Hello Inline World!")

        with self.subTest("no periods -> no output"):
            html = self._render_plugin(model_instance)
            self.assertNotIn("Hello Inline World!", html)

        period = AbsolutePeriodModel.objects.create(
            content_type=ContentType.objects.get(
                app_label="djangocms_time_wizard",
                model="timewizardinlinemodel",
            ),
            object_id=model_instance.pk,
            start=now(),
        )

        with self.subTest("content shown - start given"):
            html = self._render_plugin(model_instance)
            self.assertIn("Hello Inline World!", html)

        with self.subTest("content not shown - end given"):
            period.end = now()
            period.save()
            html = self._render_plugin(model_instance)
            self.assertNotIn("Hello Inline World!", html)

        with self.subTest("content shown - no start/end given"):
            period.start = None
            period.end = None
            period.save()
            html = self._render_plugin(model_instance)
            self.assertIn("Hello Inline World!", html)

    def _add_plugin(self, time_wizard, *args, **kwargs):
        return self._add_plugin_to_placeholder(
            "TimeWizardPlugin",
            *args,
            time_wizard=time_wizard,
            **kwargs,
        )

    def _add_inline_plugin(self, *args, **kwargs):
        return self._add_plugin_to_placeholder(
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

    def _add_text_to_plugin(self, parent, *args, **kwargs):
        return self._add_plugin_to_placeholder(
            "TextPlugin",
            position="last-child",
            target=parent,
            **kwargs,
        )

    def _add_plugin_to_placeholder(self, plugin_publisher, *args, **kwargs):
        model_instance = add_plugin(
            Placeholder.objects.get_or_create(slot="test")[0],
            plugin_publisher,
            "en",
            *args,
            **kwargs,
        )
        # see cms.tests.test_rendering for reference (of filling child-plugins)
        if "target" in kwargs:
            parent = kwargs["target"]
            if parent.child_plugin_instances is None:
                parent.child_plugin_instances = []
            parent.child_plugin_instances.append(model_instance)
        return model_instance

    def _render_plugin(self, model_instance):
        request = RequestFactory()
        request.current_page = None
        renderer = ContentRenderer(request=request)
        html = renderer.render_plugin(model_instance, {"request": request})
        return html
