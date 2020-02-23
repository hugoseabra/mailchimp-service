from rest_framework import serializers

from core.serializers import FormSerializerMixin
from namespace.serializers import SimpleNamespaceSerializer, \
    ListFieldSerializer
from . import forms


class MemberSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.MemberForm
        model = forms.MemberForm.Meta.model
        fields = (
            'pk',
            'namespace',
            'first_name',
            'last_name',
            'email',
            'birthday',
            'phone_country_code',
            'phone_region_code',
            'phone_number',
            'address1',
            'address2',
            'city',
            'state',
            'zip_code',
            'external_id',
            'tags',
            'synchronized',
            'mailchimp_id',
            'excluded',
            'created_at',
            'updated_at',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['namespace'] = \
            SimpleNamespaceSerializer(instance=instance.namespace).data

        return rep


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

        rep['member'] = MemberSerializer(instance=instance.member).data

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
