# it is a static config class for tickers
class baseStatic:
    base_url = "https://api.polygon.io/v3/reference/tickers?"

    @staticmethod
    def formulate_REST_request_url(**params):
        return baseStatic.base_url + "&".join([f"{k}={v}" for k, v in params.items()])

