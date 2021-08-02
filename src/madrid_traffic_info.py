import requests
import PmParser as pm

API_URL = 'https://informo.madrid.es/informo/tmadrid/pm.xml'


def get_latest_traffic_info():
    response = requests.get(API_URL)

    if response.status_code == 200:
        return pm.parse_traffic_data(response.content, debug=False)
    else:
        # TODO proper exception
        raise RuntimeWarning("something went wrong")

