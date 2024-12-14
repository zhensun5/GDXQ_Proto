from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

@dataclass
class SecurityType:
    code: str
    description: str
    asset_class: str
    locale: str

@dataclass
class TickerTypesResponse:
    results: List[SecurityType] = field(default_factory=list)
    count: int
    status: str
    request_id: str

    @classmethod
    def from_dict(cls, data: dict) -> Optional['TickerTypesResponse']:
        if data.get('status') != 'OK':
            print(f"Error: Response status is {data.get('status')}")
            return None

        if 'results' not in data or not data['results']:
            print("Warning: No results found in the response.")
            return None

        return cls(
            results=[SecurityType(**result) for result in data.get('results', [])],
            count=data.get('count', 0),
            status=data.get('status', ''),
            request_id=data.get('request_id', '')
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results:
            print("Warning: No security type data available to convert to DataFrame.")
            return pd.DataFrame()

        df = pd.DataFrame([vars(result) for result in self.results])
        return df

# # Usage example
# response_data = {
#     "results": [
#         {
#             "code": "CS",
#             "description": "Common Stock",
#             "asset_class": "stocks",
#             "locale": "us"
#         },
#         {
#             "code": "PFD",
#             "description": "Preferred Stock",
#             "asset_class": "stocks",
#             "locale": "us"
#         },
#         # ... (other security types)
#     ],
#     "count": 24,
#     "status": "OK",
#     "request_id": "7052f29e5bb5989384f61a792ad0d904"
# }

# parsed_response = SecurityTypesResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")
