import numpy as np
import json
from base64 import b32encode
from hashlib import sha1

def hashablize(obj):
    try:
        hash(obj)
    except TypeError:
        if isinstance(obj, dict):
            return tuple((k, hashablize(v)) for (k, v) in sorted(obj.items()))
        elif isinstance(obj, np.ndarray):
            return tuple(obj.tolist())
        elif hasattr(obj, '__iter__'):
            return tuple(hashablize(o) for o in obj)
        else:
            raise TypeError("Can't hashablize object of type %r" % type(obj))
    else:
        return obj

class NumpyJSONEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types
    Edited from mpl3d: mpld3/_display.py
    """

    def default(self, obj):
        try:
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return [self.default(item) for item in iterable]
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def deterministic_hash(thing, length=10):
    """Return a base32 lowercase string of length determined from hashing
    a container hierarchy
    """
    hashable = hashablize(thing)
    jsonned = json.dumps(hashable, cls=NumpyJSONEncoder)
    digest = sha1(jsonned.encode('ascii')).digest()
    return b32encode(digest)[:length].decode('ascii').lower()

