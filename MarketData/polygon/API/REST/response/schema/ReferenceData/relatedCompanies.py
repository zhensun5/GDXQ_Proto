from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import pandas as pd

@dataclass
class Ticker:
    ticker: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticker": self.ticker
        }

@dataclass
class RelatedTickersResponse:
    results: List[Ticker] = field(default_factory=list)
    status: str = ""
    request_id: str = ""
    ticker: str = ""

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Optional['RelatedTickersResponse']:
        if data.get("status") != "OK":
            print("Error: Response status is not OK.")
            return None

        results = data.get("results", [])
        if not results:
            print("Warning: No results found in the response.")
            return None

        tickers = [Ticker(**result) for result in results]
        return RelatedTickersResponse(
            results=tickers,
            status=data.get("status", ""),
            request_id=data.get("request_id", ""),
            ticker=data.get("ticker", "")
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results:
            print("Warning: No ticker data available to convert to DataFrame.")
            return pd.DataFrame()

        data = [ticker.to_dict() for ticker in self.results]
        return pd.DataFrame(data)

# Example usage:
# response_data = ... # JSON data from the API
# parsed_response = TickersResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")

