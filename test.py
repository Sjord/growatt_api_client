import unittest
from growatt import hash_password


class TestHashPassword(unittest.TestCase):
    def test_hash_password(self):
        assert hash_password("banaan") == "31d674be46e1ba6b54388a671cc9accb"


if __name__ == "__main__":
    unittest.main()
