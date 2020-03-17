from rest_framework import serializers

from core.serializers import FormSerializerMixin
from namespace import forms


# from . import ListFieldSerializer


class SimpleNamespaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = forms.NamespaceForm.Meta.model
        fields = (
            'pk',
            'name',
            'slug',
            'default_tag',
            'default_list_id',
            'default_list_name',
            'healthy',
            'sync_phone',
            'sync_address',
            'create_fields',
            'create_notes',
        )


class NamespaceSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.NamespaceForm
        model = forms.NamespaceForm.Meta.model
        fields = (
            'pk',
            'name',
            'slug',
            'api_key',
            'external_id',
            'default_tag',
            'default_list_name',
            'default_list_id',
            'healthy',
            'sync_phone',
            'sync_address',
            'create_fields',
            'create_notes',
            'created_at',
            'updated_at',
        )
