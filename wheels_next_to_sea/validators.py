import re

from django.core.exceptions import ValidationError
from django.utils.translation import ngettext as _
from django.utils.translation import gettext

class UppercaseValidator:
    """
    Validates whether the password contains at least min_uppercase uppercase characters.
    """

    def __init__(self, min_uppercase=1):
        """Initializes the validator.

        Args:
            min_uppercase (int, optional): Minimum number of uppercase characters to
                validate password against. Defaults to 1.
        """
        self.min_uppercase = min_uppercase

    def validate(self, password, user=None):
        """
        Validates whether the password contains at least min_uppercase uppercase characters.

        Args:
            password (str): The password to validate.
            user (User): The user to validate the password for. (unused)

        Raises:
            ValidationError: Password must contain at least {self.min_uppercase} uppercase
                character(s).
        """
        if sum(c.isupper() for c in password) < self.min_uppercase:
            raise ValidationError(
                _(
                    f"Password must contain at least {self.min_uppercase} uppercase character.",
                    f"Password must contain at least {self.min_uppercase} uppercase characters.",
                    self.min_uppercase,
                ),
                code="password_too_weak",
                params={"min_uppercase": self.min_uppercase},
            )

    def get_help_text(self):
        """
        Get the help text for the validator.
        """
        return _(
            f"Your password must contain at least {self.min_uppercase} uppercase character.",
            f"Your password must contain at least {self.min_uppercase} uppercase characters.",
            self.min_uppercase,
        ) % {"min_uppercase": self.min_uppercase}


class ContainsLowercaseValidator:
    """
    Validates whether the password contains at least min_lowercase lowercase characters.
    """

    def __init__(self, min_lowercase=1):
        """Initializes the validator.

        Args:
            min_lowercase (int, optional): Minimum number of lowercase characters to
                validate password against. Defaults to 1.
        """
        self.min_lowercase = min_lowercase

    def validate(self, password, user=None):
        """
        Validates whether the password contains at least min_lowercase lowercase characters.

        Args:
            password (str): The password to validate.
            user (User): The user to validate the password for. (unused)

        Raises:
            ValidationError: Password must contain at least {self.min_lowercase} lowercase
                character(s).
        """
        if sum(c.islower() for c in password) < self.min_lowercase:
            raise ValidationError(
                _(
                    f"Password must contain at least {self.min_lowercase} lowercase character.",
                    f"Password must contain at least {self.min_lowercase} lowercase characters.",
                    self.min_lowercase,
                ),
                code="password_too_weak",
                params={"min_lowercase": self.min_lowercase},
            )

    def get_help_text(self):
        """
        Get the help text for the validator.
        """
        return _(
            f"Your password must contain at least {self.min_lowercase} lowercase character.",
            f"Your password must contain at least {self.min_lowercase} lowercase characters.",
            self.min_lowercase,
        ) % {"min_lowercase": self.min_lowercase}


class SpecialCharacterValidator:
    """
    Validates whether the password contains at least min_characters special characters.
    """

    def __init__(self, min_characters=1):
        """Initializes the validator.

        Args:
            min_characters (int, optional): Minimum number of special characters to
                validate password against. Defaults to 1.
        """
        self.min_characters = min_characters
        self.characters = set(" !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")

    def validate(self, password, user=None):
        """
        Validates whether the password contains at least min_characters special characters.

        Args:
            password (str): The password to validate.
            user (User): The user to validate the password for. (unused)

        Raises:
            ValidationError: Password must contain at least {self.min_characters} special
                character(s).
        """
        if sum(c in self.characters for c in password) < self.min_characters:
            raise ValidationError(
                _(
                    f"Password must contain at least {self.min_characters} special character.",
                    f"Password must contain at least {self.min_characters} special characters.",
                    self.min_characters,
                ),
                code="password_too_weak",
                params={"min_characters": self.min_characters},
            )

    def get_help_text(self):
        """
        Get the help text for the validator.
        """
        return _(
            f"Your password must contain at least {self.min_characters} special character.",
            f"Your password must contain at least {self.min_characters} special characters.",
            self.min_characters,
        ) % {"min_characters": self.min_characters}