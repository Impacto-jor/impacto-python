import json
from urllib.parse import urljoin

import requests


class Impacto:

    api_url = 'https://impacto-scrapers.herokuapp.com/api/'

    def __init__(self, username=None, email=None, password=None, access_token=None):
        if not any([username, email, password, access_token]):
            raise ValueError('Must provide (username/email and password) or access_token.')
        elif (username is not None or email is not None) and password is not None:
            self.access_token = self.authenticate(username or email, password)
        elif access_token is not None:
            self.access_token = access_token

    def authenticate(self, username_or_email, password):
        data = {'password': password}
        if '@' in username_or_email:
            data['email'] = username_or_email
        else:
            data['username'] = username_or_email

        response = requests.post(urljoin(self.api_url, 'login'), data=data)
        if response.status_code >= 400:
            print(response.content)
            raise ValueError('Invalid credentials')
        else:
            return response.json()['access_token']

    def _get(self, url, params=None):
        params = params or {}
        params.update({'access_token': self.access_token})
        response = requests.get(urljoin(self.api_url, url), params=params)
        if response.ok:
            return response.json()
        else:
            try:
                json_response = response.json()
            except json.JSONDecodeError:
                raise RuntimeError(f'Error making request (status code: {response.status_code})')
            else:
                raise RuntimeError(f'Error making request ({json_response["detail"]})')

    def _get_paginated_result(self, url, *args, **kwargs):
        url = urljoin(self.api_url, url)
        finished = False
        while not finished:
            json_response = self._get(url, kwargs)
            for row in json_response['data']:
                yield row

            next_page = json_response.get('next', None)
            if next_page is None:
                finished = True
            else:
                url = next_page

    def impact(self, id):
        return self._get(f'impact/{id}')

    def impacts(self, *args, **kwargs):
        return self._get_paginated_result('impacts', *args, **kwargs)

    def insight(self, id):
        return self._get(f'insight/{id}')

    def insights(self, *args, **kwargs):
        return self._get_paginated_result('insights', *args, **kwargs)

    def story(self, id):
        return self._get(f'story/{id}')

    def stories(self, *args, **kwargs):
        return self._get_paginated_result('stories', *args, **kwargs)
