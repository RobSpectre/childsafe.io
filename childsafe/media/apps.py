from django.apps import AppConfig


class MediaConfig(AppConfig):
    name = 'media'

    def ready(self):
        import media.signals
