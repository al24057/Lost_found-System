from django.apps import AppConfig


class LostFoundWebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Lost_found_Web'
    
    def ready(self):
        import Lost_found_Web.services.signals
