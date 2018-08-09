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
        Base Method to query to Malshare API server for different options.

        :param payload: API Request Parameters
        :param output: Output Format - JSON or RAW
        :return: Response
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
        List hashes from the past 24 hours

        :return: Response as JSON
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'getlist'})

    def getlistraw(self):
        """
        List hashes from the past 24 hours

        :return: Response as RAW Text
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'getlistraw'}, 'raw')

    def getsources(self):
        """
        List of sample sources from the past 24 hours

        :return: Response as JSON
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'getsources'})

    def getsourcesraw(self):
        """
        List of sample sources from the past 24 hours

        :return: Response as RAW Text
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'getsourcesraw'}, 'raw')

    def getfiledetails(self, file_hash, output='json'):
        """
        GET stored sample file details

        :param file_hash: Sample Hash
        :param output: Type of Output - JSON or RAW
        :return: Response as JSON
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'details', 'hash': file_hash}, output)

    def validate_hash(self, file_hash):
        """
        Check if a sample hash is valid or not.

        :param file_hash: Sample Hash to check
        :return: True if hash is present else False.
        """
        return self.getfiledetails(file_hash, 'raw') != 'Invaid Hash'

    def getfile(self, file_hash, save_loc):
        """
        Method to download a sample from Malshare

        :param file_hash: Hash of the sample file to be downloaded.
        :param save_loc: Directory to save the file.
        :return: True is Download was successful else False.
        """
        if self.validate_hash(file_hash):
            self._download_file_({'api_key': self.API_KEY, 'action': 'getfile', 'hash': file_hash}, file_hash)
            return True
        return False

    def getfiletypelist(self, file_type):
        """
        List MD5/SHA1/SHA256 hashes of a specific type from the past 24 hours

        Sample File Types: C, XML, PHP, HTML, ASCII, PE-32, PE32, ISO-8859, UTF-8, MSVC, Composite,
                        data, 80386, current, BSD, Zip, 7-zip

        :param file_type: Type of Sample Type (See sample types above)
        :return: Response as JSON
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'type', 'type': file_type})

    def search(self, query):
        """
        Search sample hashes, sources and file names

        :param query: Search Query
        :return: Response as RAW Text
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'search', 'query': query}, 'raw')

    def upload_file(self, file_path):
        """
        Upload a Sample tp Malshare

        :param file_path: File to share
        :return: Hash of uploaded file is successful else False.
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
        Get list of file types & count from the past 24 hours

        :return: Response as JSON
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'gettypes'})

    def getapilimit(self):
        """
        GET allocated number of API key requests per day and remaining

        :return: Response as RAW Text
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'getlimit'}, 'raw')
