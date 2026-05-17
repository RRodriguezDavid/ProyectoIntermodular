from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'Usuarios'

    def ready(self):
        # Importar las señales aquí para que Django las registre al arrancar.
        # Sin este import, post_save nunca se conecta y los UserProfile
        # no se crean automáticamente.
        import apps.users.signals  # noqa: F401
