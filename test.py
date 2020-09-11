
from app import app 
import unittest

class TestHealthJoyCloner(unittest.TestCase): 

    def test_search_page_loads(self): 
        tester  = app.test_client(self)
        response = tester.get('/search', content_type="html/text")
        self.assertEqual(response.status_code,200)

    def test_clone_page_loads(self): 
        tester  = app.test_client(self)
        response = tester.get('/clone', content_type="html/text")
        self.assertEqual(response.status_code,200)

if __name__ == '__main__': 
    unittest.main()