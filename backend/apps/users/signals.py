"""
Señales de la app users.

post_save en User → crea o actualiza el UserProfile automáticamente.
Esto garantiza que CUALQUIER usuario (creado por registro, por
createsuperuser, desde el admin de Django o por fixtures) siempre
tenga su perfil asociado.
"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    - Si el User acaba de crearse (created=True): crea el perfil vacío.
    - Si el User ya existía y se ha guardado de nuevo: lo actualiza
      (necesario para que el admin de Django pueda editar el perfil).
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # get_or_create cubre el caso de usuarios que existían antes
        # de que las señales estuvieran configuradas (p.ej. el superusuario)
        UserProfile.objects.get_or_create(user=instance)
