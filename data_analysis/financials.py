class Financials:

    def __init__(self):
        pass

    @staticmethod
    def pct_change(input_df):
        """Calculate change percentage of current data from previous data"""
        return input_df.pct_change().fillna(0)


if __name__ == '__main__':
    import pandas as pd
    df = pd.DataFrame()
    stock = Financials.pct_change(df)
