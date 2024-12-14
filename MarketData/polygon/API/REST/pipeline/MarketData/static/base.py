from ....response.schema.MarketData.dailyOpenClose import DailyOpenCloseResponse

# it is a static config class for tickers
class baseStatic:
    base_url = "https://api.polygon.io/v3/reference/tickers?"

    @staticmethod
    def formulate_REST_request_url(**params):
        return baseStatic.base_url + "&".join([f"{k}={v}" for k, v in params.items()])


class aggregatesStatic(baseStatic):
    base_url = "https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_}/{to}?"

    def __init__(self, ticker, multiplier, timespan, from_, to):
        self.base_url = self.base_url.format(
            ticker = ticker,
            multiplier = multiplier,
            timespan = timespan,
            from_ = from_,
            to = to
        )

    def formulate_REST_request_url(self, **params):
        # remove ticker, timespan, from, to from params
        params = {k: v for k, v in params.items() if k not in ['ticker', 'multiplier', 'timespan', 'from_', 'to']}
        res_url = (
            self.base_url
            + "&".join([f"{k}={v}" for k, v in params.items()])
        )
        return res_url


class dailyOpenCloseStatic(baseStatic):
    base_url = "https://api.polygon.io/v1/open-close/{ticker}/{date}?"
    response_parser = DailyOpenCloseResponse
    
    def __init__(self, ticker, date):
        self.base_url = self.base_url.format(
            ticker = ticker,
            date = date
        )

    def formulate_REST_request_url(self, **params):
        # remove ticker, date from params
        params = {k: v for k, v in params.items() if k not in ['ticker', 'date']}
        return self.base_url + "&".join([f"{k}={v}" for k, v in params.items()])
    
    def parse_response(self, response):
        return self.response_parser.from_dict(response)
