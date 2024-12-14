import pandas as pd
import datetime as dt
from typing import Union
import pandas_market_calendars as mcal

# def get_market_calendar(market_name: str = "NYSE"):
#     return mcal.get_calendar(market_name)


# def get_market_days(market_name: str, 
#                     start_date: Union[str, dt.datetime, pd.Timestamp], 
#                     end_date: Union[str, dt.datetime, pd.Timestamp]):
#     market_calendar = get_market_calendar(market_name)
#     return market_calendar.schedule(start_date, end_date).index


class MarketTime:
    def __init__(self, market_name: str = "NYSE"):
        self.market_name = market_name
        self.market_calendar = self.get_market_calendar()

    def get_market_calendar(self):
        return mcal.get_calendar(self.market_name)

    def get_market_days(self, 
                        start_date: Union[str, dt.datetime, pd.Timestamp], 
                        end_date: Union[str, dt.datetime, pd.Timestamp]):
        return self.market_calendar.schedule(start_date, end_date).index
    
    def get_detail_hours(self, 
                         start_date: Union[str, dt.datetime, pd.Timestamp], 
                         end_date: Union[str, dt.datetime, pd.Timestamp]):
        return (self.market_calendar
                    .schedule(start_date, end_date)
                    .apply(lambda x: x.dt.tz_convert('US/Eastern')))

    def is_market_open(self, 
                       date: Union[str, dt.datetime, pd.Timestamp]):
        return self.market_calendar.is_session(date)
