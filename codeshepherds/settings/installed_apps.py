##################
# Installed apps #
##################
PRIORITY_APPS = [
    'channels',
    'whitenoise.runserver_nostatic',
]

################
# Default apps #
################
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

#####################
# Third party apps. #
#####################
THIRD_PARTY_APPS = [
    'bootstrap4',
    'django_icons',
    'rest_framework',
    'widget_tweaks',
    'corsheaders',
    'crispy_forms',
    'thumbnails',
    'django_cleanup.apps.CleanupConfig',
    'simple_history',
    'admin_honeypot',
]

##############
# Local Apps #
##############
LOCAL_APPS = [
    'accounts.apps.AccountsConfig',
    'analytics.apps.AnalyticsConfig',
    'base.apps.BaseConfig',
    'chat.apps.ChatConfig',
    'chirp.apps.ChirpConfig',
    'cookbook.apps.CookbookConfig',
    'frontend.apps.FrontendConfig',
    'history.apps.HistoryConfig',
    'home.apps.HomeConfig',
    'party.apps.PartyConfig',
    'profiles.apps.ProfilesConfig',
    'shortener.apps.ShortenerConfig',
    'testing.apps.TestingConfig',
    'thumbnailer.apps.ThumbnailerConfig',
]

##########################
# Application definition #
##########################
INSTALLED_APPS = PRIORITY_APPS + DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS
