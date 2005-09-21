import filechunker
import unittest
from os import remove

"""
- filechunker error conditions
    - should test for
        - unusually-sized data files
            - headers? footers?
                - might-should break up the data file in header-data-footer chunks
                  first?
            - incomplete files
    - might not need to test for
        - normal file errors
            - data file does not exist
            - can't open file
"""


class KnownValues(unittest.TestCase):
    """Validate the normal functionality of filechunker"""

    def setUp(self):
        """
        Initialize the known parameters to filechunker and create a temporary
        data file that contains good data.
        """
        # We will re-use the knownvalues later to make sure the filechunker
        # parses the bin-file correctly.
        self.knownvalues = []
        self.filename = "testgood.dat"
        self.recordsize = 50  # in bytes
        for i in range(7):
            self.knownvalues.append("".join([str(i) for x in
                range(self.recordsize)]))
        tempfile = open(self.filename, "wb")
        tempfile.write("".join(self.knownvalues))
        tempfile.close()

    def tearDown(self):
        """Clean up the temporary file"""
        remove(self.filename)

    def test_getknowndata(self):
        """getrecords should give known result with known input"""
        result = filechunker.getrecords(self.filename, self.recordsize)
        self.assertEqual(self.knownvalues, result)


class BadInput(unittest.TestCase):
    """Ensure that filechunker throws appropriate exceptions"""

    def setUp(self):
        """
        Initialize the known parameters to filechunker and create a temporary
        data file with an invalid file size.

        This covers such cases as incomplete records, a header and/or footer
        that is not the same byte-size as a record, extraneous trailing data.
        Note that filechunker is not expected to understand other logical
        inconsistencies in the data.  All it does is chunk up a file into
        n-size records.
        """
        self.filename = "testbad.dat"
        self.recordsize = 10
        tempfile = open(self.filename, "wb")
        tempfile.write("BAD")
        tempfile.close()

    def tearDown(self):
        """Clean up the temporary file"""
        remove(self.filename)

    def test_baddatafile(self):
        """getrecords should fail when opening a file with invalid size"""
        self.assertRaises(filechunker.InvalidFileSizeError, filechunker.getrecords,
                self.filename, self.recordsize)


if __name__ == "__main__":
    unittest.main()
