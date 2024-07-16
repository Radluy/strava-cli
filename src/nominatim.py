import requests
import xml.etree.ElementTree as ET


def get_location(lat: float, lon: float) -> tuple[str, str]:
    """Get country and city from coordinates using Nominatim. Request rates apply."""
    url = "	https://nominatim.openstreetmap.org/reverse"
    params = {"lat": lat, "lon": lon}
    headers = {"user-agent": "strava-cli"}
    response = requests.get(url=url, params=params, headers=headers)

    xml_tree = ET.fromstring(response.content)
    address = xml_tree.find('addressparts')
    country = address.find('country').text
    city = address.find('city').text
    return country, city


if __name__ == '__main__':
    country, city = get_location()
    print(country, city)
