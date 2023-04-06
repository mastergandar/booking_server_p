from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsSuperUser
from users.models import User
from users.serializers import UserRegisterSerializer, UserSerializer


class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer


class UserActivateView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def get_object(self):
        return get_object_or_404(User, id=self.kwargs['uid'])

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        user.confirm_email()
        user.save()
        return Response(
            status=status.HTTP_200_OK, data={'message': 'Account activated successfully',
                                             'user': UserSerializer(user).data}
        )


class UserMeRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.request.user.pk)


class UserViewDestroyView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all().get_not_banned()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        method = self.request.method
        if method in ['DELETE']:
            return [IsSuperUser()]
        return [AllowAny()]

    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj


