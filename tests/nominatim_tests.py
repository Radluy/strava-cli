import unittest
from src import nominatim  # noqa: E402


# Be careful with spamming the Nominatim API, might get request rated
class TestValidateAttrFilters(unittest.TestCase):
    def test_get_country(self):
        country, _ = nominatim.get_location(41.98249167, 2.824075)
        self.assertEqual(country, "España")

    def test_get_city(self):
        _, city = nominatim.get_location(41.98249167, 2.824075)
        self.assertEqual(city, "Girona")
