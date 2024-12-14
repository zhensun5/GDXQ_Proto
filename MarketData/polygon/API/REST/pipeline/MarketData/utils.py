import pandas as pd
import numpy as np

# a function to parse list of aggs into a dataframe
def parse_aggregates(aggregates):
    return pd.DataFrame(aggregates)