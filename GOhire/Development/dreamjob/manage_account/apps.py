from django.apps import AppConfig


class ManageAccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manage_account'
    
    from django.apps import AppConfig

class ManageAccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manage_account'

    def ready(self):
        import manage_account.signals  # Import signals when the app is ready
