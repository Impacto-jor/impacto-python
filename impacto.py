import json
from urllib.parse import urljoin

import requests

def response_exception(response):
    try:
        json_response = response.json()
    except json.JSONDecodeError:
        raise RuntimeError(f'Error making request (status code: {response.status_code})')
    else:
        error_message = json_response.get('detail', None)
        if not error_message:
            error_message = ', '.join([f'{key}: {value}'
                                       for key, value in json_response.items()])
        raise RuntimeError(f'Error making request ({error_message})')


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
            response_exception(response)

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

    def _get_options(self, url):
        response = requests.options(
            urljoin(self.api_url, url),
            params={'access_token': self.access_token},
        )
        return response.json()

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

    def impact_options(self):
        return self._get_options('impacts')

    def insight_options(self):
        return self._get_options('insights')

    def create_insight(self, url, type, media, comments=None, date=None,
            followers=None, likes=None, links_partner=None,
            mentions_partner=None, political_party=None, political_state=None,
            profile_picture_url=None, profile_title=None, profile_url=None,
            shares=None, story_url=None, text=None, text_snippet=None,
            title=None):
        data = {
            'comments': comments,
            'date': date,
            'followers': followers,
            'likes': likes,
            'links_partner': links_partner,
            'media': media,
            'mentions_partner': mentions_partner,
            'political_party': political_party,
            'political_state': political_state,
            'profile_picture_url': profile_picture_url,
            'profile_title': profile_title,
            'profile_url': profile_url,
            'shares': shares,
            'story_url': story_url,
            'text': text,
            'text_snippet': text_snippet,
            'title': title,
            'type': type,
            'url': url,
        }
        response = requests.post(
            urljoin(self.api_url, 'insights'),
            data=data,
            params={'access_token': self.access_token},
        )
        if not response.ok:
            response_exception(response)

        return response.json()
