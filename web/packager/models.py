from django.db import models
from django.utils.translation import gettext_lazy as _


class MCMod(models.Model):
    class ModType(models.TextChoices):
        MODS = 'md', _('Mod')
        RESOURCE_PACK = 'rp', _('Resource Pack')
        FORGE = 'fg', _('Forge')

    slug = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    zip_mod = models.BooleanField()
    mod_type = models.CharField(max_length=2, choices=ModType.choices, default=ModType.MODS)

    def __str__(self):
        return self.file_name
