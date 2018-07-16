from unittest import TestCase, main

import click
from click.testing import CliRunner

from __main__ import cli


class TestCli(TestCase):

    def test_hello(self):
         runner = CliRunner()
         result = runner.invoke(cli, ['Peter'])
         assert result.exit_code == 0
         assert result.output == 'Hello Peter!\n'


class TestDownload(TestCase):
    pass


if __name__ == '__main__':
    main()
