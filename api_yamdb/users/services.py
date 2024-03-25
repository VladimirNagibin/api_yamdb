from django.core.mail import send_mail

from django.conf import settings


def confirm_send_mail(email, confirmation_code):
    """Функция отправляющая на почту код потверждения."""
    send_mail(
        subject='YaMDB Registration',
        message=('Вы успешно зарегестрированы. '
                 f'Ваш код подтверждения: {confirmation_code}'),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email, ],
        fail_silently=True
    )
