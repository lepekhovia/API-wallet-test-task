import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Wallet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True, verbose_name=_("UUID"))
    owner = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name=_("Owner"), related_name="wallets")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, verbose_name=_("Balance"))

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")

    def __str__(self):
        return f"wallet {self.id} of {self.owner.id}"
