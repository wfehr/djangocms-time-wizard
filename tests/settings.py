HELPER_SETTINGS = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    },
    'INSTALLED_APPS': (
        'polymorphic',
        'time_wizard',
        'djangocms_time_wizard',
        'djangocms_text_ckeditor',
    ),
    'SECRET_KEY': 'foobar1337',
    'TIME_WIZARD_COUNTRIES': ['US'],
    'TIME_WIZARD_COUNTRY_PROVINCES': {'US': ['AL']},
    'CMS_CONFIRM_VERSION4': True,
}


def run():
    from app_helper import runner
    runner.run('djangocms_time_wizard')


if __name__ == '__main__':
    run()
