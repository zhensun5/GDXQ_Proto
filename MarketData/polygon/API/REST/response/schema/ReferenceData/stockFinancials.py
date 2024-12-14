from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import pandas as pd
from datetime import datetime

@dataclass
class Financial:
    start_date: str
    end_date: str
    filing_date: str
    acceptance_datetime: str
    timeframe: str
    fiscal_period: str
    fiscal_year: int
    cik: str
    sic: str
    tickers: List[str]
    company_name: str
    source_filing_url: str
    source_filing_file_url: str
    financials: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "filing_date": self.filing_date,
            "acceptance_datetime": self.acceptance_datetime,
            "timeframe": self.timeframe,
            "fiscal_period": self.fiscal_period,
            "fiscal_year": self.fiscal_year,
            "cik": self.cik,
            "sic": self.sic,
            "tickers": self.tickers,
            "company_name": self.company_name,
            "source_filing_url": self.source_filing_url,
            "source_filing_file_url": self.source_filing_file_url,
            "financials": self.financials
        }

@dataclass
class FinancialsResponse:
    results: List[Financial] = field(default_factory=list)
    status: str = ""
    request_id: str = ""
    next_url: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Optional['FinancialsResponse']:
        if data.get("status") != "OK":
            print("Error: Response status is not OK.")
            return None

        results = data.get("results", [])
        if not results:
            print("Warning: No results found in the response.")
            return None

        financials = [Financial(**result) for result in results]
        return FinancialsResponse(
            results=financials,
            status=data.get("status", ""),
            request_id=data.get("request_id", ""),
            next_url=data.get("next_url")
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results:
            print("Warning: No financial data available to convert to DataFrame.")
            return pd.DataFrame()

        data = [financial.to_dict() for financial in self.results]
        df = pd.DataFrame(data)
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])
        df['filing_date'] = pd.to_datetime(df['filing_date'])
        df['acceptance_datetime'] = pd.to_datetime(df['acceptance_datetime'])
        return df

# Example usage:
# response_data = ... # JSON data from the API
# parsed_response = FinancialsResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")

