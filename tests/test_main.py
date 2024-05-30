import unittest
from unittest.mock import patch
import sys
import os


# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from main import app, generate_short_url, shortened_urls


class FlaskAppTests(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    def test_generate_short_url(self):
        """ Test random character generation and ensure that it is always different from each other and 5 chars """
        url1 = generate_short_url()
        url2 = generate_short_url()
        while url1 == url2:
            url2 = generate_short_url()
        self.assertNotEqual(url1, url2)
        self.assertEqual(len(url1), 5)
        self.assertEqual(len(url2), 5)


    def test_index_get(self):
        """ Website's own root path should always return 200 """
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)


    def test_index_post_one(self):
        """ The returned short URL will always be a predictable 'abcde' in this scenario """
        with patch("main.generate_short_url", return_value="abcde"):
            result = self.app.post("/", data=dict(long_url="http://example.com"))
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'Your shortened URL is: <a href="abcde">abcde</a>', result.data)


    def test_index_post_two(self):
        """ The returned short URL will always be a predictable '1b2d3' in this scenario """
        with patch("main.generate_short_url", return_value="1b2d3"):
            result = self.app.post("/", data=dict(long_url="http://example.com"))
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'Your shortened URL is: <a href="1b2d3">1b2d3</a>', result.data)


    def test_redirect_url_one(self):
        """ Test the redirection """
        shortened_urls["cyru4"] = "http://example.com"
        result = self.app.get("/cyru4")
        self.assertEqual(result.status_code, 302)
        self.assertEqual(result.location, "http://example.com")


    def test_redirect_url_two(self):
        """ Test the redirection """
        shortened_urls["c4th3rin3"] = "http://example.com"
        result = self.app.get("/c4th3rin3")
        self.assertEqual(result.status_code, 302)
        self.assertEqual(result.location, "http://example.com")


    def test_redirect_url_not_found_one(self):
        """ Non-existent routes should always return 404 status code """
        result = self.app.get("/nonexistent")
        self.assertEqual(result.status_code, 404)
        self.assertIn(b"URL does not exist on our server.", result.data)


    def test_redirect_url_not_found_two(self):
        """ Non-existent routes should always return 404 status code """
        result = self.app.get("/n0n3x1st3nt")
        self.assertEqual(result.status_code, 404)
        self.assertIn(b"URL does not exist on our server.", result.data)


if __name__ == "__main__":
    unittest.main()
