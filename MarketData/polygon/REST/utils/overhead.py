import keyring
from polygon import RESTClient


# a config class for handling polygon url
class PolygonConfig:
    base_url = "https://api.polygon.io"


# a class to handle the polygon client
class PolygonClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or keyring.get_password(PolygonConfig.base_url, "toutou")
        self.client = RESTClient(self.api_key)

    def get_polygon_client(self):
        return self.client
    





