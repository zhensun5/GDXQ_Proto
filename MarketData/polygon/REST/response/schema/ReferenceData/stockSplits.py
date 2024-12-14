from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

@dataclass
class StockSplit:
    execution_date: str
    id: str
    split_from: int
    split_to: int
    ticker: str

@dataclass
class StockSplitsResponse:
    results: List[StockSplit] = field(default_factory=list)
    status: str
    request_id: str

    @classmethod
    def from_dict(cls, data: dict) -> Optional['StockSplitsResponse']:
        if data.get('status') != 'OK':
            print(f"Error: Response status is {data.get('status')}")
            return None

        if 'results' not in data or not data['results']:
            print("Warning: No results found in the response.")
            return None

        return cls(
            results=[StockSplit(**result) for result in data.get('results', [])],
            status=data.get('status', ''),
            request_id=data.get('request_id', '')
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results:
            print("Warning: No stock split data available to convert to DataFrame.")
            return pd.DataFrame()

        df = pd.DataFrame([vars(result) for result in self.results])
        df['execution_date'] = pd.to_datetime(df['execution_date'])
        return df

# # Usage example
# response_data = {
#     "results": [
#         {
#             "execution_date": "2020-08-31",
#             "id": "E36416cce743c3964c5da63e1ef1626c0aece30fb47302eea5a49c0055c04e8d0",
#             "split_from": 1,
#             "split_to": 4,
#             "ticker": "AAPL"
#         },
#         {
#             "execution_date": "2014-06-09",
#             "id": "E91a6b74ca1a9dcbce26a1f34e24ae26ba2c6359822ccf901ecd827f419137654",
#             "split_from": 1,
#             "split_to": 7,
#             "ticker": "AAPL"
#         },
#         {
#             "execution_date": "2005-02-28",
#             "id": "E90a77bdf742661741ed7c8fc086415f0457c2816c45899d73aaa88bdc8ff6025",
#             "split_from": 1,
#             "split_to": 2,
#             "ticker": "AAPL"
#         }
#     ],
#     "status": "OK",
#     "request_id": "23127ed9a0ca3f7762fd875f4faf32a5"
# }

# parsed_response = StockSplitsResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")