from rest_framework import serializers

from core.serializers import FormSerializerMixin
from namespace import forms
from .namespace_serializers import SimpleNamespaceSerializer


class ListFieldSerializer(FormSerializerMixin, serializers.ModelSerializer):
    namespace = SimpleNamespaceSerializer(read_only=True)

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
            'namespace',
            'created_at',
            'updated_at',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.namespace_pk = None
