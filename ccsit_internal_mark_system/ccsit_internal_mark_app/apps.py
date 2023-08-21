from django.apps import AppConfig


class CcsitInternalMarkAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ccsit_internal_mark_app'



class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ccsit_internal_mark_app'

    def ready(self):
        import ccsit_internal_mark_app.signals  # Import your signals module here
