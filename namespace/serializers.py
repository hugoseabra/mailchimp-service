from rest_framework import serializers

from core.serializers import FormSerializerMixin
from . import forms


class SimpleNamespaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = forms.NamespaceForm.Meta.model
        fields = (
            'pk',
            'name',
            'slug',
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
            'default_list_name',
            'healthy',
            'sync_phone',
            'sync_address',
            'create_fields',
            'created_at',
            'updated_at',
        )


class ListFieldSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.ListFieldForm
        model = forms.ListFieldForm.Meta.model
        fields = (
            'pk',
            'label',
            'tag',
            'field_type',
            'help_text',
            'active',
            'created_at',
            'updated_at',
        )
        write_only_fields = ('namespace',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.namespace_pk = None

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['namespace'] = \
            SimpleNamespaceSerializer(instance=instance.namespace).data

        return rep

    def get_form(self, data=None, files=None, **kwargs):
        if data:
            data = data.copy()
            data.update({
                'namespace': self.namespace_pk,
            })
        return super().get_form(data, files, **kwargs)
