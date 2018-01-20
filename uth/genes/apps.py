from django.apps import apps, AppConfig

class GenesConfig(AppConfig):

    def __init__(self):
        self.name = "genes"
        AppConfig.__init__(name="genes")
