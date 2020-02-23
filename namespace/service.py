from mailchimp3.mailchimpclient import MailChimpError

from namespace.models import Namespace, ListField


def get_namespace(external_id: str, api_key: str):
    """
    Resgate de um namespace.
    :param external_id: identificador único do namespace
    :param api_key: Chave de API da conta do MailChimp vinculado ao namespace
    """
    try:
        return Namespace.objects.get(
            external_id=external_id.strip(),
            api_key=api_key.strip(),
        )
    except Namespace.DoesNotExist:
        return None


def get_lists(namespace: Namespace):
    """
    Resgate listas de um namespace
    """
    result = None

    if namespace:

        fields = [
            'lists.id',
            'lists.web_id',
            'lists.name',
        ]

        try:
            data = namespace.service.lists.all(
                get_all=True,
                fields=','.join(fields)
            )

            if 'lists' in data:
                result = dict()
                result['count'] = len(data.get('lists'))
                result['results'] = data.get('lists')

        except MailChimpError as e:
            from pprint import pprint
            pprint(e)

    return result


def get_list_by_id(namespace: Namespace, list_id: str):
    """
    Resgata uma lista a partir do ID da lista e das configurações de conexão
    de um namespace
    """
    result = None

    if namespace and list_id:

        fields = [
            'id',
            'web_id',
            'name',
        ]

        try:
            result = namespace.service.lists.get(
                list_id=list_id,
                fields=','.join(fields)
            )
        except MailChimpError as e:
            from pprint import pprint
            pprint(e)

    return result


def get_list(namespace: Namespace, force=False, ):
    """
    Resgata uma lista do ID da lista a partir das configurações de um namespace
    """
    mc_list = get_list_by_id(namespace=namespace,
                             list_id=namespace.default_list_id)

    if not mc_list and force is True:
        lists = get_lists(namespace)
        if lists and 'results' in lists and lists['results']:
            mc_list = lists['results'][0]

    return mc_list


def get_fields_to_sync(namespace: Namespace):
    if namespace.create_fields is False:
        return []

    not_sync_fields = list()

    try:
        result = namespace.service.lists.merge_fields.all(
            list_id=namespace.default_list_id,
            get_all=True
        )

        existing_field_tags = list()

        if 'merge_fields' in result and result['merge_fields']:
            for field in result['merge_fields']:
                existing_field_tags.append(field.get('tag'))

        for f in namespace.fields.filter(active=True):
            if f.tag not in existing_field_tags:
                not_sync_fields.append(f)

    except MailChimpError as e:
        from pprint import pprint
        pprint(e)

    return not_sync_fields


def add_field(field: ListField):
    namespace = field.namespace

    try:
        namespace.service.lists.merge_fields.create(
            list_id=namespace.default_list_id,
            data=field.to_sync_data(),
        )
    except MailChimpError as e:
        from pprint import pprint
        pprint(e)
        raise e


def validate_namespace_by_list(namespace: Namespace, mc_list: dict = None):
    """
    Vaida um namespace setando-o como "healthy" a partir de uma lista resgata
    da platforma do MailChimp.
    """
    if mc_list and isinstance(mc_list, dict):
        namespace.healthy = True
        namespace.default_list_id = mc_list.get('id')
        namespace.default_list_name = mc_list.get('name')
    else:
        namespace.healthy = False
        namespace.default_list_name = None

    namespace.save()

    for f in get_fields_to_sync(namespace):
        add_field(f)


def validate_namespace(namespace: Namespace, force_validation=False):
    """
    Vaida um namespace setando-o como "healthy".
    """
    mc_list = get_list(namespace, force=force_validation)
    validate_namespace_by_list(namespace, mc_list)
