import json
import os
import requests
from urlparse import urlparse
import logging

class Zodiac(object):

    def __init__(self, username, password, company=None, api=None, api_version=None):

        self.api = api or 'https://dashboard.zodiacmetrics.com/api'
        self.api_version = api_version or 'v1'

        self.login_as(username, password)
        self.company = company or self.company

    def _format_url(self, url, **kwargs):
        kwargs['api'] = self.api
        kwargs['version'] = self.api_version
        return url.format(**kwargs)

    def _post(self, url, values):
        headers = {
            "Content-Type": "application/json"
        }
        resp = self.session.post(url, json=values)
        try:
            return json.loads(resp.text)
        except Exception as e:
            print resp.text
            raise e

    def _put(self, url, filepath, filename):
        headers = {
            "Content-Type": "multipart/form-data",
            "Content-Disposition": "attachment; filename=\"" + filename + "\""
        }
        with open(filepath, 'rb') as data:
            resp = self.session.put(url, data=data, headers=headers)
        return resp

    def _get(self, url):
        return self.session.get(url)

    def login_as(self, username, password):
        self.session = requests.Session()
        url = self._format_url('{api}/{version}/auth/login')
        body = self._post(url, {'email': username, 'password': password, 'rememberMe': True})
        self.company = body['mask']
        self.session.headers.update({'User-Authorization-Token': 'Bearer ' + body['token']})


    def _create_upload(self, path, filename):
        url = self._format_url(
            path,
            company=self.company
        )
        body = self._post(url, {'filename':filename})
        return body['url']


    def _create_record(self, path, filename, upload_url, description):
        s3_path = urlparse(upload_url).path
        url = self._format_url(path, company=self.company)
        self._post(
            url,
            {'filename': filename, 's3_path': s3_path, 'description': description}
        )
        return s3_path

    def _create_upload_location(self, filename):
        return self._create_upload('{api}/{version}/{company}/datasets/upload_url', filename)


    def upload_file(self, filepath, description):
        filename = filepath.split('/')[-1]
        if os.name == 'nt':
            filename = filepath.split('\\')[-1]
        upload_url = self._create_upload_location(filename)
        self._put(upload_url, filepath, filename)
        return self._create_record(
            '{api}/{version}/{company}/datasets/create', filename, upload_url, description
        )


    def _create_email_upload_location(self, filename):
        return self._create_upload('{api}/{vesion}/{company}/email/upload_url', filename)


    def upload_emails(self, filepath):
        filename = filepath.split('/')[-1]
        upload_url = self._create_email_upload_location(filename)
        self._put(upload_url, filepath, filename)
        return self._create_record(
            '{api}/{version}/{company}/email/create', filename, upload_url, ''
        )


    def submit_job(self, args):
        txlogs = []
        attrfiles = []
        for trans_log in args.transactions:
            txlogs.append(self.upload_file(trans_log, trans_log))
        for attr_file in args.attributes or []:
            attrfiles.append(self.upload_file(attr_file, attr_file))
        url = self._format_url(
            '{api}/{version}/{company}/models/{model_group_hash}/execute',
            company=self.company, model_group_hash=args.model_group_hash
        )
        self._post(
            url,
            {'transaction_logs': txlogs, 'attributes': attrfiles}
        )


    def _list_datasets(self):
        url = self._format_url('{api}/{version}/{company}/datasets/list', company=self.company)
        return json.loads(self._get(url).text)

    def list_datasets(self):
        data = self._list_datasets()
        return [d['filename'] for d in data]

    def get_latest_output(self, args):
        mgh = args.model_group_hash
        url = self._format_url(
            '{api}/{version}/{company}/datasets/{mgh}/modeling_output',
            company=self.company,
            mgh=mgh
        )
        api_text = self._get(url).text

        filename = json.loads(api_text)['id']
        resp = self._get(
            self._format_url(
                "{api}/{version}/{company}/datasets/{inst}/download_url",
                company=self.company,
                inst=filename)
        )
        download = json.loads(resp.text)['url']
        print "Download url %s" % download
        return download


    def get_download_url(self, filename):
        datasets = self._list_datasets()
        inst = [d['id'] for d in datasets if d['filename'] == filename][-1]
        if not inst:
            raise Exception("Unknown file")
        resp = self._get(
            self._format_url(
                "{api}/{version}/{company}/datasets/{inst}/download_url",
                company=self.company,
                inst=inst)
        )
        return json.loads(resp.text)['url']
