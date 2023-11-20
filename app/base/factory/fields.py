import random
import factory

from django.core.files import File


class LazyFileField(factory.django.FileField):
    def evaluate(self, instance, step, extra):
        filename, content = self._make_content(extra)
        if callable(filename):
            filename = filename(instance)
        return File(content.file, filename)


class RandomValueField(factory.declarations.BaseDeclaration):
    def __init__(self, values):
        super().__init__()
        self.values = values

    def evaluate(self, instance, step, extra):
        index = random.randint(0, len(self.values) - 1)
        return self.values[index]
