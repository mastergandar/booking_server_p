from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

validate_phone_simple = RegexValidator(
    regex=r'^\d{2,16}$',
    message="Enter the correct phone number (2-16 digits)"
)


def validate_avatar_max_size(value):
    file_size = value.size
    file_size_limit_mb = 10
    limit_kb = file_size_limit_mb * 1024 * 1024
    if file_size > limit_kb:
        raise ValidationError("Maximum file size %s MB" % file_size_limit_mb)


def validate_images_file_max_size(value):
    file_size = value.size
    file_size_limit_mb = 10
    limit_kb = file_size_limit_mb * 1024 * 1024
    if file_size > limit_kb:
        raise ValidationError("Maximum file size %s MB" % file_size_limit_mb)


class CustomPasswordValidator:

    SPECIAL_CHARS = "~!@#$%^&*_-+=`|(){}[]:;\"'<>,.?/"

    def validate(self, password, user=None):

        import string

        svalid = False
        for c in list(self.SPECIAL_CHARS):
            if c in password:
                svalid = True
                break

        if not svalid:
            raise ValidationError(
                _(f"This password must contain at least one of the characters: {self.SPECIAL_CHARS}"),
                code='password_no_special_chars'
            )

        string.digits

        uvalid = False
        for c in list(string.ascii_uppercase):
            if c in password:
                uvalid = True
                break

        if not uvalid:
            raise ValidationError(
                _(f"This password must contain at least one uppercase letter"),
                code='password_no_uppercase_letters'
            )

        dvalid = False
        for c in list(string.digits):
            if c in password:
                dvalid = True
                break

        if not dvalid:
            raise ValidationError(
                _(f"This password must contain at least one digit"),
                code='password_no_digits'
            )

    def get_help_text(self):
        return _(
            f"Your password must contain any of the special characters: {self.SPECIAL_CHARS}"
        )
