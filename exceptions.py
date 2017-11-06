class PageLoadError(Exception):
    """ Exception to be raised when the page can't be loaded. """
    status_code = 0

    def __init__(self, status_code):
        super(PageLoadError, self).__init__()
        self.status_code = status_code

class ImageDownloadError(Exception):
    """ Exception to be raised when the imace can't be downloaded. """
    status_code = 0

    def __init__(self, status_code=0):
        super(ImageDownloadError, self).__init__()
        self.status_code = status_code

class DirectoryAccessError(Exception):
    """ Exception to be raised when the directory can't be accessed. """
    pass


class DirectoryCreateError(Exception):
    """ Exception to be raised when the directory can't be created. """
    pass