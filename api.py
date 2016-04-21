import json
import requests

API = 'https://dashboard.zodiacmetrics.com/api'
API_VERSION = 'v1'


class Zodiac(object):

    def __init__(self, username, password):
        self.login_as(username, password)

    def _format_url(self, url, **kwargs):
        kwargs['api'] = API
        kwargs['version'] = API_VERSION
        return url.format(**kwargs)

    def _post(self, url, values):
        resp = self.session.post(url, json=values)
        return json.loads(resp.text)

    def _put(self, url, filepath, filename):
        headers = {
            "Content-Type": "multipart/form-data",
            "Content-Disposition": "attachment; filename=\"" + filename + "\""
        }
        with open(filepath, 'rb') as data:
            resp = self.session.put(url, data=data, headers=headers)

    def login_as(self, username, password):
        self.session = requests.Session()
        url = self._format_url('{api}/{version}/auth/login')
        body = self._post(url, {'email': username, 'password': password, 'rememberMe': True})
        self.company = body['mask']
        self.session.headers.update({'User-Authorization-Token': 'Bearer ' + body['token']})

    def _create_upload_location(self, filename):
        url = self._format_url(
            '{api}/{version}/{company}/datasets/upload_url',
            company=self.company
        )
        body = self._post(url, {'filename':filename})
        return body['url']


    def upload_file(self, filepath, description):
        filename = filepath.split('/')[-1]
        upload_url = self._create_upload_location(filename)
        self._put(upload_url, filepath, filename)
        s3path = upload_url.lstrip('https://raw-datasets.s3.amazonaws.com/').split('?')[0]
        url = self._format_url('{api}/{version}/{company}/datasets/create', company=self.company)
        self._post(
            url,
            {'description': description, 'filename': filename, 's3_path': s3path}
        )
