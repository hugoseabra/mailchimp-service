# -*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _

from .forms import MemberForm
from .models import Member
from .tasks import sync_member as _sync_member


def sync_member(modeladmin, request, queryset):
    queryset = queryset.filter(synchronized=False)
    for item in queryset:
        _sync_member.delay(member_pk=item.pk)

    num = queryset.count()
    messages.success(
        request,
        '{} {} {} agendadas para sincronização. Atualize a página para ver o'
        ' resultado em alguns instantes'.format(
            num or '0',
            'membro' if num == 1 else 'membros',
            'foi' if num == 1 else 'foram',
        )
    )


sync_member.short_description = "Sincronizar membros"


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    actions = [sync_member]
    form = MemberForm
    list_display = (
        'full_name',
        'namespace',
        'email',
        'synchronized',
        'excluded',
        'healthy',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'namespace',
        'excluded',
        'synchronized',
    )
    search_fields = (
        'namespace__name',
        'namespace__external_id',
        'namespace__api_key',
        'first_name',
        'last_name',
        'email',
        'external_id',
        'mailchimp_id',
    )
    date_hierarchy = 'created_at'
    raw_id_fields = ('namespace',)
    readonly_fields = (
        'healthy',
        'mailchimp_id',
        'pk',
        'created_at',
        'updated_at',
    )

    def healthy(self, instance):
        return instance.namespace.healthy is True

    healthy.short_description = _('healthy')
    healthy.boolean = True
