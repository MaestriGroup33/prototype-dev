from django.core.mail import send_mail


def send_email(subject: str, message: str, recipient: str):
    send_mail(
        subject,
        message,
        "ti@maestri.group",
        [
            recipient,
        ],
        fail_silently=False,
    )
