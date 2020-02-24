# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib import messages

from .forms import NamespaceForm
from .models import Namespace
from .tasks import validate_namespace


def validate_namespaces(modeladmin, request, queryset):
    for item in queryset:
        force = not item.default_list_id
        validate_namespace.delay(namespace_pk=item.pk, force_validation=force)

    num = queryset.count()
    messages.success(
        request,
        '{} {} {} agendadas para validação. Atualize a página para ver o'
        ' resultado em alguns instantes'.format(
            num or '0',
            'namespace' if num == 1 else 'namespaces',
            'foi' if num == 1 else 'foram',
        )
    )


validate_namespaces.short_description = "Validate namespaces"


@admin.register(Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    actions = [validate_namespaces]
    form = NamespaceForm
    list_display = (
        'name',
        'external_id',
        'default_list_name',
        'healthy',
    )
    list_filter = ('created_at', 'updated_at', 'healthy')
    search_fields = (
        'name',
        'slug',
        'external_id',
        'default_list_name',
        'api_key',
        'default_list_id',
    )
    prepopulated_fields = {'slug': ['name']}
    date_hierarchy = 'created_at'
    readonly_fields = (
        'default_list_name',
        'pk',
        'created_at',
        'updated_at',
    )
