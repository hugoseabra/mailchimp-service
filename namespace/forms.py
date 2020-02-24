from django import forms

from . import models


class NamespaceForm(forms.ModelForm):
    class Meta:
        model = models.Namespace
        fields = (
            'name',
            'slug',
            'api_key',
            'external_id',
            'default_tag',
            'default_list_id',
            'healthy',
            'sync_phone',
            'sync_address',
            'create_fields',
            'create_notes',
        )


class ListFieldForm(forms.ModelForm):
    class Meta:
        model = models.ListField
        fields = (
            'namespace',
            'label',
            'tag',
            'field_type',
            'help_text',
            'active',
        )

    def clean_label(self):
        label = self.cleaned_data.get('label')
        if label:
            label = str(label).title()

        return label

    def clean_tag(self):
        tag = self.cleaned_data.get('tag')
        if tag:
            tag = str(tag).replace(' ', '').replace('-', '').upper()

        return tag

