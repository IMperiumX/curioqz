from django.test import RequestFactory

from curioqz.users.api.views import UserViewSet
from curioqz.users.models import User


class TestUserViewSet:
    """ """
    def test_get_queryset(self, user: User, rf: RequestFactory):
        """

        :param user: User: 
        :param rf: RequestFactory: 

        """
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: RequestFactory):
        """

        :param user: User: 
        :param rf: RequestFactory: 

        """
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)

        assert response.data == {
            "username": user.username,
            "name": user.name,
            "url": f"http://testserver/api/users/{user.username}/",
        }
