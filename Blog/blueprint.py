from flask import Blueprint


def create_api_blueprint(name, package_name, **kwargs):

    url_prefix = kwargs.pop('url_prefix', '/')
    url_prefix = '{url_prefix}'.format(url_prefix=url_prefix)

    blueprint_name = '{name}'.format(name=name)
    return _create_bp(blueprint_name, package_name,
                      url_prefix=url_prefix, **kwargs)


def _create_bp(name, package_name, **kwargs):
    """Create blueprint"""

    url_prefix = kwargs.pop('url_prefix', '')

    bp = Blueprint(
        name, package_name,
        url_prefix=url_prefix,
        **kwargs)

    return bp
