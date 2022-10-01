"""Tests for `myproject/process/math`."""

import myproject.process as process
import unittest

class TestMath(unittest.TestCase):
    """bubblebox unit test for create"""

    def setUp(self):
        """
        Runs before each test
        """
        pass

    def test_integers(self):

        a,b = [1,2]
        c   = 3

        # parent class method
        self.assertEqual(c,process.math.addvalues(a,b),'Integer test failed')

        print("Intergers can be added\n")

    def test_floats(self):

        a,b = [1.5,2.8]
        c   = 4.3

        self.assertEqual(c,process.math.addvalues(a,b))

        print("Floats can be added\n")

    def test_lists(self):
 
        a = ['arti','patel']
        b = ['my','project']
        c = ['arti','patel','my','project']

        # parent class method
        self.assertEqual(c,process.math.addvalues(a,b))

        print("Lists can be added\n")

    def tearDown(self):
        """
        Executes after each test
        """
        pass

if __name__ == '__main__':
    unittest.main()

