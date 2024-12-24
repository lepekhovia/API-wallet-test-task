import decimal
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Wallet(models.Model):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
    OPERATION_TYPE_CHOICES = [
        (DEPOSIT, _('Deposit')),
        (WITHDRAW, _('Withdraw')),
    ]

    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True, verbose_name=_("UUID"))
    owner = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name=_("Owner"), related_name="wallets")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, verbose_name=_("Balance"))
    operation_type = models.CharField(max_length=32, verbose_name=_("Operation type"), choices=OPERATION_TYPE_CHOICES)  # - in the current task - not a necessary field, but can be useful for storing the history of operations

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")

    def __str__(self) -> str:
        return f"wallet {self.id} of {self.owner.id}"

    async def change_balance(self, amount: decimal.Decimal, type_operation: str) -> 'Wallet':
        if type_operation == self.DEPOSIT:
            self.balance += amount
            await self.asave(update_fields=['balance'])
            return self
        self.balance -= amount
        await self.asave(update_fields=['balance'])
        return self
