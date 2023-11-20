from rest_framework_api_key.permissions import BaseHasAPIKey
from rest_framework.permissions import IsAuthenticated

from authentication.models import OrganizationAPIKey


class HasOrganizationAPIKey(BaseHasAPIKey):
    model = OrganizationAPIKey


class IsAuthenticatedAndVerified(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_verified
