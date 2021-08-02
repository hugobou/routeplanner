import unittest
import pmparser as pm

# TODO better tests using mock data
class PmparserTestCase(unittest.TestCase):
    def test_parse_traffic_data(self):
        with open('pm.xml') as xmlfile:
            tmlist = pm.parse_traffic_data(xmlfile.read(), debug=True)
            self.assertGreater(len(tmlist), 0)

if __name__ == '__main__':
    unittest.main()
