class Error(Exception):
    """Base class for other exceptions"""
    pass


class EmailNotSent(Error):
    """Raised when something failed during email delivery."""
    pass
