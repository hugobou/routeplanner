import unittest
import Server


class MyTestCase(unittest.TestCase):
    def test_something(self):
        with Server.app.test_client() as client:
            rv = client.post('/route', json={
                'src': '123', 'dst': '321'
            })
            json_data = rv.get_json()


if __name__ == '__main__':
    unittest.main()


