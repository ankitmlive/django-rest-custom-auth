from django.contrib.auth.tokens import default_token_generator
from accounts.mail import BaseEmailMessage

from accounts.utils import encode_uid
#from djoser.conf import settings

class ActivationEmail(BaseEmailMessage):
    template_name = "email/activation.html"
    
    def get_context_data(self):
        activation_url = "/activate/{uid}/{token}"
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = activation_url.format(**context)
        return context

class ConfirmationEmail(BaseEmailMessage):
    template_name = "email/confirmation.html"