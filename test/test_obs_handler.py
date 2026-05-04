import unittest
from obs_handler import obs_handler
from common.exception_handling import ErrorWithCode


class TestOBShandler(unittest.TestCase):
    def setUp(self):
        """
        Use setUp interface to instantiate class to test
        :return:
        """
        print("setup")
        self.test_class = obs_handler.OBSHandler()

    def test_call_obs(self):
        """ test method of s"""
        self.test_class.OBSPath = "Wrong Path"
        expected = None
        # actual = self.test_class.call_obs()
        # Remember not to make the function to test callable!
        self.assertRaises(FileNotFoundError, self.test_class._launch_obs)

    def tearDown(self):
        """
        Method that will run after unittest is finished
        Returns everything to normal
        :return:
        """
        print("tearDown")
        del self.test_class

    def exception_successful(self):
        """
        Things to do after successfully assert an exception
        :return:
        """
        print("Failed Successfully")


if __name__ == '__main__':
    unittest.main()
