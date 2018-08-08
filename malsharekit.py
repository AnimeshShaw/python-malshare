# coding: utf-8
# !/usr/bin/env python
import argparse
import json
import os
import sys

from malshare import Malshare

__author__ = 'Animesh Shaw aka Psycho_Coder'
__version__ = '1.0'

title = """
              _     _                            _ _   
  /\/\   __ _| |___| |__   __ _ _ __ ___    /\ /(_) |_ 
 /    \ / _` | / __| '_ \ / _` | '__/ _ \  / //_/ | __|
/ /\/\ \ (_| | \__ \ | | | (_| | | |  __/ / __ \| | |_ 
\/    \/\__,_|_|___/_| |_|\__,_|_|  \___| \/  \/|_|\__|
                            
            CLI interface to interact with Malshare API
            Developed By: Animesh Shaw <Psycho_Coder>
            Email: coder@animeshshaw.com 
            Twitter: @Psycho__Coder                     
"""


def main():
    """
    Main Method and UI/CLI for the Python-Malshare.
    """
    print(title)
    desc = 'Complete implementation of the Malshare API and a toolkit to interact with it'

    parser = argparse.ArgumentParser(description=desc, prog='malsharekit.py')
    parser.add_argument('-k', '--apikey', type=str, required=True, help='Malshare API Key.')
    parser.add_argument('-l', '--dir', type=str,
                        help="Directory location to save the samples data as json. By default, "
                             "stored in the current directory.")
    parser.add_argument('--save', '--save', action='store_true',
                        help='Save the results in a file in the current directory.')
    parser.add_argument('-gl', '--latest', action='store_true', help='List hashes from the past 24 hours')
    parser.add_argument('-gtl', '--typelist', type=str, help='List MD5/SHA1/SHA256 hashes of a specific type from '
                                                             'the past 24 hours. Sample File Types: C, XML, PHP, HTML, '
                                                             'ASCII, PE-32, PE32, ISO-8859, UTF-8, MSVC, Composite, '
                                                             'data, 80386, current, BSD, Zip, 7-zip')
    parser.add_argument('-gtl24', '--typelist24', action='store_true',
                        help='Get list of file types & count from the past 24 hours')
    parser.add_argument('-gs', '--sources', action='store_true', help='List of sample sources from the past 24 hours')
    parser.add_argument('-d', '--download', type=str, help='Provide the malware hash to download the sample.')
    parser.add_argument('-i', '--details', type=str, help='Provide the malware hash to get the stored file details.')
    parser.add_argument('-u', '--upload', type=str,
                        help='Upload a Malware Sample to Malshare. Provide the file location.')
    parser.add_argument('-s', '--search', type=str, help='Search Malshare for different Malware Samples/Signatures.')
    parser.add_argument('-al', '--apilimit', action='store_true',
                        help='GET allocated number of API key requests per day and remaining')

    args = parser.parse_args()

    SAVE_LOC = ''

    ms_obj = Malshare(args.apikey)

    if args.dir and args.save:
        print('Options --save and --dir cannot be used together.')
        sys.exit()

    if args.save:
        SAVE_LOC = os.getcwd()

    if args.dir:
        SAVE_LOC = args.dir
        if os.path.isdir(SAVE_LOC):
            SAVE_LOC = os.path.abspath(args.dir)
        else:
            print('Save location doesn\'t exist or not a directory')
            sys.exit()

    if args.latest:
        print('\nFetching the List hashes from the past 24 hours...')
        RESP_DATA = ms_obj.getlist()
        if args.save or args.dir:
            print('\nNow Writing the data to a file...')
            SAVE_LOC = os.path.join(SAVE_LOC, "latest-24hrs.json")
            write_to_file(RESP_DATA, SAVE_LOC)
        else:
            print(json.dumps(RESP_DATA, indent=4, sort_keys=True))

    if args.typelist:
        print('\nFetching the List hashes of type "{0}"'.format(args.typelist))
        RESP_DATA = ms_obj.getfiletypelist(args.typelist)
        if RESP_DATA:
            if args.save or args.dir:
                print('\nNow Writing the data to a file...')
                SAVE_LOC = os.path.join(SAVE_LOC, "type-list-{0}.json".format(args.typelist))
                write_to_file(RESP_DATA, SAVE_LOC)
            else:
                print(json.dumps(RESP_DATA, indent=4, sort_keys=True))
        else:
            print('No hashes found for "{0}"'.format(args.typelist))

    if args.typelist24:
        print('\nFetching list of file types & count from the past 24 hours...')
        RESP_DATA = ms_obj.gettypeslatest()
        if args.save or args.dir:
            print('\nNow Writing the data to a file...')
            SAVE_LOC = os.path.join(SAVE_LOC, "type-list-latest-24hrs.json")
            write_to_file(RESP_DATA, SAVE_LOC)
        else:
            print(json.dumps(RESP_DATA, indent=4, sort_keys=True))

    if args.sources:
        print('\nFetching the Sample Sources from the past 24 hours...')
        RESP_DATA = ms_obj.getsources()
        if args.save or args.dir:
            print('\nNow Writing the data to a file...')
            SAVE_LOC = os.path.join(SAVE_LOC, "sources-latest-24hrs.json")
            write_to_file(RESP_DATA, SAVE_LOC)
        else:
            print(json.dumps(RESP_DATA, indent=4, sort_keys=True))

    if args.download:
        if args.save or args.dir:
            print('\nDownload the Sample with the Hash: {0}'.format(args.download))
            SAVE_LOC = os.path.join(SAVE_LOC, args.download)
            status = ms_obj.getfile(args.download, SAVE_LOC)
            if status:
                print('\nSample Downloaded Successfully. Location: ' + SAVE_LOC)
            else:
                print('\nUnable to Download Malware Sample.')
        else:
            print('\nSave location must be provided.')

    if args.details:
        print('\nGetting Details for Hash: {0}'.format(args.details))
        RESP_DATA = ms_obj.getfiledetails(args.details)
        if args.save or args.dir:
            print('\nNow Writing the data to a file...')
            SAVE_LOC = os.path.join(SAVE_LOC, "details-{0}.json".format(args.details))
            write_to_file(RESP_DATA, SAVE_LOC)
        else:
            print(json.dumps(RESP_DATA, indent=4, sort_keys=True))

    if args.upload:
        if os.path.exists(args.upload):
            print('\nUploading File: {0}'.format(os.path.basename(args.upload)))
            RESP_DATA = ms_obj.upload_file(os.path.abspath(args.upload))
            if RESP_DATA is not False:
                print('\nFile Uploaded Successfully')
                print('\nURL: https://malshare.com/sample.php?action=detail&hash={0}'.format(RESP_DATA))
            else:
                print('\nUnable to Upload Sample to Malshare.com')

    if args.search:
        print('\nSearching Malshare for : {0}'.format(args.search))
        RESP_DATA = ms_obj.search(args.search)
        if args.save or args.dir:
            print('\nNow Writing the data to a file...')
            SAVE_LOC = os.path.join(SAVE_LOC, "search-results-{0}.json".format(args.search))
            write_to_file(RESP_DATA, SAVE_LOC)
        else:
            print(json.dumps(RESP_DATA, indent=4, sort_keys=True))

    if args.apilimit:
        if args.save or args.dir:
            print('--save/--dir is not allowed with --apilimit/-al argument')
            sys.exit()
        else:
            print('API Requests Stats: ' + ms_obj.getapilimit())


def write_to_file(data, save_loc):
    try:
        with open(save_loc, 'w') as fd:
            json.dump(data, fd, indent=4)
            print('\nNew File Created: ' + save_loc)
    except PermissionError as err:
        print('\nNo Directory Write Permission: ' + err.strerror)


if __name__ == '__main__':
    sys.exit(main())