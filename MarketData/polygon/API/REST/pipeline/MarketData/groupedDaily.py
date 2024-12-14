import re
import requests
import keyring
import time
import logging
from typing import Dict, Any, Optional, Union
from datetime import datetime
from ...utils.overhead import PolygonClient
from .utils import parse_aggregates


class PolygonGroupedDailyHandler:
    """Handler for Polygon.io Grouped Daily endpoint"""
    
    def __init__(self, client=None):
        self.logger = logging.getLogger(__name__)
        self.client = client or PolygonClient().get_polygon_client()

    def _input_validation(self, date, adjusted, raw, locale, market_type, include_otc):
        if not isinstance(date, datetime) and not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            raise ValueError(
                f"Invalid date value, should be a datetime object or string in YYYY-MM-DD format, {type(date)} provided")
        if not isinstance(adjusted, bool):
            raise ValueError(f"Invalid adjusted value, should be a boolean, {type(adjusted)} provided")
        if not isinstance(raw, bool):
            raise ValueError(f"Invalid raw value, should be a boolean, {type(raw)} provided")       
        if not isinstance(include_otc, bool):
            raise ValueError(f"Invalid include_otc value, should be a boolean, {type(include_otc)} provided")
        # to do: check locale values: 'us', 'global', etc
        if not isinstance(locale, str):
            raise ValueError(f"Invalid locale value, should be a string, {type(locale)} provided")  
        # to do: check market_type values: 'stocks', 'crypto', etc
        if not isinstance(market_type, str):
            raise ValueError(f"Invalid market_type value, should be a string, {type(market_type)} provided")      

    def get_grouped_daily(self, 
                         date: Union[datetime, str],
                         adjusted: bool = True,
                         raw: bool = False,
                         locale: str = "us",
                         market_type: str = "stocks",
                         include_otc: bool = False,
                         params: Optional[Dict[str, Any]] = None,
                         parse_to_df: bool = True):
        """
        Get daily OHLCV data for all stocks on a specific date.
        
        Args:
            date (datetime): The date for the data
            adjusted (bool): Whether to adjust for splits (default: True)
            include_otc (bool): Whether to include OTC securities (default: False)
            
        Returns:
            Optional[Dict[str, Any]]: Response data or None if request fails
        """

        self._input_validation(date, adjusted, raw, locale, market_type, include_otc)

        if not isinstance(date, str):
            date = date.strftime("%Y-%m-%d")

        grouped = self.client.get_grouped_daily_aggs(
            date, 
            adjusted=adjusted, 
            raw=raw, 
            locale=locale, 
            market_type=market_type, 
            include_otc=include_otc, 
            params=params
        )

        if parse_to_df:
            return parse_aggregates(grouped)
        return grouped