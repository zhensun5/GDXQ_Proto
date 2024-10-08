from dataclasses import dataclass, field
from typing import Optional
import pandas as pd

@dataclass
class DayData:
    c: float
    h: float
    l: float
    o: float
    v: int
    vw: float

@dataclass
class LastQuote:
    P: float
    S: int
    p: float
    s: int
    t: int

@dataclass
class LastTrade:
    c: List[int]
    i: str
    p: float
    s: int
    t: int
    x: int

@dataclass
class MinData:
    av: int
    c: float
    h: float
    l: float
    n: int
    o: float
    t: int
    v: int
    vw: float

@dataclass
class PrevDay:
    c: float
    h: float
    l: float
    o: float
    v: int
    vw: float

@dataclass
class TickerData:
    day: DayData
    lastQuote: LastQuote
    lastTrade: LastTrade
    min: MinData
    prevDay: PrevDay
    ticker: str
    todaysChange: float
    todaysChangePerc: float
    updated: int

@dataclass
class TickerSnapshot:
    ticker: str
    day: Optional[dict] = field(default_factory=dict)
    lastQuote: Optional[dict] = field(default_factory=dict)
    lastTrade: Optional[dict] = field(default_factory=dict)
    min: Optional[dict] = field(default_factory=dict)
    prevDay: Optional[dict] = field(default_factory=dict)
    todaysChange: Optional[float] = None
    todaysChangePerc: Optional[float] = None
    updated: Optional[int] = None

@dataclass
class PolygonResponse:
    status: str
    request_id: str
    ticker: Optional[TickerSnapshot] = None

    @classmethod
    def from_dict(cls, data: dict) -> Optional['PolygonResponse']:
        if data.get('status') != 'OK':
            print(f"Error: Response status is {data.get('status')}")
            return None

        ticker_data = data.get('ticker')
        if not ticker_data:
            print("Warning: No ticker data found in the response.")
            return None

        return cls(
            status=data.get('status', ''),
            request_id=data.get('request_id', ''),
            ticker=TickerSnapshot(
                ticker=ticker_data.get('ticker', ''),
                day=ticker_data.get('day', {}),
                lastQuote=ticker_data.get('lastQuote', {}),
                lastTrade=ticker_data.get('lastTrade', {}),
                min=ticker_data.get('min', {}),
                prevDay=ticker_data.get('prevDay', {}),
                todaysChange=ticker_data.get('todaysChange'),
                todaysChangePerc=ticker_data.get('todaysChangePerc'),
                updated=ticker_data.get('updated')
            )
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.ticker:
            print("Warning: No ticker data available to convert to DataFrame.")
            return pd.DataFrame()

        # Flatten the nested dictionary for DataFrame conversion
        data = {**vars(self.ticker), **self.ticker.day, **self.ticker.lastQuote, **self.ticker.lastTrade, **self.ticker.min, **self.ticker.prevDay}
        df = pd.DataFrame([data])
        return df

# # Usage example
# response_data = {
#     # ... (your provided data)
# }

# parsed_response = PolygonResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")