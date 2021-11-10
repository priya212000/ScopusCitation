import unittest
import CitationRetrieval

class TestAuthorRetrieval(unittest.TestCase):
    def test_author(self):
        self.assertEqual(CitationRetrieval.citeCount('0000000337624311'), 100)
        self.assertEqual(CitationRetrieval.citeCount('000000015077255X'), 0)
        self.assertEqual(CitationRetrieval.citeCount('0000000151382318 '), 626)
        self.assertEqual(CitationRetrieval.citeCount('0000000154765461'), 157)
        self.assertEqual(CitationRetrieval.citeCount('0000000293351568'), 116)

if __name__=='__main__':
    unittest.main()