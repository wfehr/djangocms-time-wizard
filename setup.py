import os

from setuptools import find_packages, setup
from djangocms_time_wizard import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangocms-time-wizard',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'django-cms',
        'django-time-wizard',
        'django<3.0',
    ],
    include_package_data=True,
    description='Simple plugin with django-time-wizard relation',
    long_description=README,
    url='https://github.com/wfehr/djangocms-time-wizard',
    download_url='https://github.com/wfehr/djangocms-time-wizard/'
                 'tarball/master',
    author='Wolfgang Fehr',
    author_email='dev@wfehr.de',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
