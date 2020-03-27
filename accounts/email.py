from django.contrib.auth.tokens import default_token_generator
from accounts.mail import BaseEmailMessage
from accounts.utils import encode_uid

class ActivationEmail(BaseEmailMessage):
    template_name = "email/account_activation_email.html"
    
    def get_context_data(self):
        activation_url = "/activate/{uid}/{token}"
        context = super().get_context_data()
        user = context.get("user")
        context["uid"] = encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = activation_url.format(**context)
        return context

class ConfirmationEmail(BaseEmailMessage):
    template_name = "email/account_confirmation_email.html"

class PasswordResetEmail(BaseEmailMessage):
    template_name = "email/password_reset_email.html"

    def get_context_data(self):
        reset_url = "/password-reset/{uid}/{token}"
        context = super().get_context_data()
        user = context.get("user")
        context["uid"] = encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = reset_url.format(**context)
        return context

class PasswordChangedConfirmationEmail(BaseEmailMessage):
    template_name = "email/password_changed_confirmation_email.html"
