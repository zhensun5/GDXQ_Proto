from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import pandas as pd

@dataclass
class AggregateResult:
    v: int    # Volume
    vw: float # Volume-weighted average price
    o: float  # Open price
    c: float  # Close price
    h: float  # High price
    l: float  # Low price
    t: int    # Timestamp (Unix ms)
    n: int    # Number of transactions

@dataclass
class MarketDataAggregatesResponse:
    ticker: str
    queryCount: int
    resultsCount: int
    adjusted: bool
    status: str
    request_id: str
    count: int
    next_url: Optional[str]
    results: List[AggregateResult] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> Optional['MarketDataAggregatesResponse']:
        if data.get('status') != 'OK':
            print(f"Error: Response status is {data.get('status')}")
            return None

        if 'results' not in data or not data['results']:
            print("Warning: No results found in the response.")
            return None

        return cls(
            ticker=data.get('ticker', ''),
            queryCount=data.get('queryCount', 0),
            resultsCount=data.get('resultsCount', 0),
            adjusted=data.get('adjusted', False),
            results=[AggregateResult(**result) for result in data.get('results', [])],
            status=data.get('status', ''),
            request_id=data.get('request_id', ''),
            count=data.get('count', 0),
            next_url=data.get('next_url')
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
#     # ... (your provided data)
# }

# parsed_response = PolygonAggsResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")
