from django.apps import AppConfig

class MyBlogConfig(AppConfig):
    name = 'myblog'

    def ready(self):
        import myblog.signals  # Asegúrate de importar tu archivo de señales
