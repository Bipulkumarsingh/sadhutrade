import pandas as pd
from src.constants import ADJ_CLOSE_KEY, CLOSE_KEY, TICKERS_KEY, INPUT_DF_KEY, PRICES_KEY


class Handlers:

    @staticmethod
    def get_standard_input_data(df):

        if df is None:
            raise ValueError("Error: Dataframe has not been provided, there is no data to calculate the requested KPI")

        input_data = {}

        # Set dataFrame keys
        adj_close_key = ADJ_CLOSE_KEY
        close_key = CLOSE_KEY

        if adj_close_key in df.columns is True:
            prices_key = adj_close_key

        else:
            prices_key = close_key

        prices_temp = pd.DataFrame()

        df.columns = pd.MultiIndex.from_tuples(df.columns.values)
        tickers = df.columns.levels[0]

        df_list = []
        for ticker in tickers:
            df_list.append(
                pd.concat(
                    [df[ticker].loc[:, [prices_key]], prices_temp],
                    axis=1,
                    keys=[ticker]
                )
            )

        input_df =\
            pd.concat(
                df_list,
                axis=1
            )

        input_data[PRICES_KEY] = prices_key
        input_data[TICKERS_KEY] = tickers
        input_data[INPUT_DF_KEY] = input_df

        return input_data
