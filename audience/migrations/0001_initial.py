# Generated by Django 3.0.3 on 2020-03-17 20:46

import core.models.mixins.deletable_mixin
import core.models.mixins.entity_mixin
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('namespace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(max_length=100, verbose_name='last name')),
                ('email', models.EmailField(max_length=255, verbose_name='e-mail')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='birthday')),
                ('phone_country_code', models.CharField(blank=True, max_length=5, null=True, verbose_name='DDI')),
                ('phone_region_code', models.CharField(blank=True, max_length=5, null=True, verbose_name='DDD')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='phone number')),
                ('address1', models.TextField(blank=True, null=True, verbose_name='address 1')),
                ('address2', models.TextField(blank=True, null=True, verbose_name='address 2')),
                ('city', models.CharField(blank=True, max_length=150, null=True, verbose_name='city')),
                ('state', models.CharField(blank=True, max_length=80, null=True, verbose_name='state')),
                ('zip_code', models.CharField(blank=True, max_length=80, null=True, verbose_name='zip code')),
                ('external_id', models.TextField(verbose_name='external ID')),
                ('mailchimp_id', models.TextField(blank=True, editable=False, null=True, verbose_name='mailchimp ID')),
                ('tags', models.TextField(blank=True, null=True, verbose_name='tags')),
                ('synchronized', models.BooleanField(default=False, help_text='If true, it means that the member has been saved / edited in MailChimp platform.', verbose_name='synchronized')),
                ('excluded', models.BooleanField(default=False, help_text='If true, the member will be scheduled to unsubscribe in mailchimp and then be deleted.', verbose_name='excluded')),
                ('namespace', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='members', to='namespace.Namespace', verbose_name='namespace')),
            ],
            options={
                'verbose_name': 'member',
                'verbose_name_plural': 'members',
                'unique_together': {('namespace_id', 'external_id'), ('namespace_id', 'mailchimp_id')},
            },
            bases=(core.models.mixins.entity_mixin.EntityMixin, core.models.mixins.deletable_mixin.DeletableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MemberField',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('reply', models.TextField(verbose_name='reply')),
                ('list_field', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='member_fields', to='namespace.ListField', verbose_name='list field')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_fields', to='audience.Member', verbose_name='member')),
            ],
            options={
                'verbose_name': 'member field',
                'verbose_name_plural': 'member fields',
                'unique_together': {('list_field_id', 'member_id')},
            },
            bases=(core.models.mixins.entity_mixin.EntityMixin, core.models.mixins.deletable_mixin.DeletableModelMixin, models.Model),
        ),
    ]
