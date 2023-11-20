from rest_framework.versioning import URLPathVersioning
from rest_framework.test import APITestCase, APIRequestFactory


class GenericTestCase(APITestCase):
    def versioning_request(self, version="v1"):
        factory = APIRequestFactory()
        request = factory.get("/")
        request.versioning_scheme = URLPathVersioning()
        request.version = version
        return request
