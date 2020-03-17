import uuid

from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from namespace import models
from .serializers import NamespaceSerializer, ListFieldSerializer
from .service import get_lists, get_list_by_id


class NamespaceViewset(viewsets.ModelViewSet):
    serializer_class = NamespaceSerializer
    queryset = NamespaceSerializer.Meta.model.objects.get_queryset()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    )


class ListFieldViewset(viewsets.ModelViewSet):
    serializer_class = ListFieldSerializer
    queryset = ListFieldSerializer.Meta.model.objects.get_queryset()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            namespace_id=self.kwargs.get('namespace_pk'),
        )
        return queryset

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        serializer.namespace_pk = self.kwargs.get('namespace_pk')
        return serializer


class MailChimpListViewset(viewsets.ViewSet):
    """
    MailChimp namespace list
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    )

    # Cache requested url for each user for 10 minutes
    @method_decorator(cache_page(60 * 10))
    def list(self, request, *args, **kwargs):
        namespace = self.kwargs.get('namespace_pk')

        try:
            namespace_pk = uuid.UUID(namespace, version=4)
        except ValueError:
            # If it's a value error, then the string
            # is not a valid hex code for a UUID.
            content = {'detail': [
                _('Namespace provided is not a valid UUID.')
            ]}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            namespace = models.Namespace.objects.get(pk=namespace_pk)
            return Response(data=get_lists(namespace))

        except models.Namespace.DoesNotExist:
            content = {'detail': [
                _('Namespace does not exist.')
            ]}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            content = {'detail': [str(e)]}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # Cache requested url for each user for 2 hours
    @method_decorator(cache_page(60 * 60 * 2))
    def retrieve(self, request, *args, **kwargs):
        namespace = self.kwargs.get('namespace_pk')
        pk = self.kwargs.get('pk')

        try:
            namespace_pk = uuid.UUID(namespace, version=4)
        except ValueError:
            # If it's a value error, then the string
            # is not a valid hex code for a UUID.
            content = {'detail': [
                _('Namespace provided is not a valid UUID.')
            ]}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            namespace = models.Namespace.objects.get(pk=namespace_pk)

        except models.Namespace.DoesNotExist:
            content = {'detail': [
                _('Namespace does not exist.')
            ]}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        return Response(data=get_list_by_id(namespace, list_id=pk))
