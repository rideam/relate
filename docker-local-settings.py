"""
Docker-specific local settings for RELATE
This file is designed to work with the docker-compose.yml configuration
"""
from __future__ import annotations

import os
import os.path as path

import environ


_BASEDIR = path.dirname(path.abspath(__file__))


env = environ.Env()
env.read_env(os.path.join(_BASEDIR, ".env"))

# Security
SECRET_KEY = env("SECRET_KEY", default="dev-secret-key-change-in-production")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "0.0.0.0"])

# Set both of these to true if serving your site exclusively via HTTPS.
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False


from django.utils.translation import gettext_noop


RELATE_CUSTOMIZED_SITE_NAME = gettext_noop(env("SITE_NAME",default="AmplePalm"))


# Database Configuration
if "DATABASE_URL" in os.environ:
    DATABASES = {"default": env.db()}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": _BASEDIR / "db.sqlite3",
        }
    }

# Cache Configuration
# CACHE_URL = os.environ.get('CACHE_URL')
# if CACHE_URL and 'memcached' in CACHE_URL:
#     CACHES = {
#         'default': {
#             'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
#             'LOCATION': CACHE_URL.replace('memcached://', ''),
#         }
#     }
# else:
#     CACHES = {
#         'default': {
#             'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         }
#     }

# Celery Configuration
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://redis:6379/0")
# CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')


# Time Zone
TIME_ZONE = "UTC"

# Git Storage
GIT_ROOT = path.join(_BASEDIR, "git-roots")

# Bulk Storage
from django.core.files.storage import FileSystemStorage


RELATE_BULK_STORAGE = FileSystemStorage(path.join(_BASEDIR, "bulk-storage"))

# Static Files
STATIC_ROOT = path.join(_BASEDIR,  "static")

# Email Configuration
EMAIL_HOST = env("EMAIL_HOST", default="127.0.0.1")
EMAIL_PORT = int(env("EMAIL_PORT", default=25))
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", False)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

ROBOT_EMAIL_FROM = "Admin <info@amplepalm.com>"
RELATE_ADMIN_EMAIL_LOCALE = "en_US"
ADMINS = [
    ("Admin", "admin@example.com"),
]

# RELATE Configuration
RELATE_BASE_URL = env("RELATE_BASE_URL", default="http://localhost:8000")
RELATE_SIGN_IN_BY_EMAIL_ENABLED = (
    env.bool("RELATE_SIGN_IN_BY_EMAIL_ENABLED", default=True))
RELATE_SIGN_IN_BY_USERNAME_ENABLED = (
    env.bool("RELATE_SIGN_IN_BY_USERNAME_ENABLED", default=True))
RELATE_REGISTRATION_ENABLED = env.bool("RELATE_REGISTRATION_ENABLED", default=False)
RELATE_SIGN_IN_BY_EXAM_TICKETS_ENABLED = (
    env.bool("RELATE_SIGN_IN_BY_EXAM_TICKETS_ENABLED", default=False))

# Docker Configuration for code execution
RELATE_DOCKER_URL = env("RELATE_DOCKER_URL", default="unix://var/run/docker.sock")
RELATE_DOCKER_RUNPY_IMAGE = (
    env("RELATE_DOCKER_RUNPY_IMAGE", default="inducer/relate-runcode-python-amd64"))


# Maintenance Mode
# RELATE_MAINTENANCE_MODE = False

RELATE_SIGN_IN_BY_SAML2_ENABLED = False


RELATE_SOCIAL_AUTH_BACKENDS = (
    # See https://python-social-auth.readthedocs.io/en/latest/
    # for full list.
    # "social_core.backends.google.GoogleOAuth2",

    # CAUTION: Relate uses emails returned by the backend to match
    # users. Only use backends that return verified emails.
)

# Your Google "Client ID"
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
# Your Google "Client Secret"
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True

# When registering your OAuth2 app (and consent screen) with Google,
# specify the following authorized redirect URI:
# https://sitename.edu/social-auth/complete/google-oauth2/

# Blacklist these domains for social auth. This may be useful if there
# is a canonical way (e.g. SAML2) for members of that domain to
# sign in.
# RELATE_SOCIAL_AUTH_BLACKLIST_EMAIL_DOMAINS = {
#   "illinois.edu": "Must use SAML2 to sign in."
#   }

# }}}

# {{{ editable institutional id before verification?

# If set to False, user won't be able to edit institutional ID
# after submission. Set to False only when you trust your students
# or you don't want to verify insitutional ID they submit.
RELATE_EDITABLE_INST_ID_BEFORE_VERIFICATION = True

# If set to False, these fields will be hidden in the user profile form.
RELATE_SHOW_INST_ID_FORM = True
RELATE_SHOW_EDITOR_FORM = True

# }}}

# Whether disable "markdown.extensions.codehilite" when rendering page markdown.
# Default to True, as enable it sometimes crashes for some pages with code fences.
# For this reason, there will be a warning when the attribute is set to False when
# starting the server.
# RELATE_DISABLE_CODEHILITE_MARKDOWN_EXTENSION = True

# {{{ user full_name format

# RELATE's default full_name format is "'%s %s' % (first_name, last_name)",
# you can override it by supply a customized method/fuction, with
# "firstname" and "lastname" as its parameters, and return a string.

# For example, you can define it like this:

# <code>
#   def my_fullname_format(firstname, lastname):
#         return "%s%s" % (last_name, first_name)
# </code>

# and then uncomment the following line and enable it with:

# RELATE_USER_FULL_NAME_FORMAT_METHOD = my_fullname_format

# You can also import it from your custom module, or use a dotted path of the
# method, i.e.:
# RELATE_USER_FULL_NAME_FORMAT_METHOD = "path.to.my_fullname_format"

# }}}

# {{{ system email appellation priority

# RELATE's default email appellation of the receiver is a ordered list:
# ["first_name", "email", "username"], when first_name is not None
# (e.g, first_name = "Foo"), the email will be opened
# by "Dear Foo,". If first_name is None, then email will be used
# as appellation, so on and so forth.

# you can override the appellation priority by supply a customized list
# named relate_email_appellation_priority_list. The available
# elements include first_name, last_name, get_full_name, email and
# username.

# RELATE_EMAIL_APPELLATION_PRIORITY_LIST = [
#         "full_name", "first_name", "email", "username"]

# }}}

# {{{ custom method for masking user profile
# When a participation, for example, teaching assistant, has limited access to
# students' profile (i.e., has_permission(pperm.view_participant_masked_profile)),
# a built-in mask method (which is based on pk of user instances) is used be
# default. The mask method can be overridden by the following a custom method, with
# user as the args.

# RELATE_USER_PROFILE_MASK_METHOD = "path.tomy_method
# For example, you can define it like this:

# <code>
#   def my_mask_method(user):
#         return "User_%s" % str(user.pk + 100)
# </code>

# and then uncomment the following line and enable it with:

# RELATE_USER_PROFILE_MASK_METHOD = my_mask_method

# You can also import it from your custom module, or use a dotted path of the
# method, i.e.:
# RELATE_USER_PROFILE_MASK_METHOD = "path.to.my_mask_method"

# }}}

# {{{ extra checks

# This allow user to add customized startup checks for user-defined modules
# using Django's system checks (https://docs.djangoproject.com/en/dev/ref/checks/)
# For example, define a `my_check_func in `my_module` with
# <code>
#   def my_check_func(app_configs, **kwargs):
#         return [list of error]
# </code>
# The configuration should be
# RELATE_STARTUP_CHECKS_EXTRA = ["my_module.my_check_func"]
# i.e., Each item should be the path to an importable check function.
# RELATE_STARTUP_CHECKS_EXTRA = []

# }}}

# {{{ overriding built-in templates
# Uncomment the following to enable templates overriding. It should be configured
# as a list/tuple of path(s).
# For example, if you the templates are in a folder named "my_templates" in the
# root dir of the project, with base.html (project template), course_base.html,
# and sign-in-email.txt (app templates) etc., are the templates you want to
# override, the structure of the files should look like:
#    ...
#    relate/
#    local_settings.py
#    my_templates/
#        base.html
#        ...
#        course/
#            course_base.html
#            sign-in-email.txt
#                ...
#

import os.path


RELATE_OVERRIDE_TEMPLATES_DIRS = [
    os.path.join(os.path.dirname(__file__), "templates_override"),
    # os.path.join(os.path.dirname(__file__), "my_other_templates")
]

# }}}

# {{{ docker

# A string containing the image ID of the docker image to be used to run
# student Python code. Docker should download the image on first run.
# RELATE_DOCKER_RUNPY_IMAGE = "inducer/relate-runcode-python-amd64"

# A URL pointing to the Docker command interface which RELATE should use
# to spawn containers for student code.
# RELATE_DOCKER_URL = "unix://var/run/docker.sock"
# for podman
# RELATE_DOCKER_URL = f"unix://run/user/{os.getuid()}/podman/podman.sock"

RELATE_DOCKER_TLS_CONFIG = None

# Example setup for targeting remote Docker instances
# with TLS authentication:

# RELATE_DOCKER_URL = "https://relate.cs.illinois.edu:2375"
#
# import os.path
# pki_base_dir = os.path.dirname(__file__)
#
# import docker.tls
# RELATE_DOCKER_TLS_CONFIG = docker.tls.TLSConfig(
#     client_cert=(
#         os.path.join(pki_base_dir, "client-cert.pem"),
#         os.path.join(pki_base_dir, "client-key.pem"),
#         ),
#     ca_cert=os.path.join(pki_base_dir, "ca.pem"),
#     verify=True)

# }}}

# {{{ maintenance and announcements

RELATE_MAINTENANCE_MODE = False

RELATE_MAINTENANCE_MODE_EXCEPTIONS = []
# RELATE_MAINTENANCE_MODE_EXCEPTIONS = ["192.168.1.0/24"]

# May be set to a string to set a sitewide announcement visible on every page.
RELATE_SITE_ANNOUNCEMENT = None

# }}}

# Uncomment this to enable i18n, change "en-us" to locale name your language.
# Make sure you have generated, translate and compile the message file of your
# language. If commented, RELATE will use default language "en-us".

# LANGUAGE_CODE = "en-us"

# You can (and it's recommended to) override Django's built-in LANGUAGES settings
# if you want to filter languages allowed for course-specific languages.
# The format of languages should be a list/tuple of 2-tuples:
# (language_code, language_description). If there are entries with the same
# language_code, language_description will be using the one which comes latest.
# .If LANGUAGES is not configured, django.conf.global_settings.LANGUAGES will be
# used.
# Note: make sure LANGUAGE_CODE you used is also in LANGUAGES, if it is not
# the default "en-us". Otherwise translation of that language will not work.

# LANGUAGES = [
#     ("en", "English"),
#     ("zh-hans", "Simplified Chinese"),
#     ("de", "German"),
# ]

# {{{ exams and testing

# This may also be a callable that receives a local-timezone datetime and returns
# an equivalent dictionary.
#
# def RELATE_FACILITIES(now_datetime):
#     from relate.utils import localize_datetime
#     from datetime import datetime
#
#     if (now_datetime >= localize_datetime(datetime(2016, 5, 5, 0, 0))
#             and now_datetime < localize_datetime(datetime(2016, 5, 6, 0, 0))):
#         ip_ranges = [
#             "127.0.0.1/32",
#             "192.168.77.0/24",
#             ]
#     else:
#         ip_ranges = []
#
#     return {
#         "test_center": {
#             "ip_ranges": ip_ranges,
#             "exams_only": True,
#             },
#     }
#
#    # Automatically get denied facilities from PrairieTest
#    result = {}
#
#    from prairietest.utils import denied_ip_networks_at
#    pt_facilities_networks = denied_ip_networks_at(now_datetime)
#    for (course_id, facility_name), networks in pt_facilities_networks.items():
#        fdata = result.setdefault(facility_name, {})
#        fdata["exams_only"] = True
#        fdata["ip_ranges"] = [*fdata.get("ip_ranges", []), *networks]
#    return result


RELATE_FACILITIES = {
    "test_center": {
        "ip_ranges": [
            "192.168.192.0/24",
        ],
        "exams_only": False,
    },
}

# For how many minutes is an exam ticket still usable for login after its first
# use?
RELATE_TICKET_MINUTES_VALID_AFTER_USE = 12 * 60

# }}}


# vim: filetype=python:foldmethod=marker
