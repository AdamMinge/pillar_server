from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, OrderingFilter


class UserFilter(FilterSet):
    ordering = OrderingFilter(fields=("username", "email"))

    class Meta:
        model = get_user_model()
        fields = {
            "username": ["exact", "startswith", "contains"],
            "email": ["exact", "startswith", "contains"],
        }
