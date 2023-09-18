from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

def email_validation(value):
    """
        Validation of emailfield in registration form
    """
    if not "@seznam.cz" in value:
        raise ValidationError(_("Email musí obsahovat '@seznam.cz'"))


