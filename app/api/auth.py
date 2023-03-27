import functools
import os

from flask import request, abort


def token_required(view):
    """
    Authentication checker decorator
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        headers = request.headers
        auth = headers.get('X-Api-Key')
        if auth != os.environ.get('X-Api-Key'):
            abort(401)

        return view(**kwargs)

    return wrapped_view

