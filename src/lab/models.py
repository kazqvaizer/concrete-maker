from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel, models


class Recipe(TimestampedModel):
    name = models.CharField(_("Name"), max_length=255, db_index=True, unique=True)

    cement_weight = models.DecimalField(
        _("Cement, kg"), max_digits=10, decimal_places=3, default=0
    )
    sand_weight = models.DecimalField(
        _("Sand, kg"), max_digits=10, decimal_places=3, default=0
    )
    gravel_weight = models.DecimalField(
        _("Gravel, kg"), max_digits=10, decimal_places=3, default=0
    )
    water_weight = models.DecimalField(
        _("Water, kg"), max_digits=10, decimal_places=3, default=0
    )
    admixture_weight = models.DecimalField(
        _("Admixture, kg"), max_digits=10, decimal_places=3, default=0
    )

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")

    def __str__(self):
        return self.name
