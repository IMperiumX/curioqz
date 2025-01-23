from django.utils import timezone
from rest_framework import serializers

from quizify.common.utils import get_object_or_none
from quizify.users.models import User


class BearerTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=True, required=True, write_only=True)
    password = serializers.CharField(
        write_only=True,
        allow_null=True,
        required=True,
        allow_blank=True,
    )
    token = serializers.CharField(read_only=True)
    date_expired = serializers.DateTimeField(read_only=True)

    @staticmethod
    def get_keyword(obj):
        return "Bearer"

    @staticmethod
    def update_last_login(user):
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

    def get_request_user(self, data):
        request = self.context.get("request")
        if request.user and request.user.is_authenticated:
            user = request.user
        else:
            user_email = data.get("email")
            user = get_object_or_none(User, email=user_email)
            if not user:
                msg = f"user email {user_email} not exist"
                raise serializers.ValidationError(msg)
        return user

    def create(self, validated_data):
        request = self.context.get("request")
        user = self.get_request_user(validated_data)

        token, date_expired = user.create_bearer_token(request)
        self.update_last_login(user)

        return {"token": token, "date_expired": date_expired, "user": user}
