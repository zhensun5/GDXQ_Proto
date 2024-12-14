from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import pandas as pd

@dataclass
class Exchange:
    id: int
    type: str
    asset_class: str
    locale: str
    name: str
    mic: Optional[str] = None
    operating_mic: str = ""
    participant_id: Optional[str] = None
    url: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "asset_class": self.asset_class,
            "locale": self.locale,
            "name": self.name,
            "mic": self.mic,
            "operating_mic": self.operating_mic,
            "participant_id": self.participant_id,
            "url": self.url
        }

@dataclass
class ExchangesResponse:
    results: List[Exchange] = field(default_factory=list)
    status: str = ""
    request_id: str = ""
    count: int = 0

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Optional['ExchangesResponse']:
        if data.get("status") != "OK":
            print("Error: Response status is not OK.")
            return None

        results = data.get("results", [])
        if not results:
            print("Warning: No results found in the response.")
            return None

        exchanges = [Exchange(**result) for result in results]
        return ExchangesResponse(
            results=exchanges,
            status=data.get("status", ""),
            request_id=data.get("request_id", ""),
            count=data.get("count", 0)
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results:
            print("Warning: No exchange data available to convert to DataFrame.")
            return pd.DataFrame()

        data = [exchange.to_dict() for exchange in self.results]
        return pd.DataFrame(data)

# Example usage:
# response_data = ... # JSON data from the API
# parsed_response = ExchangesResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")

