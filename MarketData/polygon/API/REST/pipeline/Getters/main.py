import os
import yaml
import logging
import pandas as pd
import numpy as np
import datetime as dt
from pathlib import Path
from ..MarketData.groupedDaily import PolygonGroupedDailyHandler
from ..MarketData.aggregates import PolygonAggregatesHandler
from ..MarketData.tickerTypes import PolygonTickerTypesHandler
from ..MarketData.marketHolidays import PolygonMarketHolidaysHandler
from ..MarketData.tickers import PolygonListTickersHandler
from ..MarketData.tickerTypes import PolygonTickerTypesHandler
from ... import utils
from ...utils.overhead import PolygonClient


class TaskRabbit:
    def __init__(self, params_config_file, client_params={}):
        self.logger = logging.getLogger(__name__)
        self.params_config = yaml.load(open(params_config_file), Loader=yaml.FullLoader)
        self.client = self.get_client(**client_params)
        self.market_time_resolver = self.get_market_time_resolver()

    def get_client(self, client_params={}):
        return PolygonClient(**client_params).get_polygon_client()

    def get_market_time_resolver(self):
        return utils.datetimes.MarketTime(self.params_config["global"].get("market_name", None))
    

class PrepareTaskRabbit(TaskRabbit):
    def __init__(self, params_config_file, client_params={}):
        super().__init__(params_config_file, client_params)

    def get_tickers(self, date:dt.datetime, **params):
        handler = PolygonListTickersHandler(client=self.client)
        params = {**self.params_config.get("tickers", {}), **params}
        return handler.get_tickers(date, **params)



class EnhancedTaskRabbit(TaskRabbit):
    def __init__(self, params_config_file, client_params={}):
        super().__init__(params_config_file, client_params)

    def get_data(self, job_name:str, *args, **kwargs):
        if job_name == "grouped_daily":
            return self._get_and_save_grouped_daily(*args, **kwargs)
        elif job_name == "aggregates":
            return self._get_and_save_aggregates(*args, **kwargs)
        else:
            raise ValueError(f"Invalid job name: {job_name}")
    
    def _get_and_save_grouped_daily(self, mode:str = 'latest', overwrite_existing=False):
        """
        Get daily OHLCV data and save it to a parquet file. Supports two modes:
        1) Build up data inventory for historical periods given a config file.
        2) Get data for the last/today only.
        """
        handler = PolygonGroupedDailyHandler(client=self.client)
        params_config = self.params_config.get("grouped_daily", {})
        run_config = yaml.load(open(params_config.get("run_config_file", None)), Loader=yaml.FullLoader)
        output_dir = run_config.get("output_dir", "./ploygon/md/grouped_daily")

        if not run_config:
                raise ValueError("Run config file is required for historical mode")

        if mode == "historical":
            end_date = run_config.get("end_date", dt.datetime.today())
            start_date = run_config.get("start_date", end_date - dt.timedelta(days=1460))
        elif mode == "latest":
            end_date = dt.datetime.today()
            start_date = end_date - dt.timedelta(days=1460)

        dates = self.market_time_resolver.get_market_days(start_date, end_date)
        
        for date in dates:
            output_file = f"{output_dir}/{date.strftime('%Y-%m-%d')}.parquet"
            if os.path.exists(output_file) and not overwrite_existing:
                self.logger.info(f"input: mode[{mode}]/overwrite[{overwrite_existing}]"
                                 f"- Grouped daily data for {date} already exists, skipping")
                continue

            self.logger.info(f"input: mode[{mode}]/overwrite[{overwrite_existing}]"
                              f"- Getting grouped daily data for {date}")
            data = handler.get_grouped_daily(date, **params_config, parse_to_df=True)
            if isinstance(data, pd.DataFrame):
                data.to_parquet(output_file)
                self.logger.info(f"input: mode[{mode}]/overwrite[{overwrite_existing}]"
                                f"- Grouped daily data for {date} saved to {output_file}")
            else:
                self.logger.error(f"input: mode[{mode}]/overwrite[{overwrite_existing}]"
                                 f"- Failed to retrieve grouped daily data for {date}")
                

    def _get_and_save_aggregates(self, timespan:str, mode:str = 'latest', overwrite_existing=False):
        """
        Get aggregated OHLCV data and save it to a parquet file. Supports two modes:
        1) Build up data inventory for historical periods given a config file.
        2) Get data for the last/today only.
        """
        handler = PolygonAggregatesHandler(client=self.client)
        params_config = self.params_config.get("aggregates", {})
        run_config = yaml.load(open(params_config.get("run_config_file", None)), Loader=yaml.FullLoader)
        output_dir = Path(run_config.get("output_dir", "./polygon/md/aggregates")) / timespan

        if not run_config:
            raise ValueError("Run config file is required for historical mode")

        if mode == "historical":
            end_date = run_config.get("end_date", dt.datetime.today())
            start_date = run_config.get("start_date", end_date - dt.timedelta(days=1095))
        elif mode == "latest":
            end_date = dt.datetime.today()
            start_date = end_date - dt.timedelta(days=1095)

        dates = self.market_time_resolver.get_detail_hours(start_date, end_date)
        for date in dates:
            output_file = f"{output_dir}/{date.strftime('%Y-%m-%d')}.parquet"
            if os.path.exists(output_file) and not overwrite_existing:
                self.logger.info(f"input: mode[{mode}]/overwrite[{overwrite_existing}] "
                               f"- Aggregates data for {date} already exists, skipping")
                continue

            self.logger.info(f"input: mode[{mode}]/overwrite[{overwrite_existing}] "
                           f"- Getting aggregates data for {date}")
            
            
            data = handler.get_aggregates(date, **params_config, parse_to_df=True)
            if isinstance(data, pd.DataFrame):
                data.to_parquet(output_file)
                self.logger.info(f"input: mode[{mode}]/overwrite[{overwrite_existing}] "
                               f"- Aggregates data for {date} saved to {output_file}")
            else:
                self.logger.error(f"input: mode[{mode}]/overwrite[{overwrite_existing}] "
                                f"- Failed to retrieve aggregates data for {date}")
                

    

