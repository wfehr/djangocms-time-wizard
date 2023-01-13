from setuptools import find_packages, setup
from djangocms_time_wizard import __version__


setup(
    name='djangocms-time-wizard',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'django-cms',
        'django-time-wizard',
    ],
    include_package_data=True,
    description='Simple plugin with django-time-wizard relation',
    long_description=open('README.rst').read(),
    url='https://github.com/wfehr/djangocms-time-wizard',
    download_url='https://github.com/wfehr/djangocms-time-wizard/'
                 'tarball/master',
    author='Wolfgang Fehr',
    author_email='dev@wfehr.de',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
