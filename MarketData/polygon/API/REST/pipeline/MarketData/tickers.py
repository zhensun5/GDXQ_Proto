import re
import requests
import keyring
import time
import json
import logging
import pandas as pd
import datetime as dt
from functools import partial
from typing import Union, Optional
from datetime import datetime
from ...utils.overhead import PolygonClient
from .utils import parse_aggregates
from .static.base import baseStatic
from .basic import PolygonBaseHandler


class PolygonListTickersHandler(PolygonBaseHandler):
    def __init__(self, client = None):
        super().__init__(client)
        self.polygon_api_func = self.client.list_tickers

    def _input_validation(self, market, exchange, type, active, sort, order, limit):
        if not isinstance(limit, int):
            raise ValueError(f"Invalid limit value, should be an integer, {type(limit)} provided")

    def get_tickers(self,
                    method:str,
                    date: Union[dt.datetime, str, pd.Timestamp],
                    market: Optional[str] = None,
                    exchange: Optional[str] = None,
                    type: Optional[str] = None,
                    active: Optional[bool] = True,
                    sort: Optional[str] = None,
                    order: Optional[str] = None,
                    limit: Optional[int] = 1000,
                    raw: bool = False,
                    **params) -> dict:
        """
        Get the list of tickers supported by Polygon.io
        
        Args:
            market: Filter by market type (stocks, crypto, fx)
            exchange: Filter by exchange
            type: Filter by security type (CS, ETF, etc.)
            active: Filter for only active or inactive symbols
            sort: Sort field used for ordering
            order: Order results (asc/desc)
            limit: Limit the number of results
            raw: Return raw response from API
            
        Returns:
            dict: Ticker data response
        """
        caller_locals = locals()
        caller_locals['client'] = self.client
        
        # todo: add params validation
        # params = PolygonBaseHandler._get_params(self.polygon_api_func, caller_locals)
        # self._input_validation(**params)

        if method == "API":
            func = self.get_tickers_API
        elif method == "REST":
            func = partial(
                self.get_REST, 
                RESTStatic=baseStatic,
                polygon_api_func=self.polygon_api_func
            )
        return func(caller_locals)
    
    @staticmethod
    def _process_response_api(response: dict) -> dict:
        """Process the API response and format if needed"""
        # Add any custom processing logic here
        return response
    
    def get_tickers_API(self, caller_locals):
        response = caller_locals.pop("client").list_tickers(**caller_locals)

        if caller_locals.get("raw", False):
            return self._process_response_api(response)
        return response
    
