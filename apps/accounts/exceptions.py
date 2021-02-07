from django.utils.translation import ugettext_lazy as _
class AccountsError(Exception):
    """Generic Accounts error"""

    default_message = None

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)


class UserNotFoundError(AccountsError):
    default_message = _("No such user found!")

class PasswordError(AccountsError):
    default_message = _("Password Wrong!")