import sys
from exceptions import PageLoadError, DirectoryAccessError, DirectoryCreateError
from lib import UrlFetcher


def main():
    try:
        console_main()
    except KeyboardInterrupt:
        print("Program stopped by user.")


def console_main():
    """ This function handles all the console action. """

    fetcher = UrlFetcher()
    fetcher.get_arguments()
    print("Requesting webpage...")

    try:
        fetcher.get_html()
    except PageLoadError as err:
        if err.status_code is None:
            print("UrlFetcher is unable to access the page.")
        else:
            print("Page failed to load. Status code: {0}".format(err.status_code))
        sys.exit()

    fetcher.get_image_list()
    if len(fetcher.images) == 0:
        sys.exit("Sorry, no images found.")

    print("Found {0} images ".format(len(fetcher.images)))

    try:
        fetcher.check_save_dir()
    except DirectoryAccessError:
        print("Sorry, the directory can't be accessed.")
        sys.exit()
    except DirectoryCreateError:
        print("Sorry, the directory can't be created.")
        sys.exit()

    print("Downloading all images...")
    fetcher.download_all_images()

    print("Writing url file...")
    fetcher.write_url_file()


    print("\nDone")


if __name__ == "__main__":
    main()