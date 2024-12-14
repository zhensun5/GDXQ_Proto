import logging
from typing import Union, Optional
import datetime as dt
import pandas as pd
from ...utils.overhead import PolygonClient
from .utils import parse_aggregates
from .basic import PolygonBaseHandler
from functools import partial
from .static.base import aggregatesStatic


class PolygonAggregatesHandler(PolygonBaseHandler):
    def __init__(self, client=None):
        super().__init__(client)
        self.polygon_api_func = self.client.list_aggs

    def _input_validation(self, ticker, multiplier, timespan, from_date, to_date, adjusted, sort, limit):
        if not isinstance(ticker, str):
            raise ValueError(f"Invalid ticker value, should be a string, {type(ticker)} provided")
        if timespan not in ['second', 'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']:
            raise ValueError("Invalid timespan value")
        if sort not in ['asc', 'desc']:
            raise ValueError("Invalid sort value")
        if limit > 50000:
            raise ValueError(f"Invalid limit value, max is 50000, {limit} provided")
        if not isinstance(multiplier, int):
            raise ValueError(f"Invalid multiplier value, should be an integer, {type(multiplier)} provided")
        if not isinstance(adjusted, bool):
            raise ValueError(f"Invalid adjusted value, should be a boolean, {type(adjusted)} provided")

    def get_aggregates(self,
                      method: str,
                      ticker: str,
                      multiplier: int = 1,
                      timespan: str = 'minute',
                      from_: Union[dt.datetime, str, pd.Timestamp] = None,
                      to: Union[dt.datetime, str, pd.Timestamp] = None,
                      adjusted: bool = True,
                      sort: str = 'asc',
                      limit: int = 50000,
                      raw: bool = False,
                      parse_to_df: bool = True,
                      **params):
        """
        Get aggregate bars for a ticker over a given date range
        
        Args:
            method: Method to use for fetching data ('API' or 'REST')
            ticker: The ticker symbol
            multiplier: The size of the timespan multiplier
            timespan: The size of the time window
            from_date: The start date
            to_date: The end date
            adjusted: Whether to adjust for splits
            sort: Sort direction ('asc' or 'desc')
            limit: Limit of results per page
            raw: Return raw response
            
        Returns:
            DataFrame or dict: Aggregates data
        """
        caller_locals = locals()
        caller_locals['client'] = self.client
        
        # todo: add params validation
        # params = PolygonBaseHandler._get_params(self.polygon_api_func, caller_locals)
        # self._input_validation(**params)
        
        if method == "API":
            func = self.get_aggregates_API
        elif method == "REST":
            func = partial(
                self.get_REST,
                RESTStatic=aggregatesStatic(ticker, multiplier, timespan, from_, to),
                polygon_api_func=self.polygon_api_func
            )
        return func(caller_locals)

    @staticmethod
    def _process_response_api(response: dict) -> dict:
        """Process the API response and format if needed"""
        return response

    def get_aggregates_API(self, caller_locals):
        response = caller_locals.pop("client").list_aggs(**caller_locals)

        if caller_locals.get("raw", False):
            return self._process_response_api(response)
        
        if caller_locals.get("parse_to_df", True):
            return parse_aggregates(response)
        return response


