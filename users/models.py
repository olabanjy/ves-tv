from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from django.utils import timezone


import random, string


from django.utils.translation import gettext_lazy as _

from . import choices


SUB_STATUS = (
    ("active", "Active"),
    ("inactive", "Inactive"),
    ("no_sub", "No Subscribtion"),
)


TEST_PHASE = (
    ("live_prod", "Live Prod"),
    ("phase_one", "Phase One"),
    ("phase_two", "Phase Two"),
    ("beta", "Beta"),
)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_code = models.CharField(max_length=200)
    first_name = models.CharField(blank=True, null=True, max_length=200)
    last_name = models.CharField(blank=True, null=True, max_length=200)
    company_name  = models.CharField(blank=True, null=True, max_length=250)
    company_banner  = models.ImageField(upload_to="vendor/banner/", blank=True)
    onboarded = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    state = models.CharField(max_length=200, blank=True, null=True)
    nationality = models.CharField(max_length=200, blank=True, null=True)
    test_phase = models.CharField(
        max_length=200, choices=TEST_PHASE, default="live_prod"
    )
    sub_status = models.CharField(max_length=200, choices=SUB_STATUS, default="no_sub")
    created_at = models.DateTimeField(default=timezone.now)

    role = models.TextField(
        choices=choices.ROLE_CHOICES,
        default=choices.Roles.Vendor.value,
        verbose_name=_("role"),
    )

    def __str__(self):
        return self.user.username

    @property
    def last_login(self, *args, **kwargs):
        the_last_login = self.user.last_login
        if the_last_login:
            user_last_login = the_last_login.strftime("%Y-%m-%d %H:%M")
            return user_last_login
        return None


def profile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.get_or_create(user=instance)

    profile, created = Profile.objects.get_or_create(user=instance)
    if profile.user_code is None or profile.user_code == "":
        profile.user_code = str(
            "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        )
        profile.phone = instance.username
        profile.save()


post_save.connect(profile_receiver, sender=settings.AUTH_USER_MODEL)


class WebhookBackup(models.Model):
    req_body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.created_at}"


class Subscribtion(models.Model):
    user = models.ForeignKey("Profile", on_delete=models.CASCADE, blank=True, null=True)
    sub_active = models.BooleanField(default=False)
    starts_date = models.DateTimeField(blank=True, null=True)
    ends_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.user.username}"


class UserProfile(models.Model):
    phone = models.CharField(
        max_length=40,
        null=True,
    )
    first_name = models.CharField(blank=True, null=True, max_length=200)
    last_name = models.CharField(blank=True, null=True, max_length=200)
    dob = models.DateField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    nationality = models.CharField(max_length=200, blank=True, null=True)
    test_phase = models.CharField(
        max_length=200, choices=TEST_PHASE, default="live_prod"
    )
    sub_status = models.CharField(max_length=200, choices=SUB_STATUS, default="no_sub")
    created_at = models.DateTimeField(default=timezone.now)


class UserSubscribtion(models.Model):
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE, null=True)
    sub_active = models.BooleanField(default=False)
    starts_date = models.DateTimeField(blank=True, null=True)
    ends_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}"


class CampaignNotificationBackup(models.Model):
    req_body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.created_at}"
