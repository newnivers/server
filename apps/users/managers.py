from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, password=None, **kwargs):
        user = self.model(
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin_user(self, password=None, **kwargs):
        user = self.create_user(
            password=password,
            is_admin=True,
            **kwargs,
        )
        return user

    def create_superuser(self, password=None, **kwargs):
        user = self.create_user(
            password=password,
            is_admin=True,
            is_superuser=True,
            **kwargs,
        )
        return user
