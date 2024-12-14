from dataclasses import dataclass, field
from typing import Dict, Optional
import pandas as pd

@dataclass
class MarketStatus:
    afterHours: bool
    currencies: Dict[str, str]
    earlyHours: bool
    exchanges: Dict[str, str]
    indicesGroups: Dict[str, str]
    market: str
    serverTime: str

@dataclass
class MarketStatusResponse:
    status: MarketStatus

    @classmethod
    def from_dict(cls, data: dict) -> 'MarketStatusResponse':
        if not data:
            print("Warning: No market status data found.")
            return cls(status=MarketStatus(
                afterHours=False,
                currencies={},
                earlyHours=False,
                exchanges={},
                indicesGroups={},
                market='',
                serverTime=''
            ))

        return cls(
            status=MarketStatus(
                afterHours=data.get('afterHours', False),
                currencies=data.get('currencies', {}),
                earlyHours=data.get('earlyHours', False),
                exchanges=data.get('exchanges', {}),
                indicesGroups=data.get('indicesGroups', {}),
                market=data.get('market', ''),
                serverTime=data.get('serverTime', '')
            )
        )

    def to_dataframe(self) -> pd.DataFrame:
        data = {
            "afterHours": [self.status.afterHours],
            "earlyHours": [self.status.earlyHours],
            "market": [self.status.market],
            "serverTime": [pd.to_datetime(self.status.serverTime)]
        }
        
        # Flatten the nested dictionaries
        for key, value in self.status.currencies.items():
            data[f"currency_{key}"] = [value]
        
        for key, value in self.status.exchanges.items():
            data[f"exchange_{key}"] = [value]
        
        for key, value in self.status.indicesGroups.items():
            data[f"indicesGroup_{key}"] = [value]

        df = pd.DataFrame(data)
        return df

# # Usage example
# status_data = {
#     "afterHours": False,
#     "currencies": {
#         "crypto": "open",
#         "fx": "open"
#     },
#     "earlyHours": False,
#     "exchanges": {
#         "nasdaq": "closed",
#         "nyse": "closed",
#         "otc": "closed"
#     },
#     "indicesGroups": {
#         "s_and_p": "closed",
#         "societe_generale": "closed",
#         "msci": "closed",
#         "ftse_russell": "closed",
#         "mstar": "open",
#         "mstarc": "open",
#         "cccy": "open",
#         "cgi": "closed",
#         "nasdaq": "closed",
#         "dow_jones": "closed"
#     },
#     "market": "closed",
#     "serverTime": "2024-10-10T22:29:46-04:00"
# }

# parsed_response = MarketStatusResponse.from_dict(status_data)
# df = parsed_response.to_dataframe()
# print(df)