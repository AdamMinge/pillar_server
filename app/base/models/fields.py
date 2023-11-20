from django.db import models
from django.core.exceptions import ValidationError


class VersionField(models.CharField):
    description = "Version number in X.Y.Z format"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 10)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, Version):
            return value
        if value is None:
            return value
        try:
            return Version(value)
        except ValueError as exc:
            raise ValueError("Version number must be in X.Y.Z format") from exc

    def from_db_value(self, value, expression, connection):
        # pylint: disable=unused-argument
        return self.to_python(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return str(value)


class Version:
    def __init__(self, version_str):
        version_parts = version_str.split(".")
        if len(version_parts) != 3:
            raise ValidationError("Version number must be in X.Y.Z format")
        self.major = int(version_parts[0])
        self.minor = int(version_parts[1])
        self.patch = int(version_parts[2])

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __repr__(self):
        return f'Version("{self}")'

    def __eq__(self, other):
        return (
            isinstance(other, Version)
            and self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) < (
            other.major,
            other.minor,
            other.patch,
        )


class LookupFieldDefault:
    requires_context = True

    def __init__(self, queryset, lookup_field):
        self.queryset = queryset
        self.lookup_field = lookup_field

    def __call__(self, serializer_field):
        return self.queryset.get(
            id=serializer_field.context["view"].kwargs[self.lookup_field]
        )

    def __repr__(self):
        return f"{self.__class__.__name__}()"
