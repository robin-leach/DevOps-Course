import requests
import json
import logging
import os

log = logging.getLogger('app')

def make_trello_request(method, endpoint, extra_params = {}):
    params = {
        'key': os.getenv("TRELLO_KEY"),
        'token': os.getenv("TRELLO_TOKEN"),
    }

    params.update(extra_params)

    log.debug(
    f"""Sending HTTP request to Trello API.
        Method: {method.value}
        URL: {endpoint}
        Parameters: {json.dumps(params)}
    """
    )

    response = requests.request(method.value, endpoint, params=params)
    details = f'{len(response.json())} items found.' if method == "GET" else ''
    log.debug(f'Trello returned {response.status_code}.{details}')

    return response