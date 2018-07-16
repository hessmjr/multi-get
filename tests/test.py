import unittest
import os
import click
from click.testing import CliRunner

from multiget.__main__ import cli
from multiget.download import Request, parse_filename


class TestDownload(unittest.TestCase):

    def test_filename_parse_good(self):
        url = 'http://httpbin.org/image/jpeg'
        filename = 'jpeg'
        assert filename == parse_filename(url)

    def test_filename_parse_good_extension(self):
        url = 'http://httpbin.org/image/something.png'
        filename = 'something.png'
        assert filename == parse_filename(url)

    def test_filename_none_present(self):
        url = 'http://httpbin.org/'
        filename = 'index.html'
        assert filename == parse_filename(url)

    def test_good_url_request(self):
        request = Request('http://httpbin.org/image/jpeg')
        request.get()
        filepath = os.path.join(os.getcwd(), 'jpeg')
        assert os.path.isfile(filepath)




class TestCli(unittest.TestCase):
    pass
    # def test_good_url(self):
    #      runner = CliRunner()
    #      result = runner.invoke(cli, ['http://httpbin.org/image/jpeg'])
    #      assert result.exit_code == 0
    #      assert result.output == 'File download complete.\n'
    # http://ipv4.download.thinkbroadband.com/20MB.zip


if __name__ == '__main__':
    unittest.main()
