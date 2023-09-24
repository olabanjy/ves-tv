from enum import unique

from .enum import DocEnum
from django.utils.translation import gettext_lazy as _


@unique
class VerificationStatus(DocEnum):
    """
    Provider Payment Channels.
    """

    Uploading = "Uploading", "Course content still being uploaded"
    Submitted = "Submitted", "Course content submitted"
    InReview = "In Review", "Course still in review"
    Approved = "Approved", "Course verification approved"
    Rejected = "Rejected", "Course verification rejected"
    Removed = "Removed", "Course removed by admin"


_readable_task_status = {
    VerificationStatus.Uploading.value: _("Uploading"),
    VerificationStatus.Submitted.value: _("Submitted"),
    VerificationStatus.InReview.value: _("In Review"),
    VerificationStatus.Rejected.value: _("Rejected"),
    VerificationStatus.Approved.value: _("Approved"),
    VerificationStatus.Removed.value: _("Removed"),
}


VERIFICATION_CHOICES = [
    (d.value, _readable_task_status[d.value]) for d in VerificationStatus
]

