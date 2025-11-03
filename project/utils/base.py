from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    updated_at = models.DateTimeField(
        auto_now=True, blank=False, verbose_name=_("updated at"), editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        verbose_name=_("created at"),
        editable=False,
    )

    class Meta:
        abstract = True