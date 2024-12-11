from django.db import models
from django.conf import settings
from .user_models import User

class Admin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_profile',
        primary_key=True
    )
    # Add any admin-specific fields here

    def save(self, *args, **kwargs):
        if not self.user_id:
            user = User.objects.create(username=f'admin_{self.pk}')
            user.role = 'admin'
            user.save()
            self.user = user
        super(Admin, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.get_full_name()}'
