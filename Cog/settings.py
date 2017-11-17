"""
Django settings for Cog project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
# from decouple import config
import dj_database_url
import logger
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# print(STATICFILES_DIRS)
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Dashboard',
    'pipeline',
    'djangobower',
    'crispy_forms',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Cog.middleware.LogUserDetailsMiddleware',
]

ROOT_URLCONF = 'Cog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/Dashboard/Extensions/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Cog.wsgi.application'

LOGIN_URL = '/login/'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

BOWER_COMPONENTS_ROOT = "Dashboard/static"

BOWER_PATH = '/usr/local/bin/bower'

BOWER_INSTALLED_APPS = (
    "https://github.com/weareoutman/clockpicker.git",
    "bootstrap#^3.3.7",
    "jquery#^3.2.1",
    "d3#^4.10.0",
    "font-awesome",
    "eonasdan-bootstrap-datetimepicker#latest",
    'moment',
    'jquery-ui',
)

STATIC_URL = '/static/'

PIPELINE = {
    'STYLESHEETS': {
        'preload_css': {
            'source_filenames': (
                'bower_components/please-wait/build/please-wait.css',
            ),
            'output_filename': 'css/preload.min.css',
            'variant': 'datauri',
        },
        'libraries': {
            'source_filenames': (
                'bower_components/bootstrap/dist/css/bootstrap.css',
                'bower_components/clockpicker/dist/bootstrap-clockpicker.css',
                'bower_components/font-awesome/css/font-awesome.min.css',
                'bower_components/eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.min.css',
                'bower_components/jquery-ui/themes/base/jquery-ui.min.css',
                'css/Dashboard.css',
            ),
            # Compress passed libraries and have
            # the output in`css/libs.min.css`.
            'output_filename': 'css/libs.min.css',
            'variant': 'datauri',
        }
    },
    'JAVASCRIPT': {
        'preload_js': {
            'source_filenames': (
                'bower_components/please-wait/build/please-wait.js',
            ),
            # Compress all passed files into `js/libs.min.js`.
            'output_filename': 'js/preload.min.js',
        },
        'universal_libraries': {
            'source_filenames': (
                'bower_components/jquery/dist/jquery.js',
                'bower_components/bootstrap/dist/js/bootstrap.js',
                'bower_components/moment/min/moment.min.js',
                'bower_components/clockpicker/dist/bootstrap-clockpicker.js',
                'bower_components/d3/d3.min.js',
                'bower_components/eonasdan-bootstrap-datetimepicker/build/js/bootstrap-datetimepicker.min.js',
                'js/jquery.easing.min.js',
                'bower_components/jquery-ui/jquery-ui.min.js',
                'js/ScrollingNav.js',
            ),
            # Compress all passed files into `js/libs.min.js`.
            'output_filename': 'js/preload.min.js',
        },
        'libraries': {
            'source_filenames': (
                'bower_components/jquery/dist/jquery.js',
                'bower_components/bootstrap/dist/js/bootstrap.js',
                'bower_components/moment/min/moment.min.js',
                'bower_components/clockpicker/dist/bootstrap-clockpicker.js',
                'bower_components/d3/d3.min.js',
                'bower_components/eonasdan-bootstrap-datetimepicker/build/js/bootstrap-datetimepicker.min.js',
                'js/jquery.easing.min.js',
                'bower_components/jquery-ui/jquery-ui.min.js',
                'js/ScrollingNav.js',
                'js/Job.js',
                'js/Task.js',
                'js/Event.js',
                'js/JobHandler.js',
                'js/Utils.js',
                'js/Ajax_Queries.js',
                'js/CenterClockGraph.js',
                'js/Notifications.js',
                'js/Dashboard.js',
                'js/SideBar.js',
                'js/Waiting_dialog.js',
                'js/ExtensionHandler.js',
                'js/Extensions.js',
            ),
            # Compress all passed files into `js/libs.min.js`.
            'output_filename': 'js/libs.min.js',
        }
    }
}
PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
# STATICFILES_STORAGE = 'django_pipeline_forgiving.storages.PipelineForgivingStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

# SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = 'kufx5ij(o*t)z^1(p1%mw_qim2#k+o)070xno8xuhgw39gig$^'
DEBUG = False
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
