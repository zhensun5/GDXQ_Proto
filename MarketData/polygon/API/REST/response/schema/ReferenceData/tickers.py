from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

@dataclass
class TickerInfo:
    ticker: str
    name: str
    market: str
    locale: str
    primary_exchange: str
    type: str
    active: bool
    currency_name: str
    cik: str
    composite_figi: str
    share_class_figi: str
    last_updated_utc: str

@dataclass
class TickersResponse:
    results: List[TickerInfo] = field(default_factory=list)
    status: str
    request_id: str
    count: int

    @classmethod
    def from_dict(cls, data: dict) -> Optional['TickersResponse']:
        if data.get('status') != 'OK':
            print(f"Error: Response status is {data.get('status')}")
            return None

        if 'results' not in data or not data['results']:
            print("Warning: No results found in the response.")
            return None

        return cls(
            results=[TickerInfo(**result) for result in data.get('results', [])],
            status=data.get('status', ''),
            request_id=data.get('request_id', ''),
            count=data.get('count', 0)
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results:
            print("Warning: No data available to convert to DataFrame.")
            return pd.DataFrame()

        df = pd.DataFrame([vars(result) for result in self.results])
        df['last_updated_utc'] = pd.to_datetime(df['last_updated_utc'])
        return df

# # Usage example
# response_data = {
#     "results": [
#         {
#             "ticker": "AAPL",
#             "name": "Apple Inc.",
#             "market": "stocks",
#             "locale": "us",
#             "primary_exchange": "XNAS",
#             "type": "CS",
#             "active": True,
#             "currency_name": "usd",
#             "cik": "0000320193",
#             "composite_figi": "BBG000B9XRY4",
#             "share_class_figi": "BBG001S5N8V8",
#             "last_updated_utc": "2024-10-04T00:00:00Z"
#         }
#     ],
#     "status": "OK",
#     "request_id": "9c7c30621d6a063c66cde0ecea2afeaf",
#     "count": 1
# }

# parsed_response = TickersResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")
