from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

@dataclass
class MarketHoliday:
    date: str
    exchange: str
    name: str
    status: str
    open: Optional[str] = None
    close: Optional[str] = None

@dataclass
class MarketHolidayResponse:
    results: List[MarketHoliday] = field(default_factory=list)

    @classmethod
    def from_list(cls, data: List[dict]) -> 'MarketHolidayResponse':
        if not data:
            print("Warning: No holiday data found.")
            return cls()

        return cls(
            results=[MarketHoliday(**holiday) for holiday in data]
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results:
            print("Warning: No holiday data available to convert to DataFrame.")
            return pd.DataFrame()

        df = pd.DataFrame([vars(holiday) for holiday in self.results])
        df['date'] = pd.to_datetime(df['date'])
        if 'open' in df.columns:
            df['open'] = pd.to_datetime(df['open'], errors='coerce')
        if 'close' in df.columns:
            df['close'] = pd.to_datetime(df['close'], errors='coerce')
        return df

# # Usage example
# holiday_data = [
#     {
#         "date": "2024-11-28",
#         "exchange": "NASDAQ",
#         "name": "Thanksgiving",
#         "status": "closed"
#     },
#     {
#         "date": "2024-11-28",
#         "exchange": "NYSE",
#         "name": "Thanksgiving",
#         "status": "closed"
#     },
#     {
#         "close": "2024-11-29T18:00:00.000Z",
#         "date": "2024-11-29",
#         "exchange": "NYSE",
#         "name": "Thanksgiving",
#         "open": "2024-11-29T14:30:00.000Z",
#         "status": "early-close"
#     },
#     # ... (other holidays)
# ]

# parsed_response = MarketHolidayResponse.from_list(holiday_data)
# df = parsed_response.to_dataframe()
# print(df)