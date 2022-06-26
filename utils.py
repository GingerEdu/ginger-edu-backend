from django.core.mail import EmailMultiAlternatives


def send_mail(to, title='', mail_body='', from_email=""):
    if isinstance(to, str):
        receivers = [to]
    else:
        receivers = [email for email in to if email]
    email = EmailMultiAlternatives(title, mail_body, to=receivers)
    email.attach_alternative(mail_body, 'text/html')
    email.send()
