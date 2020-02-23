import requests
from mailchimp3 import MailChimp


def get_client(namespace_name, api_key) -> MailChimp:
    version = '1.0.0'

    headers = requests.utils.default_headers()
    headers['User-Agent'] = 'MailchimpService-{}/{}'.format(version,
                                                            namespace_name)

    return MailChimp(
        mc_api=api_key,
        enabled=True,
        request_headers=headers,
    )
