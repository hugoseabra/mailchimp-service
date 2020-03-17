# Generated by Django 3.0.3 on 2020-03-17 20:46

import core.models.mixins.deletable_mixin
import core.models.mixins.entity_mixin
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Namespace',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(max_length=255, verbose_name='slug')),
                ('default_tag', models.CharField(db_index=True, max_length=80, unique=True, verbose_name='Default tag')),
                ('external_id', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='external ID')),
                ('api_key', models.CharField(db_index=True, max_length=48, verbose_name='api key')),
                ('default_list_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='default list ID')),
                ('default_list_name', models.CharField(blank=True, editable=False, max_length=255, null=True, verbose_name='default list name')),
                ('healthy', models.BooleanField(default=False, help_text='If false, it means that mailchimp api key or list ID are not available.', verbose_name='healthy')),
                ('sync_address', models.BooleanField(default=False, help_text='If true, the service will send member address to mailchimp.', verbose_name='synchronize address')),
                ('sync_phone', models.BooleanField(default=False, help_text='If true, the service will send member phone to mailchimp.', verbose_name='synchronize phone')),
                ('create_fields', models.BooleanField(default=False, help_text='If true, the service will create and register value in custom fields in member record in mailchimp.', verbose_name='synchronize fields')),
                ('create_notes', models.BooleanField(default=False, help_text='If true, the service will create notes in member record in mailchimp.', verbose_name='create notes')),
            ],
            options={
                'verbose_name': 'namespace',
                'verbose_name_plural': 'namespaces',
                'unique_together': {('external_id', 'slug')},
            },
            bases=(core.models.mixins.entity_mixin.EntityMixin, core.models.mixins.deletable_mixin.DeletableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ListField',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('field_type', models.CharField(choices=[('text', 'Text'), ('number', 'Number')], default='text', max_length=6, verbose_name='field type')),
                ('label', models.CharField(max_length=50, verbose_name='label')),
                ('tag', models.CharField(max_length=50, verbose_name='tag')),
                ('help_text', models.CharField(blank=True, max_length=255, null=True, verbose_name='help text')),
                ('active', models.BooleanField(default=False, help_text='If true, it means that the field will be created in list in MailChimp platform.', verbose_name='active')),
                ('namespace', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fields', to='namespace.Namespace', verbose_name='namespace')),
            ],
            options={
                'verbose_name': 'list field',
                'verbose_name_plural': 'list fields',
                'unique_together': {('namespace_id', 'tag')},
            },
            bases=(core.models.mixins.entity_mixin.EntityMixin, core.models.mixins.deletable_mixin.DeletableModelMixin, models.Model),
        ),
    ]