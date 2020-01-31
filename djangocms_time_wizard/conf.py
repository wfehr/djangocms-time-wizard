from django.conf import settings

DJANGOCMS_TIME_WIZARD_WRAPPER = getattr(settings,
                                        'DJANGOCMS_TIME_WIZARD_WRAPPER',
                                        True)
