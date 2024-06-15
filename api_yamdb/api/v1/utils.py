from django.core.mail import EmailMessage


def send_confirmation_code_email(user, confirmation_code):
    email = EmailMessage(
        'Ваш код подтверждения. YAMDB',
        """
        Добрый день, {user}!
        Ваш код: {confirmation_code}.
        Пожалуйста, не сообщайте его никому.
        """.format(user=user, confirmation_code=confirmation_code),
        to=[user.email]
    )
    email.send()
