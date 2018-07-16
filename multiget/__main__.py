import sys, os
import click
import requests

from cli_tools import URL, validate_num, validate_size, is_number
from download import Request, BYTES


# use click library to build command line interface arguments and options
#   - 1 argument and 3 options (number of chunks, size of chunks, total size)
#   - URL argument required for download
#   - number of chunks default to 4, validated
#   - size of chunks default to 1, validated
#   - total file size not default, overwrites the size of chunks if so
@click.command()
@click.argument('url', required=True, type=URL())
@click.option('--num', default=4, show_default=True, callback=validate_num,
              help='Number of file chunks')
@click.option('--size', default=1, show_default=True, callback=validate_size,
              help='File chunk size, in MiB')
@click.option('--total', metavar='INTEGER',
              help='Total file download size, in MiB.  Overrides size of the '
              'download chunks, if specified.')
@click.option('--verbose', is_flag=True, help='Turn on logging')
@click.version_option()


def main(url, num, size, total, verbose):
    """
    Retrieves a file from the given URL.  URL must be valid format.  File
    retrieved in chunks, range and size of chunks can be specified.
    """
    req = requests.head(url)
    print int(req.headers['content-length'])

    # if total specified then override chunk size
    if total is not None:

        # first ensure value is an integer and convert
        if not is_number(total):
            raise click.BadParameter('Should be a number.',
                                     param_hint=['--total'])
        total = int(total)

        # if user specified negative number then request is for entire file
        if total < 0:
            req = requests.head(url)
            total = int(req.headers['content-length'])

        # set the chunk size, increase by num chunks for rounding error
        size = (int(total) / int(num)) + int(num)

    # otherwise estimate the total size of the file download
    else:
        total = size * num
        size *= BYTES

    if verbose:
        click.echo('Requesting URL: %s' % url)
        click.echo('Number of chunks: %s' % num)
        click.echo('Size of chunks: %s' % size)
        click.echo('Estimated total: %s' % total)

    request = Request(url, num, size, verbose)
    request.get()
    print 'File download complete.'


# entry point for file, also sets up the relative python file location
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    main()
