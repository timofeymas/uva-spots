from django.apps import AppConfig

class Study_spot_projectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'study_spot_project' 

    def ready(self):
        import study_spot_project.signals
