from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as AuthGroupAdmin

from rest_framework_api_key.admin import APIKeyModelAdmin
from rest_framework_api_key.models import APIKey

from authentication.models import OrganizationAPIKey, Organization, User


admin.site.unregister(APIKey)
admin.site.unregister(Group)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "active")


@admin.register(OrganizationAPIKey)
class OrganizationApiKeyAdmin(APIKeyModelAdmin):
    list_display = (*APIKeyModelAdmin.list_display, "get_organization_name")
    search_fields = (*APIKeyModelAdmin.search_fields, "get_organization_name")

    @admin.display(ordering="organization__name", description="Organization")
    def get_organization_name(self, obj: OrganizationAPIKey):
        return obj.organization.name


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "created_at"]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets = list(fieldsets)
        for fieldset in fieldsets:
            if "user_permissions" in fieldset[1]["fields"]:
                fieldset[1]["fields"] = tuple(
                    f for f in fieldset[1]["fields"] if f != "user_permissions"
                )
        return fieldsets


@admin.register(Group)
class GroupAdmin(AuthGroupAdmin):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets = list(fieldsets)
        for fieldset in fieldsets:
            if "permissions" in fieldset[1]["fields"]:
                fieldset[1]["fields"] = tuple(
                    f for f in fieldset[1]["fields"] if f != "permissions"
                )
        return fieldsets
