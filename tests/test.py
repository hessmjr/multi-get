import unittest
import os
import click
from click.testing import CliRunner

from multiget.__main__ import cli
from multiget.download import Request, parse_filename, BYTES


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
        os.remove(filepath)

    def test_good_url_large_request(self):
        request = Request('http://ipv4.download.thinkbroadband.com/20MB.zip')
        request.get()
        filepath = os.path.join(os.getcwd(), '20MB.zip')
        assert os.path.isfile(filepath)
        assert os.path.getsize(filepath) == 4 * (BYTES ** 2)
        os.remove(filepath)

    def test_bad_url(self):
        request = Request('http://nothere.website/badurl.jpg')
        request.get()
        filepath = os.path.join(os.getcwd(), 'badurl.jpg')
        assert not os.path.isfile(filepath)


class TestCli(unittest.TestCase):

    # def test_good_url(self):
    #      runner = CliRunner()
    #      result = runner.invoke(cli, ['http://httpbin.org/image/jpeg'])
    #      assert result.exit_code == 0
    #      assert result.output == 'File download complete.\n'
    # http://ipv4.download.thinkbroadband.com/20MB.zip

    def test_help(self):
        pass

    def test_version(self):
        pass

    def test_bad_url(self):
        pass

    def test_good_url(self):
        pass

    def test_entire_file_request(self):
        pass


if __name__ == '__main__':
    unittest.main()
