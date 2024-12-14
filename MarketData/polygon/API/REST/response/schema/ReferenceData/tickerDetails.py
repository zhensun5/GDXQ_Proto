from dataclasses import dataclass, field
from typing import Optional, Dict
import pandas as pd

@dataclass
class Address:
    address1: str
    city: str
    state: str
    postal_code: str

@dataclass
class Branding:
    logo_url: str
    icon_url: str

@dataclass
class TickerDetails:
    ticker: str
    name: str
    market: str
    locale: str
    primary_exchange: str
    type: str
    active: bool
    currency_name: str
    cik: str
    composite_figi: str
    share_class_figi: str
    market_cap: int
    phone_number: str
    address: Address
    description: str
    sic_code: str
    sic_description: str
    ticker_root: str
    homepage_url: str
    total_employees: int
    list_date: str
    branding: Branding
    share_class_shares_outstanding: int
    weighted_shares_outstanding: int
    round_lot: int

@dataclass
class TickerDetailsResponse:
    request_id: str
    results: Optional[TickerDetails] = None
    status: str

    @classmethod
    def from_dict(cls, data: dict) -> Optional['TickerDetailsResponse']:
        if data.get('status') != 'OK':
            print(f"Error: Response status is {data.get('status')}")
            return None

        results_data = data.get('results')
        if not results_data:
            print("Warning: No results found in the response.")
            return None

        address_data = results_data.get('address', {})
        branding_data = results_data.get('branding', {})

        return cls(
            request_id=data.get('request_id', ''),
            status=data.get('status', ''),
            results=TickerDetails(
                ticker=results_data.get('ticker', ''),
                name=results_data.get('name', ''),
                market=results_data.get('market', ''),
                locale=results_data.get('locale', ''),
                primary_exchange=results_data.get('primary_exchange', ''),
                type=results_data.get('type', ''),
                active=results_data.get('active', False),
                currency_name=results_data.get('currency_name', ''),
                cik=results_data.get('cik', ''),
                composite_figi=results_data.get('composite_figi', ''),
                share_class_figi=results_data.get('share_class_figi', ''),
                market_cap=results_data.get('market_cap', 0),
                phone_number=results_data.get('phone_number', ''),
                address=Address(
                    address1=address_data.get('address1', ''),
                    city=address_data.get('city', ''),
                    state=address_data.get('state', ''),
                    postal_code=address_data.get('postal_code', '')
                ),
                description=results_data.get('description', ''),
                sic_code=results_data.get('sic_code', ''),
                sic_description=results_data.get('sic_description', ''),
                ticker_root=results_data.get('ticker_root', ''),
                homepage_url=results_data.get('homepage_url', ''),
                total_employees=results_data.get('total_employees', 0),
                list_date=results_data.get('list_date', ''),
                branding=Branding(
                    logo_url=branding_data.get('logo_url', ''),
                    icon_url=branding_data.get('icon_url', '')
                ),
                share_class_shares_outstanding=results_data.get('share_class_shares_outstanding', 0),
                weighted_shares_outstanding=results_data.get('weighted_shares_outstanding', 0),
                round_lot=results_data.get('round_lot', 0)
            )
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results:
            print("Warning: No data available to convert to DataFrame.")
            return pd.DataFrame()

        data = vars(self.results)
        data['address'] = vars(self.results.address)
        data['branding'] = vars(self.results.branding)
        flat_data = {**data, **data['address'], **data['branding']}
        del flat_data['address']
        del flat_data['branding']
        
        df = pd.DataFrame([flat_data])
        df['list_date'] = pd.to_datetime(df['list_date'])
        return df

# # Usage example
# response_data = {
#     "request_id": "776af563b7290dcd5b690101e14fb5c2",
#     "results": {
#         "ticker": "AAPL",
#         "name": "Apple Inc.",
#         "market": "stocks",
#         "locale": "us",
#         "primary_exchange": "XNAS",
#         "type": "CS",
#         "active": True,
#         "currency_name": "usd",
#         "cik": "0000320193",
#         "composite_figi": "BBG000B9XRY4",
#         "share_class_figi": "BBG001S5N8V8",
#         "market_cap": 3447994188860,
#         "phone_number": "(408) 996-1010",
#         "address": {
#             "address1": "ONE APPLE PARK WAY",
#             "city": "CUPERTINO",
#             "state": "CA",
#             "postal_code": "95014"
#         },
#         "description": "Apple is among the largest companies in the world, with a broad portfolio of hardware and software products targeted at consumers and businesses. Apple's iPhone makes up a majority of the firm sales, and Apple's other products like Mac, iPad, and Watch are designed around the iPhone as the focal point of an expansive software ecosystem. Apple has progressively worked to add new applications, like streaming video, subscription bundles, and augmented reality. The firm designs its own software and semiconductors while working with subcontractors like Foxconn and TSMC to build its products and chips. Slightly less than half of Apple's sales come directly through its flagship stores, with a majority of sales coming indirectly through partnerships and distribution.",
#         "sic_code": "3571",
#         "sic_description": "ELECTRONIC COMPUTERS",
#         "ticker_root": "AAPL",
#         "homepage_url": "https://www.apple.com",
#         "total_employees": 161000,
#         "list_date": "1980-12-12",
#         "branding": {
#             "logo_url": "https://api.polygon.io/v1/reference/company-branding/YXBwbGUuY29t/images/2024-10-01_logo.svg",
#             "icon_url": "https://api.polygon.io/v1/reference/company-branding/YXBwbGUuY29t/images/2024-10-01_icon.png"
#         },
#         "share_class_shares_outstanding": 15204140000,
#         "weighted_shares_outstanding": 15204137000,
#         "round_lot": 100
#     },
#     "status": "OK"
# }

# parsed_response = TickerDetailsResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")
