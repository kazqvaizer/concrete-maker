from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LabConfig(AppConfig):
    name = "lab"
    verbose_name = _("Lab")
