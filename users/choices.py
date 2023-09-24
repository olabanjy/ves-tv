from enum import unique

from core.enum import DocEnum
from django.utils.translation import gettext_lazy as _


@unique
class Roles(DocEnum):
    """
    User Roles
    """

    SuperAdmin = "Admin", "Super Admin user"
    Vendor = "Vendor", "Vendor Administrator User"
    SystemAdmin = "SystemAdmin", "System Administrator"


_readable_roles = {
    Roles.SuperAdmin.value: _("SuperAdmin"),
    Roles.Vendor.value: _("Vendor"),
    Roles.SystemAdmin.value: _("SystemAdmin"),
}


ROLE_CHOICES = [(d.value, _readable_roles[d.value]) for d in Roles]