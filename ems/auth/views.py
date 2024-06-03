from rest_framework.response import Response
from rest_framework import permissions, generics
from auth import serializers
from knox.models import AuthToken
from users.serializers import nested_serializers as users_serializers
from throttles import LoginThrottle
from authaudit.signals import user_logged_in


class LoginView(generics.GenericAPIView):

    """ Представление входа (авторизации) """

    permission_classes = [permissions.AllowAny, ]
    serializer_class = serializers.LoginSerializer
    throttle_classes = [LoginThrottle, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        user_logged_in(sender=user.__class__, request=request, user=user)
        return Response({
            'user_profiles': users_serializers.UserDetailSerializer(user).data,
            'token': AuthToken.objects.create(user)[1]
        })
