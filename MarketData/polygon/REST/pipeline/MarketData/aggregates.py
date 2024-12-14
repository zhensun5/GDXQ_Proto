import re
import requests
import keyring
from datetime import datetime, timedelta
import time
import logging
from ...utils.overhead import PolygonClient
from utils import parse_aggregates


class PolygonAggregatesHandler:
    def __init__(self, client=None):
        self.client = client or PolygonClient().get_polygon_client()
        print(self.client, type(self.client))

    def _input_validation(self, ticker, multiplier, timespan, from_date, to_date, adjusted, sort, limit):
        # check ticker value
        if not isinstance(ticker, str):
            raise ValueError(f"Invalid ticker value, should be a string, {type(ticker)} provided")
        # check timespan values
        if timespan not in ['second', 'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']:
            raise ValueError("Invalid timespan value")
        # check sort values
        if sort not in ['asc', 'desc']:
            raise ValueError("Invalid sort value")
        # check limit values
        if limit > 50000:
            raise ValueError(f"Invalid limit value, max is 50000, {limit} provided")
        # check from_date format
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', from_date):
            raise ValueError("Invalid from_date format, should be YYYY-MM-DD")
        # check to_date format
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', to_date):
            raise ValueError("Invalid to_date format, should be YYYY-MM-DD")
        # check multiplier values
        if not isinstance(multiplier, int):
            raise ValueError(f"Invalid multiplier value, should be an integer, {type(multiplier)} provided")
        # check adjusted values
        if not isinstance(adjusted, bool):
            raise ValueError(f"Invalid adjusted value, should be a boolean, {type(adjusted)} provided")

    def get_aggregates(
            self, 
            ticker: str, 
            multiplier: int, 
            timespan: str, 
            from_date: str, 
            to_date: str, 
            adjusted: bool = True, 
            sort: str = 'asc', 
            limit: int = 5000,
            parse_to_df: bool = True
        ):
        """
        Fetches aggregate bars for a given ticker over a specified date range.

        :param ticker: The ticker symbol (e.g., 'AAPL').
        :param multiplier: The size of the timespan multiplier.
        :param timespan: The size of the time window (e.g., 'minute', 'day').
        :param from_date: The start date of the aggregate time window (YYYY-MM-DD).
        :param to_date: The end date of the aggregate time window (YYYY-MM-DD).
        :param adjusted: Whether or not the results are adjusted for splits.
        :param sort: Sort the results by timestamp ('asc' or 'desc').
        :param limit: Limits the number of base aggregates queried.
        :return: A list of aggregate data points.
        """
        self._input_validation(ticker, multiplier, timespan, from_date, to_date, adjusted, sort, limit)
        aggs = []
        for a in self.client.list_aggs(
            ticker,
            multiplier,
            timespan,
            from_date,
            to_date,
            adjusted=adjusted,
            sort=sort,
            limit=limit
        ):
            aggs.append(a)
        if parse_to_df:
            return parse_aggregates(aggs)
        return aggs

# Example usage:
# aggregator = PolygonAggregator(api_key="YOUR_API_KEY")
# aggregates = aggregator.get_aggregates("AAPL", 1, "day", "2023-01-01", "2023-01-31")
# print(aggregates)



