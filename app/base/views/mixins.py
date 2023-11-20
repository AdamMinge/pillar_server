from rest_access_policy import AccessViewSetMixin


class AccessPolicyViewSetMixin(AccessViewSetMixin):
    def __init__(self, *args, **kwargs):
        self.permission_classes = list(self.permission_classes)
        super().__init__(*args, **kwargs)
