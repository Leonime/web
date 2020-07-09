import logging

from django.conf import settings
from rest_framework import status
from sendgrid import Mail, SendGridAPIClient

from core.exceptions import EmailNotSent

logger = logging.getLogger(__name__)


class SendEmail:
    def __init__(self, **kwargs):
        self.from_email = kwargs['from_email'] if 'from_email' in kwargs else 'no-reply@codeshepherds.com'
        self.to_emails = kwargs['to_emails'] if 'to_emails' in kwargs else ''
        self.subject = kwargs['subject'] if 'subject' in kwargs else ''
        self.html_content = kwargs['html_content'] if 'html_content' in kwargs else ''

    def send(self, from_email=None, to_emails=None, subject=None, html_content=None):
        email = Mail(
            from_email=self.from_email if self.from_email is not None else from_email,
            to_emails=self.to_emails if self.to_emails is not None else to_emails,
            subject=self.subject if self.subject is not None else subject,
            html_content=self.html_content if self.html_content is not None else html_content)
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(email)
            if response.status_code != status.HTTP_202_ACCEPTED:
                raise EmailNotSent
            return response.status_code
        except EmailNotSent as e:
            logger.exception(e)
        except Exception as e:
            logger.exception(e)
