import unittest
from parser import parse_line


class TestParser(unittest.TestCase):
    """Checks that parse_line() handles a good line, a broken line, and
    the "-" size edge case without crashing."""

    def test_valid_line(self):
        # a normal, well-formed log line should parse into all expected fields
        line = '203.0.113.42 - - [01/Jun/2026:09:14:22 +0000] "GET /products/1877 HTTP/1.1" 200 5324 "-" "Mozilla/5.0"'
        result = parse_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result["ip"], "203.0.113.42")
        self.assertEqual(result["endpoint"], "/products/1877")
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["size"], 5324)

    def test_malformed_line_returns_none(self):
        # garbage input should never crash the parser -- just return None
        line = "this is not a valid log line at all"
        self.assertIsNone(parse_line(line))

    def test_dash_size_becomes_zero(self):
        # a "-" in the size field means "no body", should become 0
        line = '203.0.113.42 - - [01/Jun/2026:09:14:22 +0000] "GET /health HTTP/1.1" 200 - "-" "curl/8.0"'
        result = parse_line(line)
        self.assertEqual(result["size"], 0)


if __name__ == "__main__":
    unittest.main()