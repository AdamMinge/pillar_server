import uuid
import functools

from django.contrib.auth import get_user_model

from base.tests import GenericTestCase, invoke_repeatedly_context

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import AccessToken

from authentication.factories import UserFactory, OrganizationAPIKeyFactory
from authentication.serializers import UserSerializer
from authentication.filters import UserFilter


def attach_api_key_credentials(api_key_factory_params: dict[any] = None):
    def decorator(func):
        original_method = func.setUp if isinstance(func, type) else func

        @functools.wraps(original_method)
        def decorated_method(self, *args, **kwargs):
            self.credentials_api_key = OrganizationAPIKeyFactory.create(
                **api_key_factory_params if api_key_factory_params else {}
            )[1]
            # pylint: disable=protected-access
            old_credentials = self.client._credentials
            self.client.credentials(
                **self.client._credentials, **{"HTTP_API_KEY": self.credentials_api_key}
            )

            original_method(self, *args, **kwargs)

            if not isinstance(func, type):
                self.client.credentials(**old_credentials)
                del self.credentials_api_key

        if isinstance(func, type):
            func.setUp = decorated_method
            return func

        return decorated_method

    return decorator


def attach_user_credentials(user_factory_params: dict[any] = None):
    def decorator(func):
        original_method = func.setUp if isinstance(func, type) else func

        @functools.wraps(original_method)
        def decorated_method(self, *args, **kwargs):
            self.credentials_user = UserFactory.create(
                **user_factory_params if user_factory_params else {}
            )
            authorization_key = f"Bearer {AccessToken.for_user(self.credentials_user)}"

            # pylint: disable=protected-access
            old_credentials = self.client._credentials
            self.client.credentials(
                **self.client._credentials,
                **{"HTTP_AUTHORIZATION": authorization_key},
            )

            original_method(self, *args, **kwargs)

            if not isinstance(func, type):
                self.client.credentials(**old_credentials)
                del self.credentials_user

        if isinstance(func, type):
            func.setUp = decorated_method
            return func

        return decorated_method

    return decorator


@attach_api_key_credentials()
class LoginTestCase(GenericTestCase):
    def setUp(self):
        self.url = reverse("login", kwargs={"version": "v1"})
        self.password = "password123"
        self.user = UserFactory.create(password=self.password)

    def test_login_success(self):
        data = {"email": f"{self.user.email}", "password": self.password}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        data = {"email": f"{self.user.email}", "password": f"wrong_{self.password}"}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)


@attach_api_key_credentials()
class SignupTestCase(GenericTestCase):
    def setUp(self):
        self.url = reverse("signup", kwargs={"version": "v1"})
        self.user = UserFactory.create()

    def test_signup_success(self):
        data = {
            "email": "new_user@example.com",
            "username": "new_user",
            "password": "password123",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("url", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("verified", response.data)
        self.assertIn("activated", response.data)
        self.assertIn("staff", response.data)
        self.assertIn("created", response.data)
        self.assertIn("updated", response.data)
        self.assertEqual(response.data["email"], data["email"])
        self.assertEqual(response.data["username"], data["username"])

    def test_signup_invalid_password(self):
        data = {
            "email": "new_user@example.com",
            "username": "new_user",
            "password": "password",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_email_already_exists(self):
        data = {
            "email": f"{self.user.email}",
            "username": "new_user",
            "password": "password123",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_signup_username_already_exists(self):
        data = {
            "email": "new_user@example.com",
            "username": f"{self.user.username}",
            "password": "password123",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)


@attach_api_key_credentials()
@attach_user_credentials()
class UserListTestCase(GenericTestCase):
    def setUp(self):
        UserFactory.create(username="user_1", email="user_1@test.com")
        UserFactory.create(username="user_2", email="user_2@test.com")
        UserFactory.create(username="user_3", email="user_3@test.com")
        UserFactory.create(username="user_4", email="user_4@example.com")
        UserFactory.create(username="admin_1", email="admin_1@example.com")
        UserFactory.create(username="admin_2", email="admin_2@example.com")
        UserFactory.create(username="admin_3", email="admin_3@example.com")
        UserFactory.create(username="admin_4", email="admin_4@test.com")

    @invoke_repeatedly_context(
        steps=[
            {"filters": {}},
            {"filters": {"ordering": "username"}},
            {"filters": {"ordering": "-username"}},
            {"filters": {"ordering": "email"}},
            {"filters": {"ordering": "-email"}},
            {"filters": {"username__contains": "admin"}},
            {"filters": {"email__contains": "user"}},
            {"filters": {"username__contains": "user", "email__contains": "test"}},
        ]
    )
    def test_filtered_get_users_success(self, filters):
        url = reverse("user-list", kwargs={"version": "v1"})
        filters_url = "&".join(f"{key}={filters[key]}" for key in filters)
        filters_url = f"?{filters_url}" if filters_url else ""
        response = self.client.get(f"{url}{filters_url}")

        _filter = UserFilter(
            filters,
            queryset=get_user_model().objects.all(),
        )
        _serializer = UserSerializer(
            _filter.qs,
            many=True,
            context={"request": self.versioning_request()},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(_serializer.data))
        self.assertEqual(response.data["results"], _serializer.data)


@attach_api_key_credentials()
@attach_user_credentials()
class UserDetailTestCase(GenericTestCase):
    def test_get_user_success(self):
        url = reverse(
            "user-detail", kwargs={"version": "v1", "id": self.credentials_user.id}
        )
        response = self.client.get(url)

        user_serializer = UserSerializer(
            self.credentials_user,
            context={"request": self.versioning_request()},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, user_serializer.data)

    def test_get_user_invalid_uuid(self):
        url = reverse("user-detail", kwargs={"version": "v1", "id": str(uuid.uuid4())})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
