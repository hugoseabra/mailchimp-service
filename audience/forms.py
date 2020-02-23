from django import forms

from . import models


class MemberForm(forms.ModelForm):
    class Meta:
        model = models.Member
        fields = (
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
        )


class MemberFieldForm(forms.ModelForm):
    class Meta:
        model = models.MemberField
        fields = (
            'list_field',
            'member',
            'reply',
        )
