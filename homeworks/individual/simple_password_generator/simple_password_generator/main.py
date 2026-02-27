## main.py

"""A simple, secure, and extensible command-line password generator.

This script provides a CLI for generating random passwords with options for
uppercase letters, numbers, and special characters. It supports copying the
generated password to the clipboard using pyperclip.

Author: Alex
"""

import argparse
import string
import sys

import pyperclip
import secrets


class PasswordGenerator:
    """Generates secure random passwords with configurable character sets."""

    def __init__(self, use_uppercase: bool = True, use_numbers: bool = True, use_special: bool = True):
        """Initializes the PasswordGenerator with character set options.

        Args:
            use_uppercase (bool): Include uppercase letters if True.
            use_numbers (bool): Include digits if True.
            use_special (bool): Include special characters if True.
        """
        self._use_uppercase = use_uppercase
        self._use_numbers = use_numbers
        self._use_special = use_special

        self._charset = self._build_charset()

    def _build_charset(self) -> str:
        """Builds the character set based on the selected options.

        Returns:
            str: The string of allowed characters.
        """
        charset = list(string.ascii_lowercase)
        if self._use_uppercase:
            charset.extend(string.ascii_uppercase)
        if self._use_numbers:
            charset.extend(string.digits)
        if self._use_special:
            charset.extend(string.punctuation)
        return ''.join(charset)

    def generate(self, length: int) -> str:
        """Generates a secure random password.

        Args:
            length (int): The desired password length.

        Returns:
            str: The generated password.

        Raises:
            ValueError: If the character set is empty or length is invalid.
        """
        if not self._charset:
            raise ValueError("Character set is empty. Enable at least one character type.")
        if length < 1:
            raise ValueError("Password length must be at least 1.")

        return ''.join(secrets.choice(self._charset) for _ in range(length))


class CLI:
    """Handles command-line interface, argument parsing, and user interaction."""

    DEFAULT_LENGTH = 12

    def parse_args(self) -> dict:
        """Parses command-line arguments.

        Returns:
            dict: Parsed arguments as a dictionary.
        """
        parser = argparse.ArgumentParser(
            description="Generate a secure random password.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            '-l', '--length',
            type=int,
            default=self.DEFAULT_LENGTH,
            help='Length of the password.'
        )
        parser.add_argument(
            '--no-uppercase',
            action='store_true',
            help='Exclude uppercase letters from the password.'
        )
        parser.add_argument(
            '--no-numbers',
            action='store_true',
            help='Exclude numbers from the password.'
        )
        parser.add_argument(
            '--no-special',
            action='store_true',
            help='Exclude special characters from the password.'
        )
        parser.add_argument(
            '-c', '--copy',
            action='store_true',
            help='Copy the generated password to the clipboard.'
        )

        args = parser.parse_args()
        return {
            'length': args.length,
            'use_uppercase': not args.no_uppercase,
            'use_numbers': not args.no_numbers,
            'use_special': not args.no_special,
            'copy': args.copy
        }

    def display_password(self, password: str) -> None:
        """Displays the generated password to the user.

        Args:
            password (str): The generated password.
        """
        print("\nGenerated password:\n")
        print(password)
        print()

    def display_error(self, message: str) -> None:
        """Displays an error message to the user.

        Args:
            message (str): The error message.
        """
        print(f"Error: {message}", file=sys.stderr)

    def copy_to_clipboard(self, password: str) -> None:
        """Copies the password to the system clipboard.

        Args:
            password (str): The password to copy.
        """
        try:
            pyperclip.copy(password)
            print("Password copied to clipboard.")
        except pyperclip.PyperclipException as exc:
            self.display_error(f"Failed to copy to clipboard: {exc}")

    def run(self) -> None:
        """Runs the CLI application."""
        args = self.parse_args()

        # Validate password length
        if args['length'] < 1:
            self.display_error("Password length must be at least 1.")
            sys.exit(1)

        # Validate at least one character set is enabled
        if not (args['use_uppercase'] or args['use_numbers'] or args['use_special']):
            # Only lowercase is left, which is always included
            pass  # This is allowed

        try:
            generator = PasswordGenerator(
                use_uppercase=args['use_uppercase'],
                use_numbers=args['use_numbers'],
                use_special=args['use_special']
            )
            password = generator.generate(args['length'])
        except ValueError as exc:
            self.display_error(str(exc))
            sys.exit(1)

        self.display_password(password)

        if args['copy']:
            self.copy_to_clipboard(password)


if __name__ == "__main__":
    cli = CLI()
    cli.run()
