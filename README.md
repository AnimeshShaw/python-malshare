# python-malshare
Complete implementation of the [Malshare API](https://malshare.com/doc.php) and a toolkit to interact with it.

## Malshare Kit - Help Options
```text

C:\Users\Psycho_Coder\Documents\GitHub\python-malshare>python malsharekit.py --help

              _     _                            _ _
  /\/\   __ _| |___| |__   __ _ _ __ ___    /\ /(_) |_
 /    \ / _` | / __| '_ \ / _` | '__/ _ \  / //_/ | __|
/ /\/\ \ (_| | \__ \ | | | (_| | | |  __/ / __ \| | |_
\/    \/\__,_|_|___/_| |_|\__,_|_|  \___| \/  \/|_|\__|

            CLI interface to interact with Malshare API
            Developed By: Animesh Shaw <Psycho_Coder>
            Email: coder@animeshshaw.com
            Twitter: @Psycho__Coder

usage: main.py [-h] -k APIKEY [-l DIR] [--save] [-gl] [-gtl TYPELIST] [-gtl24]
               [-gs] [-d DOWNLOAD] [-i DETAILS] [-u UPLOAD] [-s SEARCH] [-al]

Complete implementation of the Malshare API and a toolkit to interact with it

optional arguments:
  -h, --help            show this help message and exit
  -k APIKEY, --apikey APIKEY
                        Malshare API Key.
  -l DIR, --dir DIR     Directory location to save the samples data as json.
                        By default, stored in the current directory.
  --save, --save        Save the results in a file in the current directory.
  -gl, --latest         List hashes from the past 24 hours
  -gtl TYPELIST, --typelist TYPELIST
                        List MD5/SHA1/SHA256 hashes of a specific type from
                        the past 24 hours. Sample File Types: C, XML, PHP,
                        HTML, ASCII, PE-32, PE32, ISO-8859, UTF-8, MSVC,
                        Composite, data, 80386, current, BSD, Zip, 7-zip
  -gtl24, --typelist24  Get list of file types & count from the past 24 hours
  -gs, --sources        List of sample sources from the past 24 hours
  -d DOWNLOAD, --download DOWNLOAD
                        Provide the malware hash to download the sample.
  -i DETAILS, --details DETAILS
                        Provide the malware hash to get the stored file
                        details.
  -u UPLOAD, --upload UPLOAD
                        Upload a Malware Sample to Malshare. Provide the file
                        location.
  -s SEARCH, --search SEARCH
                        Search Malshare for different Malware
                        Samples/Signatures.
  -al, --apilimit       GET allocated number of API key requests per day and
                        remaining
```

## Sample Usage

__1. Get List hashes from the past 24 hours__

```text
python malsharekit.py --apikey <Your-Key-Here> -gl
```

The Above will print the data to the console. Use `--save` to store them in the current directory or `--dir` to 
save the data in a custom location (must be directory).

```text
python malsharekit.py --apikey <Your-Key-Here> --save -gl
```

or 

```text
python malsharekit.py --apikey <Your-Key-Here> --dir /home/myuser/data -gl
```

__2. Downloading a Sample from Malshare__

```text
python malsharekit.py --apikey <Your-Key-Here> --save -d d25ca94d2e43d0b8addca830297e169f
```

##Contact

_Email:_ coder[at]animeshshaw[dot]com

_Twitter:_ https://twitter.com/Psycho__Coder

## License
This software is under [MIT License](https://en.wikipedia.org/wiki/MIT_License)