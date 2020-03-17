from rest_framework import viewsets
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated

from .serializers import MemberSerializer, MemberFieldSerializer


class MemberViewset(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    queryset = MemberSerializer.Meta.model.objects.get_queryset()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    )

    def perform_destroy(self, instance):
        instance.excluded = True
        instance.save()


class MemberFieldViewset(viewsets.ModelViewSet):
    serializer_class = MemberFieldSerializer
    queryset = MemberFieldSerializer.Meta.model.objects.get_queryset()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(member_id=self.kwargs.get('member_pk'))
        return queryset

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        serializer.member_pk = self.kwargs.get('member_pk')
        return serializer
