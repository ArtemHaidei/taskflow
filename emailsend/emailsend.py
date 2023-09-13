import jwt

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from users.utils import get_user_by_pk


class EmailSender:
    @staticmethod
    def send(subject, message, from_email=None, recipient_list=None):
        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,  # Change to True if you do not want errors to be displayed in the console
            )
            return message
        except Exception as e:
            # TODO: Add logging here
            print(str(e))
            return False

    @staticmethod
    def create_jwt_token(user):
        payload = {
            'email': user.email,
            'exp': timezone.now() + timedelta(hours=settings.EMAIL_TOKEN_EXPIRE_TIME),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def send_verify_email(self, pk):
        user = get_user_by_pk(pk=pk)

        token = self.create_jwt_token(user)
        verify_url = reverse('user-verify-email') + f'?token={token}'

        subject = f"Please, verify your email address"
        message = (f'Hello, {user.first_name} {user.last_name}!\n'
                   f'Please verify your email address clicking the link below:\n\n'
                   f'http://{settings.ALLOWED_HOSTS[0]}{verify_url} \n\n'
                   'Best regards,\n'
                   'TaskFlow Team\n'
                   )

        return self.send(subject=subject, message=message, recipient_list=[user.email])
