from django.apps import AppConfig


class NewsyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsyapp'

    def ready(self):
        # Import celery app now that Django is mostly ready.
        # This initializes Celery and autodiscovers tasks
        import newsyapp.celery