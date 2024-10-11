"""from django.apps import AppConfig
import apps.myblog.signals


class MyBlogConfig(AppConfig):
    name = 'apps.myblog'

    def ready(self):
        import myblog.signals  # Asegúrate de importar tu archivo de señales

"""
"""from django.apps import AppConfig

class MyBlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.myblog'
"""


from django.apps import AppConfig
import apps.myblog.signals  # Importación fuera de la clase


class MyBlogConfig(AppConfig):
    name = 'apps.myblog'

    def ready(self):
        import apps.myblog.signals  # Usa la ruta correcta para la importación
