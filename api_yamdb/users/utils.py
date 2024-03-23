
from django.core.mail import send_mail


def confirm_send_mail(email, confirmation_code):
    """Функция отправляющая на почту код потверждения."""
    send_mail(
        subject='YaMDB Registration',
        message=('Вы успешно зарегестрированы. '
                 f'Ваш код подтверждения: {confirmation_code}'),
        from_email='YaMDB@yandex.ru',
        recipient_list=[email, ],
        fail_silently=True
    )
