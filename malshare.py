# coding: utf-8
# !/usr/bin/env python

import requests

__author__ = 'Animesh Shaw aka Psycho_Coder'
__version__ = '1.0'


class Malshare():
    def __init__(self, api_key):
        self.API_KEY = api_key
        self.API_URL = 'http://www.malshare.com/api.php'

    def get_response(self, payload, output='json'):
        """

        :param payload:
        :param output:
        :return:
        """
        resp = requests.get(self.API_URL, params=payload)
        if resp is not None:
            if output == 'json':
                return resp.json()
            elif output == 'raw':
                return resp.text
        return False

    def _download_file_(self, payload, file_hash):
        data = requests.get(self.API_URL, params=payload, stream=True)

        with open(file_hash, 'wb') as fd:
            for chunk in data.iter_content(chunk_size=128):
                fd.write(chunk)

    def getlist(self):
        """

        :return:
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'getlist'})

    def getlistraw(self):
        """

        :return:
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'getlistraw'}, 'raw')

    def getsources(self):
        """

        :return:
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'getsources'})

    def getsourcesraw(self):
        """

        :return:
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'getsourcesraw'}, 'raw')

    def getfiledetails(self, file_hash, output='json'):
        """

        :param file_hash:
        :param output:
        :return:
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'details', 'hash': file_hash}, output)

    def validate_hash(self, file_hash):
        """

        :param file_hash:
        :return:
        """
        return self.getfiledetails(file_hash, 'raw') != 'Invaid Hash'

    def getfile(self, file_hash, save_loc):
        """

        :param file_hash:
        :return:
        """
        if self.validate_hash(file_hash):
            self._download_file_({'api_key': self.API_KEY, 'action': 'getfile', 'hash': file_hash}, file_hash)
            return True
        return False

    def getfiletypelist(self, file_type):
        """

        Sample File Types: C, XML, PHP, HTML, ASCII, PE-32, PE32, ISO-8859, UTF-8, MSVC, Composite,
                        data, 80386, current, BSD, Zip, 7-zip
        :param file_type:
        :return:
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'type', 'type': file_type})

    def search(self, query):
        """

        :param query:
        :return:
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'search', 'query': query}, 'raw')

    def upload_file(self, file_path):
        """

        :param file_path:
        :return:
        """
        try:
            with open(file_path, 'rb') as fd:
                file_bin = {'upload': fd}
                resp = requests.post(self.API_URL, files=file_bin, data={'api_key': self.API_KEY, 'action': 'upload'})
                if 'Success' in resp.text:
                    return resp.text.split(' - ')[1]
                else:
                    return False
        except FileNotFoundError as err:
            print('Problem with Uploading File: ' + err.strerror)

    def gettypeslatest(self):
        """

        :return:
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'gettypes'})

    def getapilimit(self):
        """

        :return:
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'getlimit'}, 'raw')