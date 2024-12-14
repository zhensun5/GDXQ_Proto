import time
import json
import logging
import urllib3
import pandas as pd
from urllib3.util.retry import Retry
import certifi
from ...utils.overhead import PolygonClient

class PolygonBaseHandler:
    def __init__(self, 
                 polygonCarrier = None, 
                 client = None, 
                 num_pools:int=1, 
                 retries:int=5):
        self.logger = logging.getLogger(__name__)
        self.polygonCarrier = polygonCarrier or PolygonClient()
        self.client = client or self.polygonCarrier.client
        self.headers = {
            "Authorization": "Bearer " + self.polygonCarrier.api_key,
            "Accept-Encoding": "gzip",
            "User-Agent": f"Polygon.io PythonClient/unknown",
        }
        self.__init_pool_manager(num_pools, retries, self.headers)

    def authorize_REST(self, url):
        return url + "&apiKey=" + self.polygonCarrier.api_key
    
    def __init_pool_manager(self, num_pools, retries, headers):
        retry_strategy = Retry(
            total=retries,
            status_forcelist=[
                413,
                429,
                499,
                500,
                502,
                503,
                504,
            ],  # default 413, 429, 503
            backoff_factor=0.1,  # [0.0s, 0.2s, 0.4s, 0.8s, 1.6s, ...]
        )

        self.pool_manager = urllib3.PoolManager(
            num_pools=num_pools,
            headers=headers,  # default headers sent with each request.
            ca_certs=certifi.where(),
            cert_reqs="CERT_REQUIRED",
            retries=retry_strategy,  # use the customized Retry instance
        )

    @staticmethod
    def _get_params(polygon_api_func, caller_locals):
        params = (
            caller_locals['client']
                ._get_params(
                    polygon_api_func, 
                    caller_locals
                )
        )
        return params

    def paginate_REST(
            self, 
            url:str, 
            limit:int, 
            sleep_time:int=15, 
            response_parser=None, 
            **params
        ):
        paginate_results = []
        while True:
            resp = self.pool_manager.request('GET', url)
            results, iter_more, url, count = self._process_response_REST(resp, response_parser)
            paginate_results.append(results)
            if iter_more and url:
                if limit:
                    assert count == limit, f"Count mismatch with limit: {count} != {limit}"
                time.sleep(sleep_time)
            else:
                break
        return pd.concat(paginate_results, axis=0)
    
    @staticmethod
    def _process_response_REST(response: dict, add_response_parser = None) -> tuple:
        """Process the REST response and format if needed"""
        # Add any custom processing logic here

        if response.status != 200:
            raise ValueError(f"Error fetching tickers: REST request failed with status {response.status}")

        json_data = json.loads(response.data)
        status = json_data.get("status", None)
        if status != "OK":
            raise ValueError(f"Error fetching tickers: data request from REST failed with status {status}")

        request_id = json_data.get("request_id", None)
        count = json_data.get("count", None)
        next_url = json_data.get("next_url", None)
        if add_response_parser is None:
            results = pd.DataFrame(json_data.get("results", []))
        else:
            results = add_response_parser(json_data).to_dataframe()

        if next_url:
            return results, True, next_url, count
        return results, False, None, count


    def get_REST(self, caller_locals, RESTStatic, polygon_api_func):
        """
        Get list of tickers with pagination support
        
        Returns:
            If pagination needed: Tuple[data, next_url]
            If no pagination: data
        """
        params = PolygonBaseHandler._get_params(polygon_api_func, caller_locals)
        url = RESTStatic.formulate_REST_request_url(**params)
        results = self.paginate_REST(
            url, 
            limit=params.get("limit", None), 
            response_parser=RESTStatic.parse_response,
        )
        return results
