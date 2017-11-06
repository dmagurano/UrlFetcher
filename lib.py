import argparse
import re
import os
import sys
from urllib.parse import urljoin
import requests
from exceptions import PageLoadError, ImageDownloadError, DirectoryAccessError, DirectoryCreateError


class UrlFetcher(object):
    """Fetcher class."""

    def __init__(self):
        self.url = None
        self.save_dir = None
        self.url_file = None
        self.page_html = None
        self.format_list = ["jpg", "png", "gif", "svg", "jpeg"]
        self.images = None
        self.n_to_download = 0

    def get_arguments(self):
        """ Gets the arguments from the command line. """

        parser = argparse.ArgumentParser(
            description='Downloads images from given URL and store links to a file')

        parser.add_argument('url', nargs=1, help="URL to fetch")
        parser.add_argument('-s', '--save-dir', type=str, default="Images",
                            help="Directory in which images should be saved")
        parser.add_argument('-f', '--file', type=str, default="Links.txt",
                            help="Name of the file to store images URL")
        args = parser.parse_args()

        self.url = args.url[0]
        if not re.match(r'^[a-zA-Z]+://', self.url):
            self.url = 'http://' + self.url

        self.save_dir = os.path.join(os.getcwd(), args.save_dir)

        if args.file.lower().endswith('.txt'):
            self.url_file = args.file
        else:
            self.url_file = args.file + ".txt"

        return self.url, self.url_file, self.save_dir

    def get_html(self):
        """ Downloads HTML content of page given the url"""
        try:
            page = requests.get(self.url)
            if page.status_code != 200:
                raise PageLoadError(page.status_code)
        except requests.exceptions.ConnectionError:
            raise PageLoadError(None)

        self.page_html = page.text
        return self.page_html

    def get_image_list(self):
        """ Gets list of images from the page_html. """
        pat = re.compile(r'<img [^>]*src="([^"]+)')
        pat2 = re.compile(r'<a [^>]*href="([^"]+)')
        img = pat.findall(self.page_html)
        links = pat2.findall(self.page_html)
        img_list = self.process_links(img)
        img_links = self.process_links(links)
        img_list.extend(img_links)

        images = [urljoin(self.url, img_url) for img_url in img_list]

        images = list(set(images))
        self.images = images
        self.n_to_download = len(images)
        return self.images

    def process_links(self, links):
        """ Function to process the list of links and filter images links."""
        links_list = []
        for link in links:
            if os.path.splitext(link)[1][1:].strip().lower() in self.format_list:
                links_list.append(link)
        return links_list

    def check_save_dir(self):
        """ Checks if the path exists and the fetcher has
            write permissions.
        """
        if os.path.isdir(self.save_dir):
            if not os.access(self.save_dir, os.W_OK):
                raise DirectoryAccessError
        elif os.access(os.path.dirname(self.save_dir), os.W_OK):
            try:
                os.makedirs(self.save_dir)
            except FileExistsError:
                sys.exit(
                    "A file with the same name as the folder already exists, please use a different filename")
        else:
            raise DirectoryCreateError
        return True

    def download_all_images(self):
        failed_count = 0
        total_counter = 0

        for img_url in self.images:
            try:
                self.download_image(img_url)
            except ImageDownloadError:
                failed_count += 1
            total_counter += 1
            update_progress(total_counter / self.n_to_download)

    def download_image(self, img_url):
        """ Downloads a single image.
            Also, raises the appropriate exception if required.
        """
        img_request = None
        try:
            img_request = requests.request(
                'get', img_url, stream=True)
            if img_request.status_code != 200:
                raise ImageDownloadError(img_request.status_code)
        except:
            raise ImageDownloadError()

        img_content = img_request.content
        with open(os.path.join(self.save_dir, img_url.split('/')[-1]), 'wb') as f:
            byte_image = bytes(img_content)
            f.write(byte_image)
        return True

    def write_url_file(self):
        with open(self.url_file, "w") as f:
            for item in self.images:
                f.write("{}\n".format(item))


# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 10  # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength * progress))
    text = "\rPercent: [{0}] {1}% {2}".format("#" * block + "-" * (barLength - block), progress * 100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
