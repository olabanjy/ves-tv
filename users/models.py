from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_init, pre_save
from django.template.loader import render_to_string
from django.dispatch import receiver
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum
from allauth.account.signals import user_signed_up, user_logged_in
import random, string
from datetime import timedelta, date, datetime


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
    phone = models.CharField(
        max_length=40,
        null=True,
        blank=True,
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
    # productID = models.CharField(blank=True, null=True, max_length=200)
    # userID = models.CharField(blank=True, null=True, max_length=200)
    # traceUniqueID = models.CharField(blank=True, null=True, max_length=200)
    # updateType = models.CharField(blank=True, null=True, max_length=200)
    # updateTime = models.CharField(blank=True, null=True, max_length=200)
    # updateDesc = models.CharField(blank=True, null=True, max_length=200)
    # effectiveTime = models.CharField(blank=True, null=True, max_length=200)
    # expiryTime = models.CharField(blank=True, null=True, max_length=200)
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
