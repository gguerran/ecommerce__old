from rest_framework.viewsets import ModelViewSet

from ecommerce.accounts.models import User
from ecommerce.accounts.permissions import IsAuthenticatedOrWriteOnly
from ecommerce.accounts.serizalizers import (
    UserSerializer, UpdateUserSerializer
)


class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrWriteOnly]
    filterset_fields = ('username')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all().order_by('created')
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'update':
            return UpdateUserSerializer
        return UserSerializer
