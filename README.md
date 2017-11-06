UrlFetcher
==========
Downloads images from given URL and store links to a file

Built using Python v3.6.1
#### Dependencies ####
UrlFetcher depends upon ``requests``

``httpretty`` is used for testing

Usage
-----
```sh
$ python url-fetcher.py [-h] [-s SAVE_DIR] [-f FILE] url
```

Options
-------

```sh
positional arguments:
  url                   URL to fetch

optional arguments:
  -h, --help            show this help message and exit
  -s SAVE_DIR, --save-dir SAVE_DIR
                        Directory in which images should be saved
  -f FILE, --file FILE  Name of the file to store images URL
  ```