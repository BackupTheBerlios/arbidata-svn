import recordparser
import struct
import unittest

class KnownValues(unittest.TestCase):
    def setUp(self):
        """
        Initialize the known parameters to filechunker and create the temporary
        data file.
        """
        # $TODO - expand supported field types
        # NOTE: For the purposes of this test, don't expect to compare 'f'-type
        # floats!  The precision conversion using struct.pack -> struct.unpack
        # is problematic!  Use 'd' instead because Python floats are actually
        # C-doubles.  Use '=d' if necessary.
        int1 = -10
        uint1 = 20
        string1 = "This is a string"  # pack this as a 30-byte string
        char1 = "J"
        short1 = 0
        float1 = 5.23
        double1 = -256.3456789107
        ushort1 = 5
        string2 = "This is another string"  # pack this as a 30-byte string
        long1 = 2147483647
        ulong1 = 3000000000

        # Use the fields above in this order.
        self.fieldmap = "iI30schddH30slL"
        self.sourcekeys = ("int1", "uint1", "string1", "char1", "short1",
                "float1", "double1", "ushort1", "string2", "long1", "ulong1")

        # Create the raw data that getfields will parse
        self.rawdata = struct.pack(self.fieldmap, int1, uint1, string1, char1,
                short1, float1, double1, ushort1, string2, long1, ulong1)

        # This is what getfields should return
        self.knownvalues = {"char1":char1, "short1":short1, "ushort1":ushort1,
                "int1":int1, "uint1":uint1, "long1":long1, "ulong1":ulong1,
                "float1":float1, "double1":double1, "string1":string1,
                "string2":string2}

    def tearDown(self):
        pass

    def test_getknowndata(self):
        """getfields should give known result with known input"""
        result = recordparser.getfields(self.rawdata, self.fieldmap,
                self.sourcekeys)
        self.assertEqual(self.knownvalues, result)


class BadInput(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_toomanykeys(self):
        """getfields should fail if passed too many keys"""
        self.assertRaises(recordparser.KeyListMismatchError,
                recordparser.getfields, "1234567890", "10s", ("key1", "key2"))

    def test_toofewkeys(self):
        """getfields should fail if passed too few keys"""
        self.assertRaises(recordparser.KeyListMismatchError,
                recordparser.getfields, "1234567890", "10s", ())


if __name__ == "__main__":
    unittest.main()
