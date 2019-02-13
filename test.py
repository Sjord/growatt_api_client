import unittest
from growatt import hash_password, Timespan
from datetime import date


class TestHashPassword(unittest.TestCase):
    def test_hash_password(self):
        assert hash_password("banaan") == "31d674be46e1ba6b54388a671cc9accb"


class TestTimespan(unittest.TestCase):
    def test_format_date(self):
        d = date(2012, 6, 15)
        assert Timespan.day.format_date(d) == "2012-06-15"
        assert Timespan.month.format_date(d) == "2012-06"
        assert Timespan.year.format_date(d) == "2012"
        assert Timespan.total.format_date(d) == ""


if __name__ == "__main__":
    unittest.main()
