from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import pandas as pd

@dataclass
class QuoteCondition:
    id: int
    type: str
    name: str
    asset_class: str
    sip_mapping: Dict[str, str]
    data_types: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "asset_class": self.asset_class,
            "sip_mapping": self.sip_mapping,
            "data_types": self.data_types
        }

@dataclass
class QuoteConditionsResponse:
    results: List[QuoteCondition] = field(default_factory=list)
    status: str = ""
    request_id: str = ""
    count: int = 0
    next_url: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Optional['QuoteConditionsResponse']:
        if data.get("status") != "OK":
            print("Error: Response status is not OK.")
            return None

        results = data.get("results", [])
        if not results:
            print("Warning: No results found in the response.")
            return None

        conditions = [QuoteCondition(**result) for result in results]
        return QuoteConditionsResponse(
            results=conditions,
            status=data.get("status", ""),
            request_id=data.get("request_id", ""),
            count=data.get("count", 0),
            next_url=data.get("next_url")
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results:
            print("Warning: No quote conditions data available to convert to DataFrame.")
            return pd.DataFrame()

        data = [condition.to_dict() for condition in self.results]
        return pd.DataFrame(data)

# Example usage:
# response_data = ... # JSON data from the API
# parsed_response = QuoteConditionsResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")

