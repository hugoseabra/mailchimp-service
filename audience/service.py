import hashlib

from django.utils.translation import ugettext_lazy as _
from mailchimp3.mailchimpclient import MailChimpError

from audience.models import Member
from mailchimp_service.exceptions import MailChimpServiceException


def get_member_hash(member: Member):
    return hashlib.md5(str(member.email).encode()).hexdigest()


def add_creation_note(member: Member):
    namespace = member.namespace

    if namespace.create_notes is False:
        return

    note = "CONTACT CREATED\n"
    note += "{created_from}: {created_from_value}\n"
    note += "{created_at}: {created_at_value}\n"
    note = note.format(
        created_from=_('Created from'),
        created_from_value=namespace.name,
        created_at=_('created at'),
        created_at_value=namespace.created_at.strftime(
            '%d/%m/%Y %Hh%M'
        )
    )

    namespace.service.lists.members.notes.create(
        list_id=namespace.default_list_id,
        subscriber_hash=member.mailchimp_id,
        data={
            'note': note,
        }
    )


def add_update_note(member: Member):
    namespace = member.namespace

    if namespace.create_notes is False:
        return

    note = "CONTACT UPDATED\n"
    note += "{updated_from}: {updated_from_value}\n"
    note += "{updated_at}: {updated_at_value}\n"
    note = note.format(
        updated_from=_('Updated from'),
        updated_from_value=namespace.name,
        updated_at=_('updated at'),
        updated_at_value=namespace.updated_at.strftime(
            '%d/%m/%Y %Hh%M'
        )
    )

    namespace.service.lists.members.notes.create(
        list_id=namespace.default_list_id,
        subscriber_hash=member.mailchimp_id,
        data={
            'note': note,
        }
    )


def update_tags(member: Member):
    namespace = member.namespace

    if not member.tags:
        return

    existing_tags = namespace.service.lists.members.tags.all(
        list_id=namespace.default_list_id,
        subscriber_hash=get_member_hash(member),
    )

    tags = dict()

    if member.tags:
        for t in existing_tags.get('tags', list()):
            tags[t.get('name')] = 'inactive'

        for m_tag in member.tags.split(';'):
            t = m_tag.strip()
            tags[t] = 'active'

    tags.update({
        namespace.default_tag: 'active',
    })

    namespace.service.lists.members.tags.update(
        list_id=namespace.default_list_id,
        subscriber_hash=get_member_hash(member),
        data={
            'tags': [{'name': k, 'status': v} for k, v in tags.items()],
        },
    )


def clean_tags(member: Member):
    namespace = member.namespace

    existing_tags = namespace.service.lists.members.tags.all(
        list_id=namespace.default_list_id,
        subscriber_hash=get_member_hash(member),
    )

    tags = list()

    if member.tags:
        for t in existing_tags.get('tags', list()):
            tags.append({'name': t.get('name'), 'status': 'inactive'})

    namespace.service.lists.members.tags.update(
        list_id=namespace.default_list_id,
        subscriber_hash=get_member_hash(member),
        data={
            'tags': tags,
        },
    )


def sync_member(member: Member):
    if member.excluded is False and member.synchronized is True:
        raise MailChimpServiceException(
            _('Member already synchronized.')
        )

    namespace = member.namespace

    if namespace.healthy is False:
        raise MailChimpServiceException(
            _('Unhealthy namespaces cannot have members synchronized.')
        )

    service = namespace.service

    if member.sync_create is True:
        try:
            data = member.to_sync_data()
            data['status'] = 'subscribed'

            mc_member = service.lists.members.create(
                list_id=namespace.default_list_id,
                data=data,
            )
            member.mailchimp_id = mc_member.get('id')
            member.synchronized = True
            member.save()

            add_creation_note(member)
            update_tags(member)

        except MailChimpError as e:
            raise_error = True
            for error in [error for error in e.args]:
                if 'status' in error and error['status'] == 400:
                    member.mailchimp_id = get_member_hash(member)
                    raise_error = False

            if raise_error is True:
                from pprint import pprint
                pprint(e)
                raise MailChimpServiceException(str(e))

    if member.sync_update is True:
        try:
            data = member.to_sync_data()
            data['status'] = 'subscribed'

            if member.mailchimp_id:
                m_hash = member.mailchimp_id
            elif 'id' not in data:
                m_hash = get_member_hash(member)
                data['id'] = m_hash
            else:
                m_hash = data['id']

            mc_member = service.lists.members.update(
                list_id=namespace.default_list_id,
                subscriber_hash=m_hash,
                data=data,
            )
            member.mailchimp_id = mc_member.get('id')
            member.synchronized = True
            member.save()

            add_update_note(member)
            update_tags(member)

        except MailChimpError as e:
            from pprint import pprint
            pprint(e)
            raise MailChimpServiceException(str(e))

    elif member.sync_delete is True:
        try:
            data = member.to_sync_data()
            data['status'] = 'unsubscribed'

            service.lists.members.update(
                list_id=namespace.default_list_id,
                subscriber_hash=member.mailchimp_id,
                data=data,
            )
            clean_tags(member)
            member.delete()

        except MailChimpError as e:
            from pprint import pprint
            pprint(e)
            raise MailChimpServiceException(str(e))
