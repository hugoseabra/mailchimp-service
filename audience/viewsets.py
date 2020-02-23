from rest_framework import viewsets

from .serializers import MemberSerializer, MemberFieldSerializer


class MemberViewset(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    queryset = MemberSerializer.Meta.model.objects.get_queryset()

    def perform_destroy(self, instance):
        instance.excluded = True
        instance.save()


class MemberFieldViewset(viewsets.ModelViewSet):
    serializer_class = MemberFieldSerializer
    queryset = MemberFieldSerializer.Meta.model.objects.get_queryset()

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        serializer.member_pk = self.kwargs.get('member_pk')
        return serializer
