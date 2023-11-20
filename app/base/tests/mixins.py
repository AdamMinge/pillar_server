from django.apps import apps


class TearDownModelsTestCaseMixin:
    # pylint: disable=invalid-name
    def tearDown(self):
        for model in apps.get_models():
            model.objects.all().delete()
        super().tearDown()
