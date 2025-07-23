
from django.core.mail import send_mail
from django.conf import settings

def send_password_email(to_email, full_name, password):
    subject = 'Email Verification'
    message = (
        f'Hi {full_name},\n\n'
        'Thank you for registering. Wait for admin verification email.\n'
        f'Your password is: {password}\n\n'
        'Best regards,\nTethics Electrics Group'
    )
    from_email = settings.EMAIL_HOST_USER

    try:
        send_mail(subject, message, from_email, [to_email], fail_silently=False)
        print('Email sent successfully.')
    except Exception as e:
        print(f'Error sending email: {e}')


def send_verification_email(to_email, full_name):
    subject = 'Email Verification'
    message = (
        f'Hi {full_name},\n\n'
        'Thank you for registering. Admin has verified you.\n'
        'Welcome on board\n\n'
        'Best regards,\nTethics Electrics Group'
    )
    from_email = settings.EMAIL_HOST_USER

    try:
        send_mail(subject, message, from_email, [to_email], fail_silently=False)
        print('Email sent successfully.')
    except Exception as e:
        print(f'Error sending email: {e}')