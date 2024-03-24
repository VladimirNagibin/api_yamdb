from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_HOST_USER


def confirm_send_mail(email, confirmation_code):
    """Функция отправляющая на почту код потверждения."""
    send_mail(
        subject='YaMDB Registration',
        message=('Вы успешно зарегестрированы. '
                 f'Ваш код подтверждения: {confirmation_code}'),
        from_email=EMAIL_HOST_USER,
        recipient_list=[email, ],
        fail_silently=True
    )
