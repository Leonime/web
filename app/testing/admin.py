from django.contrib import admin

from testing.forms import TestingAdmin
from testing.models import Testing

admin.site.register(Testing, TestingAdmin)
