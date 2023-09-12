from django.core.mail import send_mail
from django.conf import settings


class EmailSender:
    def __init__(self, subject, message, from_email=None, recipient_list=None):
        self.subject = subject
        self.message = message
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL
        self.recipient_list = recipient_list or []

    def send(self):
        try:
            send_mail(
                self.subject,
                self.message,
                self.from_email,
                self.recipient_list,
                fail_silently=False,  # Change to True if you do not want errors to be displayed in the console
            )
            return True
        except Exception as e:
            # TODO: Add logging here
            print(str(e))  # Change to logger.error(str(e)) if you use logging
            return False


