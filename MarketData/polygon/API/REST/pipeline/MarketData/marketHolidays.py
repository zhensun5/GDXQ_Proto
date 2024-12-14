import logging
from typing import Dict, Any, Optional, List
from ...utils.overhead import PolygonClient
from polygon.rest.models import MarketHoliday


class PolygonMarketHolidaysHandler:
    """Handler for Polygon.io Market Holidays endpoint"""
    
    def __init__(self, client=None):
        self.logger = logging.getLogger(__name__)
        self.client = client or PolygonClient().get_polygon_client()

    def get_market_holidays(self, 
                          params: Optional[Dict[str, Any]] = None,
                          parse_to_df: bool = True) -> List[MarketHoliday]:
        """
        Get a list of market holidays.
        
        Args:
            params (Optional[Dict[str, Any]]): Additional parameters for the request
            parse_to_df (bool): Whether to parse the response to a DataFrame (default: True)
            
        Returns:
            List[MarketHoliday]: List of market holidays
        """
        holidays = self.client.get_market_holidays(params=params)

        if parse_to_df:
            import pandas as pd
            # Convert holidays to DataFrame
            holiday_data = [
                {
                    'date': h.date,
                    'name': h.name,
                    'status': h.status,
                    'exchange': h.exchange
                }
                for h in holidays if isinstance(h, MarketHoliday)
            ]
            return pd.DataFrame(holiday_data)
            
        return holidays