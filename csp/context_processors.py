from django.utils.encoding import smart_text
from django.utils.functional import lazy
from django.utils import six
from csp.middleware import get_nonce

def csp(request):
    """
    Context processor that provides a CSP nonce, or the string 'NOTPROVIDED' if
    it has not been provided by the middleware
    """
    def _get_val():
        nonce = get_nonce(request)
        if nonce is None:
            # We could fail here in a way that forces resolution to ensure
            # nonce is working. As things stand, inlines that use nonce will
            # just be seen as violations.
            return 'NOTPROVIDED'
        else:
            return smart_text(nonce)
    _get_val = lazy(_get_val, six.text_type)

    return {'csp_nonce': _get_val()}
