from datetime import timedelta, datetime

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from backend_api.celery import app
from members.managers.custom_manager import generate_activation_link
from members.settings import CONFIRM_TITLE, SENDER


@app.task
def dispatch_mail(user_pk):
    user = get_user_model().objects.get(pk=user_pk)
    title = CONFIRM_TITLE
    data = {
        'context': {
            'message': 'please click the link to activate your account',
            'activation_link': generate_activation_link(user)
        }
    }
    html_content = render_to_string('base_template.html', data)
    text_content = strip_tags(html_content)
    message = EmailMultiAlternatives(title, text_content, SENDER, [user.email])
    message.attach_alternative(html_content, "text/html")
    message.send()


@app.task(name='remind_to_verify_account')
def dispatch_reminder():
    members = get_user_model().objects.filter(is_active=False)
    for member in members:
        if member.date_joined + timedelta(days=7) == datetime.utcnow().date():
            dispatch_mail.apply_async(args=[member.pk])
