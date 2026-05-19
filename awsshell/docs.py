from __future__ import unicode_literals
from awsshell import db


def load_lazy_doc_index(filename):
    d = load_doc_db(filename)
    return DocRetriever(d)


def load_doc_db(filename):
    d = db.ConcurrentDBM.open(filename, create=True)
    return d


class DocRetriever(object):
    """Retrieve documentation for the AWS CLI."""
    def __init__(self, doc_index):
        # Internally, most of the speedup comes from
        # the fact that this data is pre-rendered and
        # indexed.
        self._doc_index = doc_index
        self._cache = {}


