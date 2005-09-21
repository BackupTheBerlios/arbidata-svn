"""Read n-size records from a binary file"""


class FileChunkerError(Exception): pass
class InvalidFileSizeError(FileChunkerError): pass


def getrecords(filename, recordsize):
    """Open the specified file and return the records in a list"""
    records = []
    # Read the whole file
    infile = open(filename, "rb").read()
    # Make sure it's the right size
    if len(infile) % recordsize > 0:
        raise InvalidFileSizeError
    # Slice up infile into recordsize-sized chunks
    for x in range(len(infile) / recordsize):
        records.append(infile[(x * recordsize):(x * recordsize + recordsize)])
    return records
