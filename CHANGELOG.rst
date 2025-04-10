=========
Changelog
=========

v2.2.1 (2025-04-10)
===================

- include static files in package

v2.2.0 (2025-04-10)
===================

- remove red border; fix #6
- updated frontend wrapper logic to be more dynamic via JavaScript

v2.1.1 (2025-03-14)
===================

- semi-fix for #8; initializing works better, but is not perfect yet

v2.1.0 (2025-02-05)
===================

- fix version for django-time-wizard < 4.1.0 due to frontend errors

v2.0.0 (2024-03-08)
===================

- added tests to check if migrations are missing
- updated existing migrations to avoid 'missing migrations' for django 4+
- added/changed test environment to check against django-cms 4.1
- changed test environment to render plugins directly instead of depending on
  pages
- updated package informations regarding classifiers for python, django and
  django-cms

v1.0.7 (2023-09-28)
===================

- added `AppConfig.default_auto_field` to lock ID-fields in order to avoid
  migrations if projects use a different field in their settings

v1.0.6 (2023-01-16)
===================

- integrated tests for the cms plugin(s)

v1.0.5 (2023-01-13)
===================

- updated the testing environment
- little project-setup adjustments
