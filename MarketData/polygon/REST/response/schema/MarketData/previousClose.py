from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime

@dataclass
class StockResult:
    T: str  # Ticker
    v: int  # Volume
    vw: float  # Volume Weighted Average Price
    o: float  # Open Price
    c: float  # Close Price
    h: float  # High Price
    l: float  # Low Price
    t: int  # Timestamp
    n: int  # Number of Transactions

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Ticker": self.T,
            "Volume": self.v,
            "VWAP": self.vw,
            "Open": self.o,
            "Close": self.c,
            "High": self.h,
            "Low": self.l,
            "Timestamp": datetime.fromtimestamp(self.t / 1000),  # Convert to datetime
            "Transactions": self.n
        }

@dataclass
class StockDataResponse:
    ticker: str = ""
    queryCount: int = 0
    resultsCount: int = 0
    adjusted: bool = False
    results: List[StockResult] = field(default_factory=list)
    status: str = ""
    request_id: str = ""
    count: int = 0

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Optional['StockDataResponse']:
        if data.get("status") != "OK":
            print("Error: Response status is not OK.")
            return None

        results = data.get("results", [])
        if not results:
            print("Warning: No results found in the response.")
            return None

        stock_results = [StockResult(**result) for result in results]
        return StockDataResponse(
            ticker=data.get("ticker", ""),
            queryCount=data.get("queryCount", 0),
            resultsCount=data.get("resultsCount", 0),
            adjusted=data.get("adjusted", False),
            results=stock_results,
            status=data.get("status", ""),
            request_id=data.get("request_id", ""),
            count=data.get("count", 0)
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results:
            print("Warning: No stock data available to convert to DataFrame.")
            return pd.DataFrame()

        data = [result.to_dict() for result in self.results]
        return pd.DataFrame(data)

# Example usage:
# response_data = ... # JSON data from the API
# parsed_response = StockDataResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")