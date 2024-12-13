from django.db import models
from django.conf import settings
from .user_models import User

class Admin(models.Model):
    """Admin model that can manage entities."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_profile',
        primary_key=True
    )

    def save(self, *args, **kwargs):
        if not self.user_id:
            user = User.objects.create(username=f'admin_{self.pk}')
            user.role = 'admin'
            user.save()
            self.user = user
        super(Admin, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.get_full_name()}'
