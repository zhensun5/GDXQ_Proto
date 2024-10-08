import requests
import keyring
from datetime import datetime, timedelta
import time
import logging
from REST.response.schema.aggregates import PolygonAggsResponse


class PolygonDataPipeline:
    base_url = "https://api.polygon.io"

    def __init__(self, api_key=None):
        self.api_key = api_key or keyring.get_password(self.base_url, "toutou")
        self.session = requests.Session()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_tickers_for_date(self, date):
        while True:
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as e:
                self.logger.error(f"Error fetching tickers: {e}")
                break

    def get_time_series_data(self, ticker, date):
        url = f"{self.base_url}/v2/aggs/ticker/{ticker}/range/1/minute/{date}/{date}"
        params = {
            "adjusted": True,
            "sort": "asc",
            "limit": 50000,
            "apiKey": self.api_key
        }
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            parsed_data = PolygonAggsResponse.from_dict(data)
            df = parsed_data.to_dataframe()
            return df
        except requests.RequestException as e:
            self.logger.error(f"Error fetching data for {ticker}: {e}")
            return None

    def process_date(self, date):
        for ticker in tickers:
            time_series_data = self.get_time_series_data(ticker, date)
            if time_series_data:
                self.logger.info(f"Processed {len(time_series_data)} data points for {ticker} on {date}")
            time.sleep(12)  # Rate limiting: 5 requests per minute


# Usage
if __name__ == "__main__":
    api_key = "YOUR_POLYGON_API_KEY"
    pipeline = PolygonDataPipeline(api_key)
    pipeline.run_pipeline("2023-01-01", "2023-01-07")