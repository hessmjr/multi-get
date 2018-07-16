from unittest import TestCase, main

import click
from click.testing import CliRunner

from multiget.__main__ import cli
from multiget.download import Request, parse_filename


class TestCli(TestCase):

    def test_good_url(self):
         runner = CliRunner()
         result = runner.invoke(cli, ['https://httpbin.org/image/jpeg'])
         assert result.exit_code == 0
         assert result.output == 'File download complete.\n'


class TestDownload(TestCase):

    def test_filename_parse(self):
        url = 'https://httpbin.org/image/jpeg'
        filename = 'jpeg'

        assert filename == parse_filename(url)


if __name__ == '__main__':
    main()
