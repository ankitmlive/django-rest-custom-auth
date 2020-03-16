from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    use_in_migrations = True
    
    def create_user(self, fullname, username, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        if not fullname:
            raise ValueError(_('The fullname must be set'))
        if not username:
            raise ValueError(_('The username must be set'))
        if not email:
            raise ValueError(_('User must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          username = username,
                          fullname = fullname,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, fullname, email, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
            fullname=fullname
		)

        user.is_admin = True
        #user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

