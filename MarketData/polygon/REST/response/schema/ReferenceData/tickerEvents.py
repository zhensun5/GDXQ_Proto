from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

@dataclass
class TickerChangeEvent:
    ticker: str

@dataclass
class Event:
    ticker_change: TickerChangeEvent
    type: str
    date: str

@dataclass
class TickerEvents:
    name: str
    composite_figi: str
    cik: str
    events: List[Event] = field(default_factory=list)

@dataclass
class TickerEventsResponse:
    request_id: str
    results: Optional[TickerEvents] = None
    status: str

    @classmethod
    def from_dict(cls, data: dict) -> Optional['TickerEventsResponse']:
        if data.get('status') != 'OK':
            print(f"Error: Response status is {data.get('status')}")
            return None

        results_data = data.get('results')
        if not results_data:
            print("Warning: No results found in the response.")
            return None

        events_data = results_data.get('events', [])

        return cls(
            request_id=data.get('request_id', ''),
            status=data.get('status', ''),
            results=TickerEvents(
                name=results_data.get('name', ''),
                composite_figi=results_data.get('composite_figi', ''),
                cik=results_data.get('cik', ''),
                events=[Event(
                    ticker_change=TickerChangeEvent(**event.get('ticker_change', {})),
                    type=event.get('type', ''),
                    date=event.get('date', '')
                ) for event in events_data]
            )
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results or not self.results.events:
            print("Warning: No event data available to convert to DataFrame.")
            return pd.DataFrame()

        events_list = [
            {
                "name": self.results.name,
                "composite_figi": self.results.composite_figi,
                "cik": self.results.cik,
                "ticker": event.ticker_change.ticker,
                "type": event.type,
                "date": event.date
            }
            for event in self.results.events
        ]

        df = pd.DataFrame(events_list)
        df['date'] = pd.to_datetime(df['date'])
        return df

# # Usage example
# response_data = {
#     "results": {
#         "name": "Meta Platforms, Inc. Class A Common Stock",
#         "composite_figi": "BBG000MM2P62",
#         "cik": "0001326801",
#         "events": [
#             {
#                 "ticker_change": {
#                     "ticker": "META"
#                 },
#                 "type": "ticker_change",
#                 "date": "2022-06-09"
#             },
#             {
#                 "ticker_change": {
#                     "ticker": "FB"
#                 },
#                 "type": "ticker_change",
#                 "date": "2012-05-18"
#             }
#         ]
#     },
#     "status": "OK",
#     "request_id": "144c5f3b0575b08314e676ceb132ca19"
# }

# parsed_response = TickerEventsResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")