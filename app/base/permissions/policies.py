from rest_framework.permissions import BasePermission
from rest_access_policy import AccessPolicy


class GenericAccessPolicy(AccessPolicy):
    permissions: list[type[BasePermission]] = []
    statements = [
        {
            "action": ["*"],
            "principal": ["*"],
            "effect": "allow",
        },
    ]

    def __get_permissions(self):
        permissions = []
        for cls in self.__class__.mro():
            if hasattr(cls, "permissions"):
                permissions.extend(
                    permission_type() for permission_type in getattr(cls, "permissions")
                )
        return permissions

    def has_permission(self, request, view):
        return all(
            permission.has_permission(request, view)
            for permission in self.__get_permissions()
        ) and AccessPolicy.has_permission(self, request, view)

    def has_object_permission(self, request, view, obj):
        return all(
            permission.has_object_permission(request, view, obj)
            for permission in self.__get_permissions()
        ) and AccessPolicy.has_object_permission(self, request, view, obj)
