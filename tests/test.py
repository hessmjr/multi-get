import os
import unittest
import requests
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
        assert os.path.isfile(filepath), 'File not created'
        os.remove(filepath)

    def test_good_url_large_request(self):
        request = Request('http://ipv4.download.thinkbroadband.com/20MB.zip')
        request.get()
        filepath = os.path.join(os.getcwd(), '20MB.zip')
        assert os.path.isfile(filepath), 'File not created'
        assert os.path.getsize(filepath) == 4 * (BYTES ** 2), 'File wrong size'
        os.remove(filepath)
        assert 4 == len(request.threads), 'Wrong number threads created'

    def test_bad_url(self):
        request = Request('http://nothere.website/badurl.jpg')
        request.get()
        filepath = os.path.join(os.getcwd(), 'badurl.jpg')
        assert not os.path.isfile(filepath), 'File was created, not good'

    def test_good_url_large_request_download_all(self):
        # figure out how much of the file is supposed to be downloaded
        resp = requests.head('http://ipv4.download.thinkbroadband.com/20MB.zip')
        file_size = int(resp.headers['content-length'])
        num_chunk = 10
        chunk_size = (file_size / num_chunk) + num_chunk

        # setup the request and find the file that should be created
        request = Request('http://ipv4.download.thinkbroadband.com/20MB.zip',
                          num_chunk=num_chunk, chunk_size=chunk_size)
        request.get()
        filepath = os.path.join(os.getcwd(), '20MB.zip')

        # assert processed correctly
        assert os.path.isfile(filepath), 'File not created'
        assert os.path.getsize(filepath) == file_size, 'File wrong size'
        os.remove(filepath)
        assert num_chunk == len(request.threads), 'Wrong number threads created'


class TestCli(unittest.TestCase):

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert 0 == result.exit_code, 'Wrong exit code'
        assert 'Usage:' in result.output, 'Wrong output'

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        assert 0 == result.exit_code, 'Wrong exit code'
        assert 'version' in result.output, 'Wrong output'

    def test_bad_url(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['http://bad'])
        assert 2 == result.exit_code, 'Wrong exit code'
        assert 'incomplete URL' in result.output, 'Wrong output'

    def test_good_url(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['http://httpbin.org/image/jpeg'])
        filepath = os.path.join(os.getcwd(), 'jpeg')
        assert 0 == result.exit_code, 'Wrong exit code'
        assert 'File download complete' in result.output, 'Wrong output'
        assert os.path.isfile(filepath), 'File not created'
        os.remove(filepath)

    def test_entire_file_request(self):
        url = 'http://ipv4.download.thinkbroadband.com/20MB.zip'
        resp = requests.head(url)
        file_size = int(resp.headers['content-length'])

        # run process
        runner = CliRunner()
        result = runner.invoke(cli, [url, '--total=-1'])
        filepath = os.path.join(os.getcwd(), '20MB.zip')

        # assert processed correctly
        assert 0 == result.exit_code, 'Wrong exit code'
        assert 'File download complete' in result.output, 'Wrong output'
        assert os.path.isfile(filepath), 'File not created'
        assert os.path.getsize(filepath) == file_size, 'File wrong size'
        os.remove(filepath)

    def test_bad_num_input(self):
        url = 'http://httpbin.org/image/jpeg'
        runner = CliRunner()
        result = runner.invoke(cli, [url, '--num=0'])
        assert 2 == result.exit_code, 'Wrong exit code'
        assert 'Should be between 0 and 100' in result.output, 'Wrong output'

    def test_bad_size_input(self):
        url = 'http://httpbin.org/image/jpeg'
        runner = CliRunner()
        result = runner.invoke(cli, [url, '--size=0'])
        assert 2 == result.exit_code, 'Wrong exit code'
        assert 'Should be greater than 0' in result.output, 'Wrong output'

    def test_all_three_input(self):
        url = 'http://ipv4.download.thinkbroadband.com/5MB.zip'
        resp = requests.head(url)
        file_size = int(resp.headers['content-length'])

        # run process
        runner = CliRunner()
        result = runner.invoke(cli, [url, '--total=-1', '--size=2', '--num=5'])
        filepath = os.path.join(os.getcwd(), '5MB.zip')

        # assert processed correctly
        assert 0 == result.exit_code, 'Wrong exit code'
        assert 'File download complete' in result.output, 'Wrong output'
        assert os.path.isfile(filepath), 'File not created'
        assert os.path.getsize(filepath) == file_size, 'File wrong size'
        os.remove(filepath)


if __name__ == '__main__':
    unittest.main()
