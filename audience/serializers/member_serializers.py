from copy import deepcopy

from rest_framework import serializers

from audience import forms
from audience.models import MemberField
from audience.serializers import MemberFieldSerializer
from core.serializers import FormSerializerMixin
from namespace.models import ListField
from namespace.serializers import SimpleNamespaceSerializer


class MemberSerializer(FormSerializerMixin, serializers.ModelSerializer):
    member_fields = MemberFieldSerializer(many=True, read_only=True)

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
            'member_fields',
            'synchronized',
            'mailchimp_id',
            'excluded',
            'created_at',
            'updated_at',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.member_fields = list()

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['namespace'] = \
            SimpleNamespaceSerializer(instance=instance.namespace).data

        rep['tags'] = list()
        if instance.tags:
            rep['tags'] = instance.tags.split(';')

        return rep

    def to_internal_value(self, data: dict):
        data = self.normalize_data(deepcopy(data))

        if 'tags' in data and data['tags']:
            tags = data['tags']
            if isinstance(tags, str):
                tags = eval(data['tags'])

            if isinstance(tags, list):
                tags = [x.strip() for x in list(set(tags)) if x]
                data['tags'] = ';'.join(tags)

        return super().to_internal_value(data)
