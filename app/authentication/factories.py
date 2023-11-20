import factory

from django.contrib.auth import get_user_model

from authentication.models import OrganizationAPIKey, Organization


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Sequence(lambda n: f"organization_{n}")


class OrganizationAPIKeyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrganizationAPIKey

    organization = factory.SubFactory(OrganizationFactory)
    name = factory.Sequence(lambda n: f"api_key_{n}")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_key(*args, **kwargs)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall(
        "set_password", get_user_model().objects.make_random_password()
    )
    is_verified = True
