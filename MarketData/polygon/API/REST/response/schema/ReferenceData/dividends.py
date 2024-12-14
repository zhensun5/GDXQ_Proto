from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

@dataclass
class Dividend:
    cash_amount: float
    currency: str
    declaration_date: str
    dividend_type: str
    ex_dividend_date: str
    frequency: int
    id: str
    pay_date: str
    record_date: str
    ticker: str

@dataclass
class DividendsResponse:
    results: List[Dividend] = field(default_factory=list)
    status: str
    request_id: str
    next_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> Optional['DividendsResponse']:
        if data.get('status') != 'OK':
            print(f"Error: Response status is {data.get('status')}")
            return None

        if 'results' not in data or not data['results']:
            print("Warning: No results found in the response.")
            return None

        return cls(
            results=[Dividend(**result) for result in data.get('results', [])],
            status=data.get('status', ''),
            request_id=data.get('request_id', ''),
            next_url=data.get('next_url')
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results:
            print("Warning: No dividend data available to convert to DataFrame.")
            return pd.DataFrame()

        df = pd.DataFrame([vars(result) for result in self.results])
        date_columns = ['declaration_date', 'ex_dividend_date', 'pay_date', 'record_date']
        for column in date_columns:
            df[column] = pd.to_datetime(df[column])
        return df

# # Usage example
# response_data = {
#     "results": [
#         {
#             "cash_amount": 0.25,
#             "currency": "USD",
#             "declaration_date": "2024-08-01",
#             "dividend_type": "CD",
#             "ex_dividend_date": "2024-08-12",
#             "frequency": 4,
#             "id": "E47fd49ef418c51f7d2415b66030f735adaccf72d85f6b86eea12f96aa1d1c535",
#             "pay_date": "2024-08-15",
#             "record_date": "2024-08-12",
#             "ticker": "AAPL"
#         },
#         # ... (other dividends)
#     ],
#     "status": "OK",
#     "request_id": "373635cbaa7a38bd88cb352b74f57e1f",
#     "next_url": "https://api.polygon.io/v3/reference/dividends?cursor=YXA9MjAyMi0wMi0wNCZhcz1BQVBMJmxpbWl0PTEwJm9yZGVyPWRlc2Mmc29ydD1leF9kaXZpZGVuZF9kYXRlJnRpY2tlcj1BQVBM"
# }

# parsed_response = DividendsResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")

