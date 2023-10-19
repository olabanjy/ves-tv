from django.db import models

from django.utils import timezone
from users.models import Profile

from django.db.models.signals import post_save
# Create your models here.

class Contracts(models.Model):
    vendor = models.OneToOneField(Profile, on_delete=models.CASCADE)
    contract_file = models.FileField(upload_to='vendor/contracts', blank=True, null=True)
    signed = models.BooleanField(default=False)
    resubmitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)



def contract_receiver(sender, instance, created, *args, **kwargs):
    if created:
        contract = Contracts.objects.get_or_create(vendor=instance)

    contract, created = Contracts.objects.get_or_create(vendor=instance)

post_save.connect(contract_receiver, sender=Profile)


class BankAccount(models.Model):
    vendor = models.OneToOneField(
        Profile, on_delete=models.CASCADE,
    )
    account_number = models.CharField(max_length=11, blank=True, null=True)
    account_name = models.CharField(max_length=100, blank=True, null=True)
    account_bank = models.CharField(max_length=100, blank=True, null=True)
    account_bank_code = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.vendor.user.email