import threading
import datetime
import jwt

from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from urllib.parse import urljoin

from .settings import api_settings


class AccountVerificationSender:
    sender = api_settings.EMAIL_SENDER
    logo = api_settings.EMAIL_LOGO
    signature = api_settings.EMAIL_SIGNATURE
    subject = api_settings.EMAIL_ACCOUNT_VERIFICATION_SUBJECT
    plain = api_settings.EMAIL_ACCOUNT_VERIFICATION_PLAIN
    html = api_settings.EMAIL_ACCOUNT_VERIFICATION_HTML

    def send(self, user, url, token, thread=True):
        if thread:
            thr = threading.Thread(target=self._send, args=(user, url, token))
            thr.start()
        else:
            self._send(user, url, token)

    def _send(self, user, url, token):
        context = self.create_context(user, url, token)

        subject = Template(self.subject).render(Context(context))
        text = render_to_string(self.plain, context)
        html = render_to_string(self.html, context)

        msg = EmailMultiAlternatives(subject, text, self.sender, [user.email])
        msg.attach_alternative(html, "text/html")
        msg.send()

    def create_context(self, user, url, token):
        return {
            "logo": f"{self.logo}",
            "signature": f"{self.signature}",
            "url": urljoin(url, token),
            "username": f"{user.username}",
        }


class PasswordRecoverySender:
    sender = api_settings.EMAIL_SENDER
    logo = api_settings.EMAIL_LOGO
    signature = api_settings.EMAIL_SIGNATURE
    subject = api_settings.EMAIL_PASSWORD_RECOVERY_SUBJECT
    plain = api_settings.EMAIL_PASSWORD_RECOVERY_PLAIN
    html = api_settings.EMAIL_PASSWORD_RECOVERY_HTML

    def send(self, user, url, token, thread=True):
        if thread:
            thr = threading.Thread(target=self._send, args=(user, url, token))
            thr.start()
        else:
            self._send(user, url, token)

    def _send(self, user, url, token):
        context = self.create_context(user, url, token)

        subject = Template(self.subject).render(Context(context))
        text = render_to_string(self.plain, context)
        html = render_to_string(self.html, context)

        msg = EmailMultiAlternatives(subject, text, self.sender, [user.email])
        msg.attach_alternative(html, "text/html")
        msg.send()

    def create_context(self, user, url, token):
        return {
            "logo": f"{self.logo}",
            "signature": f"{self.signature}",
            "url": urljoin(url, token),
            "username": f"{user.username}",
        }


class TokenGenerator:
    algorithm = api_settings.TOKEN_GENERATOR_ALGORITHM
    secret = api_settings.TOKEN_GENERATOR_SECRET

    def make_token(self, user, **kwargs):
        exp = (datetime.datetime.today() + self.token_lifetime).timestamp()
        payload = {"email": user.email, "exp": exp}
        payload.update(**kwargs)
        return jwt.encode(
            payload, self.secret, algorithm=self.algorithm
        ), datetime.datetime.fromtimestamp(exp)

    def check_token(self, token, **kwargs):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            email, _ = payload["email"], payload["exp"]
            for key, value in kwargs.items():
                if payload[key] != value:
                    return False, None

            users = [get_user_model().objects.get(email=email)]

        except (
            ValueError,
            get_user_model().DoesNotExist,
            jwt.DecodeError,
            jwt.ExpiredSignatureError,
        ):
            return False, None

        if len(users) == 0 or users[0] is None:
            return False, None

        return True, users[0]


class AccountVerificationTokenGenerator(TokenGenerator):
    token_lifetime = api_settings.ACCOUNT_VERIFICATION_TOKEN_LIFETIME


class PasswordRecoveryTokenGenerator(TokenGenerator):
    token_lifetime = api_settings.PASSWORD_RECOVERY_TOKEN_LIFETIME
