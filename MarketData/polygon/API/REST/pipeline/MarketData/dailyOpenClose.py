import logging
from typing import Union, Optional
import datetime as dt
import pandas as pd
from ...utils.overhead import PolygonClient
from .utils import parse_aggregates
from .basic import PolygonBaseHandler
from functools import partial
from .static.base import dailyOpenCloseStatic



class PolygonDailyOpenCloseHandler(PolygonBaseHandler):
    def __init__(self, client=None):
        super().__init__(client)
        self.polygon_api_func = self.client.get_daily_open_close_agg

    def _input_validation(self, ticker: str, date: Union[str, dt.datetime, pd.Timestamp], adjusted: bool):
        """Validate input parameters"""
        if not isinstance(ticker, str):
            raise ValueError(f"Invalid ticker value, should be a string, {type(ticker)} provided")
        if not isinstance(adjusted, bool):
            raise ValueError(f"Invalid adjusted value, should be a boolean, {type(adjusted)} provided")

    def get_daily_open_close(self,
                           method: str,
                           ticker: str,
                           date: Union[str, dt.datetime, pd.Timestamp],
                           adjusted: bool = True,
                           raw: bool = False,
                           parse_to_df: bool = True,
                           **params):
        """
        Get the daily open, close and after hours prices of a stock for a given date
        
        Args:
            method: Method to use for fetching data ('API' or 'REST')
            ticker: The ticker symbol
            date: The date to get data for
            adjusted: Whether to adjust for splits
            raw: Return raw response
            
        Returns:
            DataFrame or dict: Daily open/close data
        """
        caller_locals = locals()
        caller_locals['client'] = self.client

        # Convert datetime to string format if needed
        if isinstance(date, (dt.datetime, pd.Timestamp)):
            caller_locals['date'] = date.strftime('%Y-%m-%d')
        
        if method == "API":
            func = self.get_daily_open_close_API
        elif method == "REST":
            func = partial(
                self.get_REST,
                RESTStatic=dailyOpenCloseStatic(ticker, date), 
                polygon_api_func=self.polygon_api_func
            )
        return func(caller_locals)

    @staticmethod
    def _process_response_api(response: dict) -> dict:
        """Process the API response and format if needed"""
        return response

    def get_daily_open_close_API(self, caller_locals):
        """Get daily open/close data using Polygon API"""
        response = caller_locals.pop("client").get_daily_open_close_agg(**caller_locals)

        if caller_locals.get("raw", False):
            return self._process_response_api(response)
        
        if caller_locals.get("parse_to_df", True):
            # Convert response to DataFrame
            df = parse_aggregates(response)
            return df
        return response
