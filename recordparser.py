"""
recordparser
- inputs
    - the raw record as a string full of bytes
    - the format string (per struct module)
        - we're going to try and use higher-level, fixed-length (in bytes)
          fields.  basically, a subset of ansi c types:
            - integer types:
        - OR, should we use the full set of ansi c types per struct?
            - probably this and let the user be aware of how to use it
              properly.
    - a list of names to use as keys
        - the number of names in the list must match the number of values that
          the format string parses out
        - the names must be in the correct order per the format string
- returns
    - a dictionary of all the fields in the records
"""

import struct


class RecordParserError(Exception): pass
class KeyListMismatchError(RecordParserError): pass


def getfields(rawdata, fieldmap, keylist):
    valuelist = struct.unpack(fieldmap, rawdata)
    valuelist = map(_map_fromcstring, valuelist)
    if len(valuelist) != len(keylist):
        raise KeyListMismatchError
    retval = dict(zip(keylist, valuelist))
    return retval

def _map_fromcstring(cstring):
    if type("") != type(cstring) or cstring.find("\0") == -1:
        return cstring
    else:
        return cstring[0:cstring.find("\0")]
