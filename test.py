import unittest
import destiny_stats

class TestDestinyStats(unittest.TestCase):

    def setUp(self):
        self.app = destiny_stats.app.test_client()

    def test_view_index(self):
        rv = self.app.get('/')
        assert 'Destiny Vaults' in rv.data

    def test_api_tools_get(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_empty_summary_search(self):
        rv = self.app.get('/summary')
        self.assertEqual(rv.status_code, 302)

    def test_summary_search(self):
        rv = self.app.get('/summary?search=el+machete+loco')
        self.assertEqual(rv.status_code, 200)
        assert 'el machete loco' in rv.data


if __name__ == '__main__':
    unittest.main()