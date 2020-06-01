from django.apps import AppConfig


class ScraperConfig(AppConfig):
    name = 'scraper'

    def ready(self):
        from data_updater import updater
        updater.start()
