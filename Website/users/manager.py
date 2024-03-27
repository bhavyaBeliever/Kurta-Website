from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("username not defined")
        extra_fields['email']=self.normalize_email(extra_fields['email'])
        user=self.model(username=username, **extra_fields)
        user.set_password(password)
        return user
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault(is_staff=True)
        extra_fields.setdefault(is_superuser=True)
        extra_fields.setdefault(is_active=True)
        return self.create_user(username=username, password=password, **extra_fields)
    
