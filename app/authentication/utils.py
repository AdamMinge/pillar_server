import datetime
import threading
import jwt

from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.conf import settings


class EmailVerificationTokenSender:
    subject = getattr(
        settings, "VERIFICATION_EMAIL_SUBJECT", "Confirm your email {{ user.username }}"
    )
    plain = getattr(settings, "VERIFICATION_EMAIL_PLAIN", "verification_mail.txt")
    html = getattr(settings, "VERIFICATION_EMAIL_HTML", "verification_mail.html")
    sender = settings.EMAIL_HOST_USER
    verification_url = getattr(settings, "VERIFICATION_EMAIL_VERIFICATION_URL", None)
    logo_url = getattr(settings, "VERIFICATION_EMAIL_LOGO_URL", None)
    signature = getattr(settings, "VERIFICATION_EMAIL_SIGNATURE", None)

    def send(self, user, token: str, thread=True):
        if thread:
            thr = threading.Thread(target=self._send, args=(user, token))
            thr.start()
        else:
            self._send(user, token)

    def _send(self, user, token: str):
        context = {
            "verification_url": f"{self.verification_url}/{token}",
            "logo_url": self.logo_url,
            "signature": self.signature,
        }

        subject = Template(self.subject).render(Context(context))
        text = render_to_string(self.plain, context)
        html = render_to_string(self.html, context)

        msg = EmailMultiAlternatives(subject, text, self.sender, [user.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


class EmailVerificationTokenGenerator:
    algorithm = "HS256"
    secret = settings.SECRET_KEY
    token_lifetime = datetime.timedelta(days=1)

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

    @staticmethod
    def now():
        return datetime.datetime.now().timestamp()
