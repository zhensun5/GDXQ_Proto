from dataclasses import dataclass
from typing import Optional
import pandas as pd

@dataclass
class DailyOpenCloseResponse:
    status: str
    from_date: str
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    afterHours: Optional[float] = None
    preMarket: Optional[float] = None

    @classmethod
    def from_dict(cls, data: dict) -> Optional['DailyOpenCloseResponse']:
        if data.get('status') != 'OK':
            print(f"Error: Response status is {data.get('status')}")
            return None

        return cls(
            status=data.get('status', ''),
            from_date=data.get('from', ''),
            symbol=data.get('symbol', ''),
            open=data.get('open', 0.0),
            high=data.get('high', 0.0),
            low=data.get('low', 0.0),
            close=data.get('close', 0.0),
            volume=data.get('volume', 0),
            afterHours=data.get('afterHours'),
            preMarket=data.get('preMarket')
        )

    def to_dataframe(self) -> pd.DataFrame:
        data = {
            "from_date": [self.from_date],
            "symbol": [self.symbol],
            "open": [self.open],
            "high": [self.high],
            "low": [self.low],
            "close": [self.close],
            "volume": [self.volume],
            "afterHours": [self.afterHours],
            "preMarket": [self.preMarket]
        }
        df = pd.DataFrame(data)
        df['from_date'] = pd.to_datetime(df['from_date'])
        return df

# # Usage example
# response_data = {
#     "status": "OK",
#     "from": "2024-10-02",
#     "symbol": "AAPL",
#     "open": 225.89,
#     "high": 227.37,
#     "low": 223.02,
#     "close": 226.78,
#     "volume": 31929459,
#     "afterHours": 226.9715,
#     "preMarket": 225.6
# }

# parsed_response = DailyOpenCloseResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")
