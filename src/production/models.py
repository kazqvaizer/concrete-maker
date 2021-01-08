from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel, models


class Batch(TimestampedModel):
    recipe = models.ForeignKey(
        "lab.recipe", verbose_name=_("Recipe"), on_delete=models.PROTECT
    )
    volume = models.DecimalField(
        _("Volume, m3"), max_digits=10, decimal_places=3, default=0
    )

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
        verbose_name = _("Batch")
        verbose_name_plural = _("Batches")

    def __str__(self):
        return f"{self.recipe.name}: {self.volume} м3"
