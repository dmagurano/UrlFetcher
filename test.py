import unittest
import os
import httpretty
from exceptions import PageLoadError
from lib import UrlFetcher

# Absolute path to http_resources dir.
HTTP_RESOURCES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'http_resources')


class UrlFetcherTest(unittest.TestCase):
    def setUp(self):
        self.fetcher = UrlFetcher()
        self.resources = {'site': 'http://github.com/contact',
                          'file': 'github.html',
                          'result': {'https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif',
                                     'https://assets-cdn.github.com/images/modules/contact/heartocat.png'}}
        httpretty.enable()
        with open(os.path.join(HTTP_RESOURCES_PATH, self.resources['file'])) as html:
            self.actual_html = html.read()
        httpretty.register_uri(httpretty.GET, self.resources['site'], body=self.actual_html)

    def test_get_image_list(self):
        self.fetcher.url = self.resources['site']
        self.fetcher.get_html()
        links = self.fetcher.get_image_list()
        self.assertSetEqual(set(links), self.resources['result'], "Test HTML page image link parsing")

    def test_get_html_200(self):
        self.fetcher.url = self.resources['site']
        self.fetcher.get_html()
        self.assertEqual(self.fetcher.page_html, self.actual_html)

    def test_get_html_404(self):
        httpretty.register_uri(httpretty.GET, 'http://404test.com', body="error", status=404)
        try:
            self.fetcher.url = 'http://404test.com'
            self.fetcher.get_html()
        except PageLoadError as e:
            self.assertEqual(e.status_code, 404)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()
        del self.resources
        del self.fetcher


if __name__ == '__main__':
    unittest.main()
