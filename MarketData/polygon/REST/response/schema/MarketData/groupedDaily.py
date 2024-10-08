from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

@dataclass
class AggregateResult:
    T: str    # Ticker symbol
    v: float  # Volume
    vw: float # Volume-weighted average price
    o: float  # Open price
    c: float  # Close price
    h: float  # High price
    l: float  # Low price
    t: int    # Timestamp (Unix ms)
    n: int    # Number of transactions

@dataclass
class PolygonAggsResponse:
    queryCount: int
    resultsCount: int
    adjusted: bool
    results: List[AggregateResult] = field(default_factory=list)
    status: str
    request_id: str
    count: int

    @classmethod
    def from_dict(cls, data: dict) -> Optional['AggregatesResponse']:
        if data.get('status') != 'OK':
            print(f"Error: Response status is {data.get('status')}")
            return None

        if 'results' not in data or not data['results']:
            print("Warning: No results found in the response.")
            return None

        return cls(
            queryCount=data.get('queryCount', 0),
            resultsCount=data.get('resultsCount', 0),
            adjusted=data.get('adjusted', False),
            results=[AggregateResult(**result) for result in data.get('results', [])],
            status=data.get('status', ''),
            request_id=data.get('request_id', ''),
            count=data.get('count', 0)
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results:
            print("Warning: No data available to convert to DataFrame.")
            return pd.DataFrame()

        df = pd.DataFrame([vars(result) for result in self.results])
        df['datetime'] = pd.to_datetime(df['t'], unit='ms')
        df = df.drop('t', axis=1)
        df = df.set_index('datetime')
        return df

# # Usage example
# response_data = {
#     "queryCount": 10637,
#     "resultsCount": 10637,
#     "adjusted": True,
#     "results": [
#         {"T": "DEI", "v": 1.427613e+06, "vw": 17.548, "o": 17.52, "c": 17.54, "h": 17.725, "l": 17.26, "t": 1727812800000, "n": 13636},
#         {"T": "KORE", "v": 4436, "vw": 2.215, "o": 2.26, "c": 2.14, "h": 2.32, "l": 2.14, "t": 1727812800000, "n": 67},
#         # ... (other results)
#     ],
#     "status": "OK",
#     "request_id": "132a1e26a7efa65bddbfe705b19d591f",
#     "count": 10637
# }

# parsed_response = PolygonAggsResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")