from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from quizify.authentication import errors
from quizify.authentication.mixins import AuthMixin

from . import serializers


class TokenCreateAPIView(AuthMixin, CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.BearerTokenSerializer
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = self.check_user_auth(serializer.validated_data)
            self.send_success_auth_signal(user=user)
            resp = super().create(request, *args, **kwargs)
        except errors.AuthFailedError as e:
            return Response(e.as_data(), status=400)
        except Exception as e:  # noqa: BLE001
            return Response({"error": str(e)}, status=400)
        else:
            return resp
