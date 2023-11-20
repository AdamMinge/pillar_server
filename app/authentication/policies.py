from base.permissions import GenericAccessPolicy

from authentication.permissions import (
    HasOrganizationAPIKey,
    IsAuthenticated,
    IsAuthenticatedAndVerified,
)


class OrganizationAPIKeyAccessPolicy(GenericAccessPolicy):
    permissions = [HasOrganizationAPIKey]


class AuthenticatedAccessPolicy(OrganizationAPIKeyAccessPolicy):
    permissions = [IsAuthenticated]


class AuthenticatedAndVerifiedAccessPolicy(OrganizationAPIKeyAccessPolicy):
    permissions = [IsAuthenticatedAndVerified]


class UserAccessPolicy(AuthenticatedAndVerifiedAccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["*"],
            "effect": "allow",
        },
    ]
