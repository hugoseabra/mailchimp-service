from rest_framework import serializers

from audience import forms
from core.serializers import FormSerializerMixin
from namespace.serializers import ListFieldSerializer


class MemberFieldSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.MemberFieldForm
        model = forms.MemberFieldForm.Meta.model
        fields = (
            'pk',
            'list_field',
            'reply',
            'created_at',
            'updated_at',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.member_pk = None

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['list_field'] = \
            ListFieldSerializer(instance=instance.list_field).data

        return rep

    def get_form(self, data=None, files=None, **kwargs):
        if data:
            data = data.copy()
            data.update({
                'member': self.member_pk,
            })
        return super().get_form(data, files, **kwargs)
