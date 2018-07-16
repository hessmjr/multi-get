import click
import urlparse
import validators


class URL(click.ParamType):
    """
    Class used to validate and build URLs for requesting
    """

    name = 'url'

    def convert(self, value, param, ctx):
        """
        Overriden method for validation of user argument.
        """
        # validate the URL with 'validators' library
        if not validators.url(value):
            self.fail('incomplete URL (%s).' % value, param, ctx)

        # check if URL using correct protocol with urlparse library
        parsed = urlparse.urlparse(value)
        if parsed.scheme not in ('http'):
            self.fail('invalid URL protocol (%s).  Only HTTP is '
                      'allowed' % parsed.scheme, param, ctx)
        return value


def validate_num(ctx, param, value):
    """
    Validates the value for the number of chunks.  Requirements:
        - integer
        - value greater than 0
        - value less than 100
    """
    if not isinstance(value, (int, long)):
        raise click.BadParameter('Should be an integer.')
    if not (value > 0 and value < 100):
        raise click.BadParameter('Should be between 0 and 100.')
    return value


def validate_size(ctx, param, value):
    """
    Validates the value for file sizes.  Requirements:
        - integer
        - value greater than 0
    """
    if not isinstance(value, (int, long)):
        raise click.BadParameter('Should be an integer.')
    if not value > 0:
        raise click.BadParameter('Should be greater than 0.')
    return value


def is_number(s):
    """
    Python Central's recommended quickest and easist number validation
    """
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
