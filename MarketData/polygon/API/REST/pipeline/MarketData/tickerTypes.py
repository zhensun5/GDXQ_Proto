import re
import requests
import keyring
import time
import logging
import pandas as pd
from typing import Optional, Union
from datetime import datetime
from typing import Optional
from ...utils.overhead import PolygonClient

class PolygonTickerTypesHandler:
    def __init__(self, client=None):
        self.logger = logging.getLogger(__name__)
        self.client = client or PolygonClient().get_polygon_client()

    def _input_validation(self, asset_class, locale):
        if not isinstance(asset_class, str):
            raise ValueError(f"Invalid asset_class value, should be a string, {type(asset_class)} provided")   
        # to do: check locale values: 'us', 'global', etc
        if not isinstance(locale, str):
            raise ValueError(f"Invalid locale value, should be a string, {type(locale)} provided")    

    def get_ticker_types(self,
                        asset_class: Optional[str] = None,
                        locale: Optional[str] = None,
                        raw: bool = False
                        ) -> dict:
        """
        Get symbol types mapping.
        
        Args:
            asset_class: Asset class (stocks, options, crypto, fx)
            locale: Locale of the symbol types
            raw: Return raw response from API
            
        Returns:
            dict: Ticker types response with mapping of ticker types to their descriptions
        """
        response = self.client.get_ticker_types(
            asset_class=asset_class,
            locale=locale
        )
        
        if raw:
            return response
            
        return self._process_response(response)
    
    def _process_response(self, response: dict) -> dict:
        """Process the API response and format if needed"""
        return pd.DataFrame(response)