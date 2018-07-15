import sys, os
import click

from cli_tools import URL, validate_num, validate_size
from download import Request


# use click library to build command line interface arguments and options
#   - 1 argument and 3 options (number of chunks, size of chunks, total size)
#   - URL argument required for download
#   - number of chunks default to 4, validated
#   - size of chunks default to 1, validated
#   - total file size not default, overwrites the number of chunks if so
@click.command()
@click.argument('url', required=True, type=URL())
@click.option('--num', default=4, show_default=True, callback=validate_num,
              help='Number of file chunks')
@click.option('--size', default=1, show_default=True, callback=validate_size,
              help='File chunk size, in MiB')
@click.option('--total', metavar='INTEGER',
              help='Total file download size, in MiB.  Overrides number of '
              'chunks if specified.')
@click.version_option()


def main(url, num, size, total):
    """
    Retrieves a file from the given URL.  URL must be valid format.  File
    retrieved in chunks, range and size of chunks can be specified.
    """

    # if total specified then override number of chunks
    if total is not None:
        validate_size(total)
        num = total / size

    # TODO filler for now, replace with GET logic .......................................
    click.echo('num: %s' % num)
    click.echo('size: %s' % size)
    click.echo('total: %s' % total)
    click.echo('url: %s' % repr(url))


# entry point for file, also sets up the relative python file location
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    main()
